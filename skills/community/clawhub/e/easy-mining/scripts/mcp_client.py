#!/usr/bin/env python3
"""
Easy Mining MCP Client

Wrapper that calls the Antalpha MCP Server for BTC mining farm management.
All Nonce API logic runs on the remote server (Antalpha MCP → Nonce MCP).

MCP Protocol Flow:
1. POST initialize → get mcp-session-id from response headers
2. POST notifications/initialized → confirm session
3. POST tools/call → actual tool invocation

Usage:
    python3 scripts/mcp_client.py workspace --api-key <key>
    python3 scripts/mcp_client.py farms --api-key <key>
    python3 scripts/mcp_client.py miners --api-key <key> --farm-id <id>
    python3 scripts/mcp_client.py metrics --api-key <key> --farm-id <id>
    python3 scripts/mcp_client.py history --api-key <key> --miner-id <id>
    python3 scripts/mcp_client.py task-batches --api-key <key> --farm-id <id>
    python3 scripts/mcp_client.py create-task --api-key <key> --farm-id <id> --task-name miner.system.reboot --miner-ids <id1> <id2>
    python3 scripts/mcp_client.py get-task --api-key <key> --task-batch-id <id>
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

MCP_SERVER_URL = "https://mcp-skills.ai.antalpha.com/mcp"


class MCPClient:
    """MCP client with proper session management."""

    def __init__(self, server_url: str = MCP_SERVER_URL):
        self.server_url = server_url
        self.session_id: Optional[str] = None

    def _parse_sse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse SSE (Server-Sent Events) response format."""
        for line in response_text.split("\n"):
            if line.startswith("data: ") or line.startswith("data:"):
                data_str = line[5:].strip()
                if data_str and data_str != "[DONE]":
                    try:
                        return json.loads(data_str)
                    except json.JSONDecodeError:
                        continue
        return {}

    def initialize(self) -> bool:
        """
        Initialize MCP session.
        Must be called before any tool calls.
        Returns True if successful.
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "easy-mining-client",
                    "version": "1.0.0",
                },
            },
            "id": 1,
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.server_url, data=data, headers=headers, method="POST"
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                self.session_id = response.headers.get("mcp-session-id")
                response_text = response.read().decode("utf-8")
                result = self._parse_sse_response(response_text)

                if "error" in result:
                    print(f"Initialize error: {result['error']}", file=sys.stderr)
                    return False

                self._send_initialized()
                return True

        except Exception as e:
            print(f"Initialize failed: {e}", file=sys.stderr)
            return False

    def _send_initialized(self) -> None:
        """Send notifications/initialized to complete handshake."""
        if not self.session_id:
            return

        payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": self.session_id,
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.server_url, data=data, headers=headers, method="POST"
            )
            with urllib.request.urlopen(req, timeout=30):
                pass
        except Exception:
            pass

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP tool and return the result.
        Auto-initializes session if needed.
        """
        if not self.session_id:
            if not self.initialize():
                return {"error": "Failed to initialize MCP session"}

        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
            "id": 2,
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": self.session_id,
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.server_url, data=data, headers=headers, method="POST"
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                response_text = response.read().decode("utf-8")
                result = self._parse_sse_response(response_text)

                if "error" in result:
                    return {"error": result["error"]}

                return result.get("result", {})

        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except urllib.error.URLError as e:
            return {"error": f"Connection error: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse response: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}


_client: Optional[MCPClient] = None


def get_client() -> MCPClient:
    global _client
    if _client is None:
        _client = MCPClient()
    return _client


# ─── Tool wrappers ────────────────────────────────────────────────────────────

def get_workspace(api_key: str) -> Dict[str, Any]:
    return get_client().call_tool("easy-mining-get-workspace", {"api_key": api_key})


def list_farms(api_key: str) -> Dict[str, Any]:
    return get_client().call_tool("easy-mining-list-farms", {"api_key": api_key})


def list_agents(api_key: str) -> Dict[str, Any]:
    return get_client().call_tool("easy-mining-list-agents", {"api_key": api_key})


def list_miners(api_key: str, farm_id: str) -> Dict[str, Any]:
    return get_client().call_tool("easy-mining-list-miners", {"api_key": api_key, "farm_id": farm_id})


def list_metrics_history(
    api_key: str,
    farm_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Dict[str, Any]:
    args: Dict[str, Any] = {"api_key": api_key, "farm_id": farm_id}
    if start_date:
        args["from_date"] = start_date
    if end_date:
        args["to_date"] = end_date
    return get_client().call_tool("easy-mining-list-metrics-history", args)


def list_pool_diffs(api_key: str, farm_id: str) -> Dict[str, Any]:
    return get_client().call_tool("easy-mining-list-pool-diffs", {"api_key": api_key, "farm_id": farm_id})


def list_history(
    api_key: str,
    miner_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Dict[str, Any]:
    args: Dict[str, Any] = {"api_key": api_key, "miner_id": miner_id}
    if start_date:
        args["start_date"] = start_date
    if end_date:
        args["end_date"] = end_date
    return get_client().call_tool("easy-mining-list-history", args)


def list_miner_tasks(api_key: str, miner_id: str) -> Dict[str, Any]:
    return get_client().call_tool("easy-mining-list-miner-tasks", {"api_key": api_key, "miner_id": miner_id})


def list_task_batches(
    api_key: str,
    farm_id: str,
    page: int = 1,
    page_size: int = 20,
) -> Dict[str, Any]:
    return get_client().call_tool(
        "easy-mining-list-task-batches",
        {"api_key": api_key, "farm_id": farm_id, "page": page, "page_size": page_size},
    )


def create_task_batch(
    api_key: str,
    farm_id: str,
    task_name: str,
    miner_ids: List[str],
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    args: Dict[str, Any] = {
        "api_key": api_key,
        "farm_id": farm_id,
        "task_name": task_name,
        "miner_ids": miner_ids,
    }
    if params:
        args["params"] = params
    return get_client().call_tool("easy-mining-create-task-batch", args)


def get_task_batch(api_key: str, task_batch_id: str) -> Dict[str, Any]:
    return get_client().call_tool(
        "easy-mining-get-task-batch",
        {"api_key": api_key, "task_batch_id": task_batch_id},
    )


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Easy Mining MCP Client — BTC mining farm management via Antalpha MCP"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # workspace
    ws_p = subparsers.add_parser("workspace", help="Get workspace info")
    ws_p.add_argument("--api-key", required=True, help="Nonce API key")

    # farms
    farms_p = subparsers.add_parser("farms", help="List all farms")
    farms_p.add_argument("--api-key", required=True, help="Nonce API key")

    # agents
    agents_p = subparsers.add_parser("agents", help="List Nonce agents")
    agents_p.add_argument("--api-key", required=True, help="Nonce API key")

    # miners
    miners_p = subparsers.add_parser("miners", help="List miners in a farm")
    miners_p.add_argument("--api-key", required=True, help="Nonce API key")
    miners_p.add_argument("--farm-id", required=True, help="Farm ID")

    # metrics
    metrics_p = subparsers.add_parser("metrics", help="Farm metrics history")
    metrics_p.add_argument("--api-key", required=True, help="Nonce API key")
    metrics_p.add_argument("--farm-id", required=True, help="Farm ID")
    metrics_p.add_argument("--start-date", help="Start date (ISO8601)")
    metrics_p.add_argument("--end-date", help="End date (ISO8601)")

    # pool-diffs
    pd_p = subparsers.add_parser("pool-diffs", help="Pool change records")
    pd_p.add_argument("--api-key", required=True, help="Nonce API key")
    pd_p.add_argument("--farm-id", required=True, help="Farm ID")

    # history
    hist_p = subparsers.add_parser("history", help="Miner performance history")
    hist_p.add_argument("--api-key", required=True, help="Nonce API key")
    hist_p.add_argument("--miner-id", required=True, help="Miner ID")
    hist_p.add_argument("--start-date", help="Start date")
    hist_p.add_argument("--end-date", help="End date")

    # miner-tasks
    mt_p = subparsers.add_parser("miner-tasks", help="Miner task history")
    mt_p.add_argument("--api-key", required=True, help="Nonce API key")
    mt_p.add_argument("--miner-id", required=True, help="Miner ID")

    # task-batches
    tb_p = subparsers.add_parser("task-batches", help="List task batches")
    tb_p.add_argument("--api-key", required=True, help="Nonce API key")
    tb_p.add_argument("--farm-id", required=True, help="Farm ID")
    tb_p.add_argument("--page", type=int, default=1, help="Page number")
    tb_p.add_argument("--page-size", type=int, default=20, help="Page size")

    # create-task
    ct_p = subparsers.add_parser("create-task", help="Create task batch (WRITE - confirm first!)")
    ct_p.add_argument("--api-key", required=True, help="Nonce API key")
    ct_p.add_argument("--farm-id", required=True, help="Farm ID")
    ct_p.add_argument(
        "--task-name",
        required=True,
        choices=[
            "miner.system.reboot",
            "miner.power_mode.update",
            "miner.firmware.update",
            "miner.network.scan",
            "miner.pool.config",
            "miner.light.flash",
        ],
        help="Task type",
    )
    ct_p.add_argument("--miner-ids", nargs="+", required=True, help="Miner IDs")
    ct_p.add_argument("--params", type=json.loads, help="Task params as JSON string")

    # get-task
    gt_p = subparsers.add_parser("get-task", help="Get task batch status")
    gt_p.add_argument("--api-key", required=True, help="Nonce API key")
    gt_p.add_argument("--task-batch-id", required=True, help="Task batch ID")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    result = None

    if args.command == "workspace":
        result = get_workspace(args.api_key)
    elif args.command == "farms":
        result = list_farms(args.api_key)
    elif args.command == "agents":
        result = list_agents(args.api_key)
    elif args.command == "miners":
        result = list_miners(args.api_key, args.farm_id)
    elif args.command == "metrics":
        result = list_metrics_history(
            args.api_key, args.farm_id,
            start_date=getattr(args, "start_date", None),
            end_date=getattr(args, "end_date", None),
        )
    elif args.command == "pool-diffs":
        result = list_pool_diffs(args.api_key, args.farm_id)
    elif args.command == "history":
        result = list_history(
            args.api_key, args.miner_id,
            start_date=getattr(args, "start_date", None),
            end_date=getattr(args, "end_date", None),
        )
    elif args.command == "miner-tasks":
        result = list_miner_tasks(args.api_key, args.miner_id)
    elif args.command == "task-batches":
        result = list_task_batches(args.api_key, args.farm_id, args.page, args.page_size)
    elif args.command == "create-task":
        result = create_task_batch(
            args.api_key, args.farm_id, args.task_name, args.miner_ids,
            params=getattr(args, "params", None),
        )
    elif args.command == "get-task":
        result = get_task_batch(args.api_key, args.task_batch_id)

    if result is not None:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"error": "Unknown command"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
