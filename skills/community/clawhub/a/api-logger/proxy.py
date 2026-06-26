#!/usr/bin/env python3
"""
🦞 Lobster API Proxy - Transparent Anthropic API logging proxy
Intercepts and logs all requests/responses without modification.
"""

import argparse
import asyncio
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone, timedelta

import aiohttp
from aiohttp import web

TZ_OFFSET = timedelta(hours=8)
TZ = timezone(TZ_OFFSET)


def sanitize_headers(headers: dict) -> dict:
    """Remove sensitive auth tokens from headers for logging."""
    sanitized = {}
    sensitive_keys = {
        "x-api-key", "authorization", "proxy-authorization",
        "cookie", "set-cookie",
    }
    for k, v in headers.items():
        lower_k = k.lower()
        if lower_k in sensitive_keys:
            sanitized[k] = mask_key(v)
        else:
            sanitized[k] = v
    return sanitized


def mask_key(value: str) -> str:
    """Mask API key: keep first 8 and last 4 chars."""
    # Strip "Bearer " prefix if present
    prefix = ""
    v = value
    if v.lower().startswith("bearer "):
        prefix = v[:7]
        v = v[7:]
    if len(v) > 12:
        masked = v[:8] + "..." + v[-4:]
    else:
        masked = "***"
    return prefix + masked


def get_log_path(log_dir: str) -> str:
    """Get today's log file path."""
    now = datetime.now(TZ)
    filename = now.strftime("%Y-%m-%d") + ".jsonl"
    return os.path.join(log_dir, filename)


def write_log(log_dir: str, entry: dict):
    """Append one JSON line to today's log file."""
    path = get_log_path(log_dir)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def is_streaming_request(body: bytes) -> bool:
    """Check if the request body indicates streaming."""
    try:
        data = json.loads(body)
        return data.get("stream", False)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False


def parse_sse_content(raw: str) -> str:
    """Parse SSE stream and extract content blocks into a combined response."""
    events = []
    for line in raw.split("\n"):
        line = line.strip()
        if line.startswith("data:"):
            data_str = line[5:].lstrip(" ")
            if data_str == "[DONE]":
                continue
            try:
                events.append(json.loads(data_str))
            except json.JSONDecodeError:
                pass

    # Try to reconstruct the full response from SSE events
    # Anthropic streaming uses: message_start, content_block_start,
    # content_block_delta, content_block_stop, message_delta, message_stop
    full_message = None
    content_blocks = {}  # index -> {"type": ..., "text": ..., "name": ..., "input": ...}
    stop_reason = None
    usage = {}

    for evt in events:
        evt_type = evt.get("type", "")
        if evt_type == "message_start":
            full_message = evt.get("message", {})
            # Capture usage from message_start (contains full input tokens from this provider)
            if full_message.get("usage"):
                usage = dict(full_message["usage"])
        elif evt_type == "content_block_start":
            idx = evt.get("index", 0)
            block = evt.get("content_block", {})
            content_blocks[idx] = dict(block)  # preserve type, name, etc.
        elif evt_type == "content_block_delta":
            idx = evt.get("index", 0)
            delta = evt.get("delta", {})
            if delta.get("type") == "text_delta":
                content_blocks.setdefault(idx, {"type": "text", "text": ""})
                content_blocks[idx]["text"] = content_blocks[idx].get("text", "") + delta.get("text", "")
            elif delta.get("type") == "input_json_delta":
                content_blocks.setdefault(idx, {"type": "tool_use", "input_raw": ""})
                content_blocks[idx]["input_raw"] = content_blocks[idx].get("input_raw", "") + delta.get("partial_json", "")
        elif evt_type == "message_delta":
            delta = evt.get("delta", {})
            stop_reason = delta.get("stop_reason", stop_reason)
            # message_delta usage contains output_tokens; merge into existing usage
            delta_usage = evt.get("usage", {})
            if delta_usage:
                usage.update(delta_usage)

    # Build reconstructed response
    if full_message:
        reconstructed = dict(full_message)
        # Rebuild content array, handling both text and tool_use blocks
        content = []
        for idx in sorted(content_blocks.keys()):
            blk = content_blocks[idx]
            if blk.get("type") == "tool_use":
                # Parse accumulated input JSON
                raw_input = blk.pop("input_raw", "")
                try:
                    blk["input"] = json.loads(raw_input) if raw_input else {}
                except Exception:
                    blk["input"] = {"_raw": raw_input}
                content.append(blk)
            else:
                content.append(blk)
        if content:
            reconstructed["content"] = content
        if stop_reason:
            reconstructed["stop_reason"] = stop_reason
        if usage:
            reconstructed["usage"] = usage  # overwrite with merged usage
        return json.dumps(reconstructed, ensure_ascii=False)

    # Fallback: try to extract at least usage from events
    fallback = {"type": "message", "content": [], "role": "assistant"}
    for evt in events:
        if evt.get("type") == "message_delta":
            u = evt.get("usage", {})
            if u:
                fallback["usage"] = u
        elif evt.get("type") == "message_start":
            msg = evt.get("message", {})
            if msg.get("usage"):
                fallback.setdefault("usage", {}).update(msg["usage"])
    if content_blocks:
        fallback["content"] = [{"type": "text", "text": content_blocks.get(0, "")}]
    return json.dumps(fallback, ensure_ascii=False)


class ProxyHandler:
    def __init__(self, upstream: str, log_dir: str):
        self.upstream = upstream.rstrip("/")
        self.log_dir = log_dir
        self.session: aiohttp.ClientSession | None = None

    async def start(self):
        timeout = aiohttp.ClientTimeout(total=600, connect=30)
        self.session = aiohttp.ClientSession(timeout=timeout)

    async def stop(self):
        if self.session:
            await self.session.close()

    async def handle(self, request: web.Request) -> web.StreamResponse:
        request_id = str(uuid.uuid4())
        start_time = datetime.now(TZ)
        t0 = asyncio.get_event_loop().time()

        # Read request body
        body = await request.read()

        # Build upstream URL: preserve the path after the proxy root
        path = request.path
        query = request.query_string
        upstream_url = self.upstream + path
        if query:
            upstream_url += "?" + query

        # Forward headers (pass through as-is)
        forward_headers = {}
        for k, v in request.headers.items():
            lower_k = k.lower()
            # Skip hop-by-hop headers
            if lower_k in ("host", "transfer-encoding"):
                continue
            forward_headers[k] = v

        streaming = is_streaming_request(body)

        # Parse request body for logging
        try:
            request_body_log = json.loads(body) if body else None
        except (json.JSONDecodeError, UnicodeDecodeError):
            request_body_log = body.decode("utf-8", errors="replace") if body else None

        log_entry = {
            "timestamp": start_time.isoformat(),
            "request_id": request_id,
            "method": request.method,
            "path": path,
            "query": query or None,
            "streaming": streaming,
            "request_headers": sanitize_headers(dict(request.headers)),
            "request_body": request_body_log,
        }

        try:
            async with self.session.request(
                method=request.method,
                url=upstream_url,
                headers=forward_headers,
                data=body,
                allow_redirects=False,
            ) as upstream_resp:

                if streaming and "text/event-stream" in upstream_resp.headers.get("content-type", ""):
                    # Stream response back to client
                    response = web.StreamResponse(
                        status=upstream_resp.status,
                        headers={
                            k: v for k, v in upstream_resp.headers.items()
                            if k.lower() not in ("transfer-encoding", "content-encoding")
                        },
                    )
                    await response.prepare(request)

                    stream_chunks = []
                    async for chunk in upstream_resp.content.iter_any():
                        stream_chunks.append(chunk)
                        await response.write(chunk)

                    await response.write_eof()

                    # Log the complete streamed response
                    t1 = asyncio.get_event_loop().time()
                    raw_stream = b"".join(stream_chunks).decode("utf-8", errors="replace")

                    log_entry["response_status"] = upstream_resp.status
                    log_entry["response_headers"] = sanitize_headers(dict(upstream_resp.headers))
                    log_entry["response_body_raw_stream"] = raw_stream
                    try:
                        log_entry["response_body_parsed"] = json.loads(
                            parse_sse_content(raw_stream)
                        )
                    except (json.JSONDecodeError, Exception):
                        log_entry["response_body_parsed"] = None
                    log_entry["duration_ms"] = round((t1 - t0) * 1000, 2)

                    write_log(self.log_dir, log_entry)
                    return response

                else:
                    # Non-streaming: read full response body
                    resp_body = await upstream_resp.read()
                    t1 = asyncio.get_event_loop().time()

                    # Build response to client
                    response = web.Response(
                        status=upstream_resp.status,
                        body=resp_body,
                        headers={
                            k: v for k, v in upstream_resp.headers.items()
                            if k.lower() not in ("transfer-encoding", "content-encoding", "content-length")
                        },
                    )

                    # Log
                    try:
                        resp_body_log = json.loads(resp_body)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        resp_body_log = resp_body.decode("utf-8", errors="replace")

                    log_entry["response_status"] = upstream_resp.status
                    log_entry["response_headers"] = sanitize_headers(dict(upstream_resp.headers))
                    log_entry["response_body"] = resp_body_log
                    log_entry["duration_ms"] = round((t1 - t0) * 1000, 2)

                    write_log(self.log_dir, log_entry)
                    return response

        except Exception as e:
            t1 = asyncio.get_event_loop().time()
            log_entry["response_status"] = 502
            log_entry["error"] = str(e)
            log_entry["duration_ms"] = round((t1 - t0) * 1000, 2)
            write_log(self.log_dir, log_entry)

            return web.json_response(
                {"error": f"Proxy error: {e}"},
                status=502,
            )


async def run_proxy(port: int, upstream: str, log_dir: str):
    handler = ProxyHandler(upstream, log_dir)
    await handler.start()

    app = web.Application(client_max_size=100 * 1024 * 1024)  # 100MB max
    app.router.add_route("*", "/{path_info:.*}", handler.handle)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", port)
    await site.start()

    print(f"🦞 Lobster API Proxy running on http://127.0.0.1:{port}")
    print(f"   Upstream: {upstream}")
    print(f"   Logs:     {log_dir}")
    print(f"   Press Ctrl+C to stop")

    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
    finally:
        await handler.stop()
        await runner.cleanup()
        print("\n🦞 Proxy stopped. Bye!")


def main():
    parser = argparse.ArgumentParser(description="🦞 Lobster API Proxy")
    parser.add_argument("--port", type=int, default=8888, help="Local port (default: 8888)")
    parser.add_argument("--upstream", type=str, default="http://model.mify.ai.srv/anthropic",
                        help="Upstream API URL")
    parser.add_argument("--log-dir", type=str,
                        default="/Users/xm_plus/.openclaw/workspace/company/api-logs",
                        help="Log directory")
    args = parser.parse_args()

    os.makedirs(args.log_dir, exist_ok=True)

    try:
        asyncio.run(run_proxy(args.port, args.upstream, args.log_dir))
    except KeyboardInterrupt:
        print("\n🦞 Caught Ctrl+C, shutting down...")


if __name__ == "__main__":
    main()
