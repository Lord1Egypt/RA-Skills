#!/usr/bin/env python3
"""
Shared MCP helpers for Filtrix video generation scripts.
"""

import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import urlparse

PROTOCOL_VERSION = "2025-03-26"
DEFAULT_MCP_URL = "https://mcp.filtrix.ai/mcp"

VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".m3u8"}
SUCCESS_STATUSES = {"succeeded", "success", "completed", "done", "ready", "finished", "generated"}
FAILURE_STATUSES = {"failed", "error", "cancelled", "canceled", "rejected", "timeout", "timed_out"}


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
                    "name": "filtrix-video-gen",
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


def get_mcp_env() -> tuple[str, str]:
    api_key = os.environ.get("FILTRIX_MCP_API_KEY") or os.environ.get("MCP_API_KEY")
    if not api_key:
        raise RuntimeError("FILTRIX_MCP_API_KEY is required")
    endpoint = os.environ.get("FILTRIX_MCP_URL", DEFAULT_MCP_URL)
    return endpoint, api_key


def _walk_json(node: Any) -> Iterator[Any]:
    stack = [node]
    while stack:
        current = stack.pop()
        yield current
        if isinstance(current, dict):
            for value in current.values():
                if isinstance(value, (dict, list)):
                    stack.append(value)
        elif isinstance(current, list):
            for value in current:
                if isinstance(value, (dict, list)):
                    stack.append(value)


def _find_string_by_keys(payload: Any, keys: tuple[str, ...]) -> str | None:
    key_set = {k.lower() for k in keys}
    for node in _walk_json(payload):
        if not isinstance(node, dict):
            continue
        for key, value in node.items():
            if isinstance(key, str) and key.lower() in key_set and isinstance(value, str):
                value = value.strip()
                if value:
                    return value
    return None


def _normalize_status(status: str | None) -> str:
    if not isinstance(status, str):
        return ""
    return status.strip().lower().replace("-", "_").replace(" ", "_")


def is_success_status(status: str | None) -> bool:
    return _normalize_status(status) in SUCCESS_STATUSES


def is_failure_status(status: str | None) -> bool:
    return _normalize_status(status) in FAILURE_STATUSES


def extract_request_id(payload: dict[str, Any]) -> str | None:
    request_id = _find_string_by_keys(
        payload,
        ("request_id", "requestId", "task_id", "taskId", "job_id", "jobId"),
    )
    if request_id:
        return request_id

    fallback = _find_string_by_keys(payload, ("id",))
    if fallback and len(fallback) >= 8:
        return fallback
    return None


def extract_status(payload: dict[str, Any]) -> str | None:
    return _find_string_by_keys(payload, ("status", "state", "task_status", "job_status"))


def _is_http_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def _looks_like_video_url(value: str) -> bool:
    lower = value.lower()
    if any(ext in lower for ext in VIDEO_EXTENSIONS):
        return True
    return "video" in lower or "download" in lower


def extract_video_url(payload: dict[str, Any]) -> str | None:
    explicit = _find_string_by_keys(
        payload,
        (
            "video_url",
            "videoUrl",
            "download_url",
            "downloadUrl",
            "result_url",
            "resultUrl",
            "output_url",
            "outputUrl",
            "file_url",
            "fileUrl",
            "signed_url",
            "signedUrl",
        ),
    )
    if explicit and _is_http_url(explicit):
        return explicit

    generic = _find_string_by_keys(payload, ("url",))
    if generic and _is_http_url(generic) and _looks_like_video_url(generic):
        return generic
    return None


def extract_error_message(payload: dict[str, Any]) -> str | None:
    message = _find_string_by_keys(
        payload,
        (
            "error_message",
            "errorMessage",
            "message",
            "detail",
            "reason",
            "error",
        ),
    )
    if message:
        return message
    return None


def download_binary(url: str) -> bytes:
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=240) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Signed URL HTTP {exc.code}: {detail}")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Signed URL network error: {exc.reason}")


def _sanitize_name(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return safe[:80] if safe else "video"


def build_output_path(video_url: str, output: str | None, request_id: str | None = None) -> Path:
    if output:
        out_path = Path(output)
    else:
        parsed = urlparse(video_url)
        suffix = Path(parsed.path).suffix.lower()
        if suffix not in VIDEO_EXTENSIONS:
            suffix = ".mp4"
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rid = _sanitize_name(request_id or "video")
        out_path = Path(f"/tmp/filtrix_mcp_{rid}_{stamp}{suffix}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    return out_path
