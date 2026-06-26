import asyncio
import json
import os
import sys
from typing import Any

from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

DEFAULT_SSE_URL = "http://127.0.0.1:9876/"
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")


def get_sse_url() -> str:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            if isinstance(cfg, dict) and isinstance(cfg.get("sse_url"), str) and cfg["sse_url"].strip():
                return cfg["sse_url"].strip()
        except Exception:
            pass
    return DEFAULT_SSE_URL


def dump_content_item(item: Any) -> Any:
    if hasattr(item, "model_dump"):
        try:
            return item.model_dump()
        except Exception:
            pass
    if isinstance(item, dict):
        return item
    out = {"type": getattr(item, "type", type(item).__name__)}
    for key in ("text", "data", "mimeType", "uri", "annotations", "meta"):
        if hasattr(item, key):
            out[key] = getattr(item, key)
    return out


async def open_session():
    sse_url = get_sse_url()
    streams_cm = sse_client(sse_url)
    streams = await streams_cm.__aenter__()
    read_stream, write_stream = streams
    session_cm = ClientSession(read_stream, write_stream)
    session = await session_cm.__aenter__()
    try:
        await session.initialize()
        return sse_url, streams_cm, session_cm, session
    except Exception:
        await session_cm.__aexit__(*sys.exc_info())
        await streams_cm.__aexit__(*sys.exc_info())
        raise


async def close_session(streams_cm, session_cm, session):
    await session_cm.__aexit__(None, None, None)
    await streams_cm.__aexit__(None, None, None)


async def list_tools() -> int:
    sse_url, streams_cm, session_cm, session = await open_session()
    try:
        resp = await session.list_tools()
        tools = getattr(resp, "tools", []) or []
        print(json.dumps({
            "sse_url": sse_url,
            "count": len(tools),
            "tools": [
                {
                    "name": t.name,
                    "description": getattr(t, "description", None),
                    "inputSchema": getattr(t, "inputSchema", None),
                }
                for t in tools
            ],
        }, indent=2, ensure_ascii=False, default=str))
        return 0
    finally:
        await close_session(streams_cm, session_cm, session)


async def call_tool(tool_name: str, args: dict[str, Any]) -> int:
    sse_url, streams_cm, session_cm, session = await open_session()
    try:
        result = await session.call_tool(tool_name, args)
        payload = {
            "sse_url": sse_url,
            "tool": tool_name,
            "args": args,
            "isError": getattr(result, "isError", False),
            "content": [dump_content_item(x) for x in (getattr(result, "content", None) or [])],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
        return 0 if not payload["isError"] else 2
    finally:
        await close_session(streams_cm, session_cm, session)


def usage() -> int:
    print(
        "Usage:\n"
        "  python ./skills/burp-mcp/scripts/burp_mcp.py list-tools\n"
        "  python ./skills/burp-mcp/scripts/burp_mcp.py call <tool_name> <json_args>\n\n"
        "Examples:\n"
        "  python ./skills/burp-mcp/scripts/burp_mcp.py list-tools\n"
        "  python ./skills/burp-mcp/scripts/burp_mcp.py call get_proxy_http_history \"{\\\"offset\\\":0,\\\"count\\\":5}\"\n"
    )
    return 1


async def main() -> int:
    if len(sys.argv) < 2:
        return usage()

    cmd = sys.argv[1]
    if cmd == "list-tools":
        return await list_tools()

    if cmd == "call" and len(sys.argv) >= 4:
        tool_name = sys.argv[2]
        try:
            args = json.loads(sys.argv[3])
        except json.JSONDecodeError as e:
            print(f"Invalid JSON args: {e}", file=sys.stderr)
            return 1
        if not isinstance(args, dict):
            print("JSON args must be an object", file=sys.stderr)
            return 1
        return await call_tool(tool_name, args)

    return usage()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
