#!/usr/bin/env python3
"""
Filtrix MCP Image Generator.

This script calls Filtrix Remote MCP (`/mcp`) using API Key auth and invokes
`generate_image_text`.

Environment variables:
  FILTRIX_MCP_API_KEY   Required. Your Filtrix MCP API key.
  FILTRIX_MCP_URL       Optional. Defaults to https://mcp.filtrix.ai/mcp

Usage:
  python scripts/generate.py --prompt "a cat in space" --mode gpt-image-1
  python scripts/generate.py --prompt "city at sunset" --mode nano-banana
  python scripts/generate.py --prompt "cinematic forest" --mode nano-banana-2 --resolution 2K --enhance-mode
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

PROTOCOL_VERSION = "2025-03-26"
DEFAULT_MCP_URL = "https://mcp.filtrix.ai/mcp"
MODELS = ("gpt-image-1", "nano-banana", "nano-banana-2")
SIZES = ("1024x1024", "1536x1024", "1024x1536", "auto")
RESOLUTIONS = ("1K", "2K", "4K")


class McpClient:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key
        self.session_id: str | None = None
        self.request_id = 0

    def _next_id(self) -> str:
        self.request_id += 1
        return str(self.request_id)

    def _post(self, payload: dict[str, Any], include_id: bool = True) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session_id:
            headers["mcp-session-id"] = self.session_id

        req = urllib.request.Request(self.endpoint, data=body, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw = resp.read().decode("utf-8")
                session_id = resp.headers.get("mcp-session-id")
                if session_id:
                    self.session_id = session_id
        except urllib.error.HTTPError as exc:
            err = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"MCP HTTP {exc.code}: {err}")
        except urllib.error.URLError as exc:
            raise RuntimeError(f"MCP network error: {exc.reason}")

        # Most servers return JSON. If event-stream slips through, parse the last data frame.
        text = raw.strip()
        if text.startswith("data:"):
            data_lines = [ln[5:].strip() for ln in text.splitlines() if ln.startswith("data:")]
            text = data_lines[-1] if data_lines else "{}"

        try:
            message = json.loads(text) if text else {}
        except json.JSONDecodeError:
            raise RuntimeError(f"Unexpected MCP response: {text[:500]}")

        if include_id and isinstance(message, dict) and "error" in message:
            raise RuntimeError(f"MCP JSON-RPC error: {json.dumps(message['error'], ensure_ascii=False)}")

        return message if isinstance(message, dict) else {}

    def initialize(self) -> None:
        initialize_req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {
                    "name": "filtrix-skills-generate",
                    "version": "1.0.0",
                },
            },
        }
        self._post(initialize_req)

        initialized_notice = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        }
        # Notification may return empty body; ignore parse errors by best effort.
        try:
            self._post(initialized_notice, include_id=False)
        except RuntimeError:
            pass

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        call_req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments,
            },
        }
        message = self._post(call_req)

        result = message.get("result") if isinstance(message, dict) else None
        if not isinstance(result, dict):
            raise RuntimeError(f"Invalid MCP tools/call response: {json.dumps(message, ensure_ascii=False)[:500]}")

        content = result.get("content")
        if not isinstance(content, list) or not content:
            raise RuntimeError(f"Invalid MCP tool content: {json.dumps(result, ensure_ascii=False)[:500]}")

        first = content[0]
        if not isinstance(first, dict) or first.get("type") != "text":
            raise RuntimeError(f"Unsupported MCP content item: {json.dumps(first, ensure_ascii=False)[:500]}")

        text = first.get("text")
        if not isinstance(text, str):
            raise RuntimeError("MCP tool returned non-text content")

        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            raise RuntimeError(f"MCP tool text is not JSON: {text[:500]}")

        if not isinstance(payload, dict):
            raise RuntimeError("MCP tool payload is not an object")

        return payload


def download_image(url: str) -> bytes:
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Signed URL HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Signed URL network error: {exc.reason}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate images via Filtrix MCP")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--mode", default="gpt-image-1", choices=MODELS,
                        help="Model selector: gpt-image-1 | nano-banana | nano-banana-2")
    parser.add_argument("--size", default="1024x1024", choices=SIZES,
                        help="Output size")
    parser.add_argument("--resolution", default="1K", choices=RESOLUTIONS,
                        help="Resolution (only used by nano-banana-2)")
    parser.add_argument("--search-mode", action="store_true",
                        help="Enable search mode (only used by nano-banana-2)")
    parser.add_argument("--enhance-mode", action="store_true",
                        help="Enable enhanced thinking (only used by nano-banana-2)")
    parser.add_argument("--idempotency-key", default=None,
                        help="Optional idempotency key; auto-generated if omitted")
    parser.add_argument("--output", default=None,
                        help="Output image path (default: /tmp/filtrix_mcp_<timestamp>.png)")
    parser.add_argument("--print-json", action="store_true",
                        help="Print raw MCP tool payload")
    args = parser.parse_args()

    mcp_api_key = os.environ.get("FILTRIX_MCP_API_KEY") or os.environ.get("MCP_API_KEY")
    if not mcp_api_key:
        print("ERROR: FILTRIX_MCP_API_KEY is required", file=sys.stderr)
        sys.exit(1)

    mcp_url = os.environ.get("FILTRIX_MCP_URL", DEFAULT_MCP_URL)
    request_key = args.idempotency_key or f"gen-{uuid.uuid4().hex}"

    client = McpClient(endpoint=mcp_url, api_key=mcp_api_key)

    try:
        client.initialize()
        tool_payload = client.call_tool(
            "generate_image_text",
            {
                "prompt": args.prompt,
                "mode": args.mode,
                "size": args.size,
                "resolution": args.resolution,
                "search_mode": bool(args.search_mode),
                "enhance_mode": bool(args.enhance_mode),
                "idempotency_key": request_key,
            },
        )
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.print_json:
        print(json.dumps(tool_payload, ensure_ascii=False, indent=2))

    if tool_payload.get("ok") is not True:
        print(f"ERROR: generation failed: {json.dumps(tool_payload, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    image_url = tool_payload.get("image_url")
    if not isinstance(image_url, str) or not image_url:
        print(f"ERROR: MCP did not return image_url: {json.dumps(tool_payload, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    try:
        image_bytes = download_image(image_url)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if not args.output:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"/tmp/filtrix_mcp_{args.mode}_{ts}.png"

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(image_bytes)

    credits_used = tool_payload.get("credits_used")
    print(f"OK: {out_path} ({len(image_bytes)} bytes)")
    print(f"mode={args.mode} idempotency_key={request_key} credits_used={credits_used}")


if __name__ == "__main__":
    main()
