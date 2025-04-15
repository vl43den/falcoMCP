from flask import Flask, request, jsonify
from jsonrpcserver import method, dispatch
from falcomcp.mcp_methods import mcp_get_alerts, mcp_list_rules

app = Flask(__name__)

# Register our MCP methods with jsonrpcserver
@method
def get_alerts(start_time: str, end_time: str):
    return mcp_get_alerts(start_time, end_time)

@method
def list_rules():
    return mcp_list_rules()

@app.route("/rpc", methods=["POST"])
def handle_rpc():
    request_data = request.get_data().decode()
    response = dispatch(request_data)
    if response.wanted:
        return jsonify(response.deserialized)
    return "", 204

if __name__ == "__main__":
    # For a production deployment, ensure to run behind HTTPS and with proper access controls.
    app.run(host="0.0.0.0", port=5000, debug=False)