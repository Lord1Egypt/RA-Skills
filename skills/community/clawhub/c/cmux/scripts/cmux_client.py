#!/usr/bin/env python3
"""cmux socket client helper."""
import json
import os
import socket
import sys

SOCKET_PATH = os.environ.get("CMUX_SOCKET_PATH", "/tmp/cmux.sock")


def rpc(method, params=None, req_id=1):
    """Send a JSON-RPC request to cmux socket."""
    payload = {"id": req_id, "method": method, "params": params or {}}
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(SOCKET_PATH)
            sock.sendall(json.dumps(payload).encode("utf-8") + b"\n")
            response = sock.recv(65536).decode("utf-8")
            return json.loads(response)
    except (FileNotFoundError, ConnectionRefusedError) as e:
        return {"error": f"Socket not available: {SOCKET_PATH}", "details": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: cmux_client.py <method> [params_json]")
        print("Example: cmux_client.py workspace.list")
        print("         cmux_client.py surface.send_text '{\"text\": \"ls\\n\"}'")
        sys.exit(1)

    method = sys.argv[1]
    params = {}
    if len(sys.argv) > 2:
        params = json.loads(sys.argv[2])

    result = rpc(method, params)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
