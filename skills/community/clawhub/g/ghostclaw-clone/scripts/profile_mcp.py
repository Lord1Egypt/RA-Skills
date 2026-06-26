#!/usr/bin/env python3
"""
Profile MCP server performance for Ghostclaw tools.
Measures round-trip time for each tool (ghostclaw_analyze, etc.).
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

# Add src to path for ghostclaw imports (not strictly needed for MCP profiling)
sys.path.insert(0, str(Path(__file__).parent.parent / "ghostclaw-clone" / "src"))

MCP_SERVER_CMD = [sys.executable, "-m", "ghostclaw_mcp.server"]

# MCP protocol version
PROTOCOL_VERSION = "2024-11-05"

def send_jsonrpc(proc, method, params=None, req_id=1, is_notification=False):
    """Send a JSON-RPC request to the server's stdin and return the response dict."""
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {}
    }
    if not is_notification:
        request["id"] = req_id
    payload = (json.dumps(request) + "\n").encode()
    proc.stdin.write(payload)
    proc.stdin.flush()
    if is_notification:
        return None
    # Read response line
    line = proc.stdout.readline()
    if not line:
        raise RuntimeError("No response from MCP server")
    response = json.loads(line.decode())
    if "error" in response:
        raise RuntimeError(f"MCP error: {response['error']}")
    return response.get("result")

async def profile_mcp_tools(repo_path: str):
    print(f"🔬 Profiling MCP server on repo: {repo_path}")
    # Start server
    proc = subprocess.Popen(
        MCP_SERVER_CMD,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,  # binary mode
        bufsize=0
    )
    try:
        # Give server a moment to start
        time.sleep(0.5)

        # Initialize
        init_params = {
            "protocolVersion": PROTOCOL_VERSION,
            "clientInfo": {"name": "ghostclaw-profiler", "version": "0.1"},
            "capabilities": {}
        }
        result = send_jsonrpc(proc, "initialize", init_params, req_id=1)
        print(f"✅ Initialized: {result.get('serverInfo', {}).get('name')}")

        # Prepare for tool calls: send initialized notification (no id)
        send_jsonrpc(proc, "notifications/initialized", None, is_notification=True)

        tools_to_profile = [
            ("ghostclaw_analyze", {"repo_path": repo_path}),
            ("ghostclaw_get_ghosts", {"repo_path": repo_path}),
            ("ghostclaw_refactor_plan", {"repo_path": repo_path}),
        ]

        for idx, (tool_name, args) in enumerate(tools_to_profile, start=2):
            print(f"\n⏱️  Profiling {tool_name}...")
            start = time.perf_counter()
            result = send_jsonrpc(proc, "tools/call", {"name": tool_name, "arguments": args}, req_id=idx)
            elapsed = time.perf_counter() - start
            print(f"   Completed in {elapsed:.3f}s")
            result_size = len(json.dumps(result).encode())
            print(f"   Result size: {result_size} bytes")

        # Shutdown
        send_jsonrpc(proc, "shutdown", None, req_id=5)
        send_jsonrpc(proc, "exit", None, is_notification=True)  # notification

    finally:
        proc.stdin.close()
        proc.stdout.close()
        stderr_output = proc.stderr.read().decode(errors="ignore")
        proc.stderr.close()
        proc.wait(timeout=5)
        if stderr_output:
            print("Server stderr:", stderr_output)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Profile MCP server tools")
    parser.add_argument("repo_path", help="Path to repository to analyze")
    args = parser.parse_args()

    repo_path = Path(args.repo_path).resolve()
    if not repo_path.exists():
        print(f"Error: repo path does not exist: {repo_path}")
        sys.exit(1)

    asyncio.run(profile_mcp_tools(str(repo_path)))
