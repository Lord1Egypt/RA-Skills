#!/usr/bin/env python3
"""Odoo Drive Thru MCP client.

Connects to the Odoo `drivethru_mcp` module's MCP server (Streamable HTTP)
and lets the agent discover and call the curated Odoo tools. Auth is a static
bearer key — no OAuth — so the two subcommands are fully non-interactive.

Subcommands
-----------
  tools              List the tools the Odoo MCP server exposes (tools/list).
  call <tool> [json] Call a tool (tools/call). Arguments are a JSON object
                     passed as the 2nd arg or on stdin.

Environment
-----------
  ODOO_MCP_URL    Full MCP endpoint, e.g. https://odoo.example.com/drivethru_mcp/v1
  ODOO_MCP_TOKEN  The drivethru.mcp_key value, sent as `Authorization: Bearer`.

Output
------
Every command prints a single JSON object on stdout. On failure it prints
`{"error": {"type": ..., "message": ...}}` and exits non-zero:
  config_error (exit 2)  — ODOO_MCP_URL / ODOO_MCP_TOKEN missing
  invalid_arguments (2)  — bad CLI / JSON args
  connection_error       — server unreachable / auth rejected / transport error
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import anyio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


def _fail(error_type: str, message: str, code: int = 1) -> int:
    json.dump({"error": {"type": error_type, "message": message}}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return code


def _config():
    url = (os.environ.get("ODOO_MCP_URL") or "").strip()
    token = (os.environ.get("ODOO_MCP_TOKEN") or "").strip()
    return url, token


async def _with_session(url: str, headers: dict, fn):
    async with streamablehttp_client(url, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return await fn(session)


async def _run(fn) -> int:
    url, token = _config()
    if not url or not token:
        return _fail(
            "config_error",
            "Set ODOO_MCP_URL and ODOO_MCP_TOKEN before using this skill.",
            code=2,
        )
    headers = {"Authorization": f"Bearer {token}"}
    try:
        return await _with_session(url, headers, fn)
    except Exception as exc:  # noqa: BLE001 - normalize transport/auth errors
        cause = _unwrap(exc)
        return _fail("connection_error", f"{type(cause).__name__}: {cause}")


def _unwrap(exc: BaseException) -> BaseException:
    """Drill into anyio/ExceptionGroup wrappers to the most useful cause."""
    seen = set()
    while True:
        if id(exc) in seen:
            return exc
        seen.add(id(exc))
        inner = getattr(exc, "exceptions", None)
        if inner:
            exc = inner[0]
            continue
        return exc


async def cmd_tools(args) -> int:
    async def fn(session):
        result = await session.list_tools()
        tools = [
            {"name": t.name, "description": t.description, "inputSchema": t.inputSchema}
            for t in result.tools
        ]
        print(json.dumps({"tools": tools}, indent=2))
        return 0

    return await _run(fn)


async def cmd_call(args) -> int:
    if args.json_args is not None:
        raw = args.json_args
    elif not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    else:
        raw = ""
    raw = raw or "{}"
    try:
        arguments = json.loads(raw)
    except json.JSONDecodeError as e:
        return _fail("invalid_arguments", f"Tool arguments must be valid JSON: {e}", code=2)
    if not isinstance(arguments, dict):
        return _fail("invalid_arguments", "Tool arguments must be a JSON object.", code=2)

    async def fn(session):
        result = await session.call_tool(args.tool, arguments)
        payload = result.model_dump(mode="json", exclude_none=True)
        print(json.dumps(payload, indent=2))
        return 1 if result.isError else 0

    return await _run(fn)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Odoo Drive Thru MCP client.")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("tools", help="List the Odoo MCP tools (tools/list).")
    sp.set_defaults(func=cmd_tools)

    sp = sub.add_parser("call", help="Call an Odoo MCP tool (tools/call).")
    sp.add_argument("tool", help="Tool name (see `tools`).")
    sp.add_argument("json_args", nargs="?", default=None,
                    help="JSON object of arguments. Omit to read from stdin.")
    sp.set_defaults(func=cmd_call)
    return p


def main() -> int:
    args = build_parser().parse_args()
    try:
        return anyio.run(lambda: args.func(args))
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
