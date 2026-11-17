#!/usr/bin/env python3
"""Read-only health check for Facetory's local Streamable HTTP MCP server."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request


def post(url: str, payload: dict, session_id: str | None = None):
    headers = {
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    response = urllib.request.urlopen(request, timeout=5)
    body = response.read().decode("utf-8", "replace")
    events = []
    for line in body.splitlines():
        if line.startswith("data: ") and line[6:].strip():
            events.append(json.loads(line[6:]))
    return response.headers.get("Mcp-Session-Id"), events


def result_for(events: list[dict], request_id: int) -> dict:
    for event in events:
        if event.get("id") == request_id:
            if "error" in event:
                raise RuntimeError(json.dumps(event["error"], ensure_ascii=False))
            return event["result"]
    raise RuntimeError(f"missing JSON-RPC response for id {request_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:39093/mcp")
    args = parser.parse_args()
    initialize = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "facetory-skill-check", "version": "1"},
        },
    }
    try:
        session, events = post(args.url, initialize)
        info = result_for(events, 1)
        if not session:
            raise RuntimeError("server did not return Mcp-Session-Id")
        _, events = post(
            args.url,
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            session,
        )
        tools = result_for(events, 2).get("tools", [])
    except (OSError, urllib.error.URLError, ValueError, RuntimeError) as error:
        print(f"Facetory MCP check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
    server = info.get("serverInfo", {})
    print(f"server={server.get('name', 'unknown')} version={server.get('version', 'unknown')}")
    print(f"protocol={info.get('protocolVersion', 'unknown')} tools={len(tools)}")
    for tool in tools:
        print(tool.get("name", "<unnamed>"))


if __name__ == "__main__":
    main()
