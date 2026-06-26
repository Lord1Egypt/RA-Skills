#!/usr/bin/env python3
"""Shared safety helpers for local image validation and log redaction."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional, Tuple


SENSITIVE_FIELD_NAMES = {
    "ak",
    "api_key",
    "apikey",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "x-openclaw-ak",
    "secret",
    "password",
    "key",
}

SENSITIVE_HEADER_NAMES = {
    "x-openclaw-ak",
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
}

SUPPORTED_IMAGE_TYPES = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp",
    "gif": "image/gif",
}


def _redact_header_value(name: str, value: str) -> str:
    if name.strip().lower() in SENSITIVE_HEADER_NAMES:
        return "<redacted>"
    return value


def summarize_http_request(
    method: str,
    url: str,
    headers: dict[str, str],
    *,
    data: Optional[bytes] = None,
    multipart_hint: Optional[str] = None,
    timeout: Optional[int] = 120,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "transport": "python-urllib",
        "method": method.upper(),
        "url": url,
    }

    if timeout is not None:
        summary["timeout_sec"] = timeout

    if headers:
        summary["headers"] = {
            key: _redact_header_value(key, value)
            for key, value in headers.items()
        }

    if multipart_hint:
        summary["body"] = {
            "type": "multipart",
            "summary": multipart_hint,
        }
    elif data is not None:
        content_type = str(headers.get("Content-Type", "")).lower()
        body_type = "json" if "json" in content_type else "bytes"
        summary["body"] = {
            "type": body_type,
            "bytes": len(data),
        }

    return summary


def _looks_like_jpeg(data: bytes) -> bool:
    return len(data) >= 3 and data[:3] == b"\xff\xd8\xff"


def _looks_like_png(data: bytes) -> bool:
    return len(data) >= 8 and data[:8] == b"\x89PNG\r\n\x1a\n"


def _looks_like_gif(data: bytes) -> bool:
    return data.startswith((b"GIF87a", b"GIF89a"))


def _looks_like_webp(data: bytes) -> bool:
    return len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"


SIGNATURE_CHECKS = {
    "jpg": _looks_like_jpeg,
    "jpeg": _looks_like_jpeg,
    "png": _looks_like_png,
    "gif": _looks_like_gif,
    "webp": _looks_like_webp,
}


def detect_local_image(path_like: str | Path) -> Tuple[str, str]:
    path = Path(path_like)
    if not path.is_file():
        raise ValueError(f"File not found: {path}")

    suffix = path.suffix.lower().lstrip(".")
    if suffix not in SUPPORTED_IMAGE_TYPES:
        supported = ", ".join(f".{ext}" for ext in sorted(SUPPORTED_IMAGE_TYPES))
        raise ValueError(f"Unsupported image file type: {path.suffix or '<none>'}. Supported types: {supported}")

    with path.open("rb") as handle:
        data = handle.read(16)
    if not SIGNATURE_CHECKS[suffix](data):
        raise ValueError(f"Unsupported or invalid image file: {path}")

    return suffix, SUPPORTED_IMAGE_TYPES[suffix]


def redact_json_like(data: Any) -> Any:
    if isinstance(data, dict):
        out = {}
        for key, value in data.items():
            normalized_key = str(key).strip().lower()
            if normalized_key in SENSITIVE_FIELD_NAMES:
                out[key] = "<redacted>"
            else:
                out[key] = redact_json_like(value)
        return out
    if isinstance(data, list):
        return [redact_json_like(item) for item in data]
    return data


def redact_json_text(
    text: str,
    *,
    ak: str = "",
    http_code: Optional[int] = None,
    max_len: int = 20000,
) -> Any:
    if len(text) > max_len:
        text = text[:max_len] + "...(truncated)"
    if ak:
        text = text.replace(ak, "<redacted>")

    try:
        body = json.loads(text)
    except json.JSONDecodeError:
        envelope: Any
        if http_code is not None:
            envelope = {"http_code": http_code, "_raw": text}
        else:
            envelope = {"_raw": text}
    else:
        if http_code is not None:
            envelope = {"http_code": http_code, "body": body}
        else:
            envelope = body

    return redact_json_like(envelope)


def _count_render_items(items_obj: Any) -> Optional[dict[str, int]]:
    if isinstance(items_obj, list):
        item_count = len(items_obj)
        completed_count = sum(
            1
            for item in items_obj
            if isinstance(item, dict) and str(item.get("res_img", "")).startswith("http")
        )
        return {
            "batch_count": 1,
            "item_count": item_count,
            "completed_count": completed_count,
        }

    if not isinstance(items_obj, dict):
        return None

    batch_count = 0
    item_count = 0
    completed_count = 0
    for batch_value in items_obj.values():
        if not isinstance(batch_value, dict):
            continue
        sub_items = batch_value.get("items")
        if not isinstance(sub_items, list):
            continue
        batch_count += 1
        item_count += len(sub_items)
        completed_count += sum(
            1
            for item in sub_items
            if isinstance(item, dict) and str(item.get("res_img", "")).startswith("http")
        )

    return {
        "batch_count": batch_count,
        "item_count": item_count,
        "completed_count": completed_count,
    }


def summarize_json_like(data: Any) -> Any:
    if not isinstance(data, dict):
        return data

    summary: dict[str, Any] = {}
    for key in ("reqid", "code", "message", "error_type", "http_code"):
        value = data.get(key)
        if value not in (None, "", [], {}):
            summary[key] = value

    if "_raw" in data and "_raw" not in summary:
        summary["_raw"] = data["_raw"]

    body = data.get("body")
    if isinstance(body, dict):
        summary["body"] = summarize_json_like(body)

    data_obj = data.get("data")
    if isinstance(data_obj, dict):
        data_summary: dict[str, Any] = {}
        for key in ("msg_id", "task_id", "batch_id", "status"):
            value = data_obj.get(key)
            if value not in (None, "", [], {}):
                data_summary[key] = value

        media_info_list = data_obj.get("media_info_list")
        if isinstance(media_info_list, list):
            data_summary["media_info_count"] = len(media_info_list)

        media_urls = data_obj.get("media_urls")
        if isinstance(media_urls, list):
            data_summary["media_url_count"] = len(media_urls)

        items_summary = _count_render_items(data_obj.get("items"))
        if items_summary:
            data_summary["items_summary"] = items_summary

        if data_summary:
            summary["data"] = data_summary

    return redact_json_like(summary)


def summarize_json_text(
    text: str,
    *,
    ak: str = "",
    http_code: Optional[int] = None,
    max_len: int = 20000,
) -> Any:
    envelope = redact_json_text(text, ak=ak, http_code=http_code, max_len=max_len)
    return summarize_json_like(envelope)


def _cmd_detect_local_image(path: str) -> int:
    suffix, mime = detect_local_image(path)
    print(f"{suffix}\t{mime}")
    return 0


def _cmd_redact_json(max_len: int, http_code_raw: str, ak: str) -> int:
    http_code: Optional[int] = None
    if http_code_raw.strip():
        http_code = int(http_code_raw)
    text = sys.stdin.read()
    redacted = redact_json_text(text, ak=ak, http_code=http_code, max_len=max_len)
    print(json.dumps(redacted, ensure_ascii=False, indent=2))
    return 0


def _cmd_summarize_json(max_len: int, http_code_raw: str, ak: str) -> int:
    http_code: Optional[int] = None
    if http_code_raw.strip():
        http_code = int(http_code_raw)
    text = sys.stdin.read()
    summary = summarize_json_text(text, ak=ak, http_code=http_code, max_len=max_len)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenClaw shared safety helpers")
    subparsers = parser.add_subparsers(dest="command", required=True)

    detect_parser = subparsers.add_parser("detect-local-image")
    detect_parser.add_argument("path")

    redact_parser = subparsers.add_parser("redact-json")
    redact_parser.add_argument("--max-len", type=int, default=20000)
    redact_parser.add_argument("--http-code", default="")
    redact_parser.add_argument("--ak", default="")

    summarize_parser = subparsers.add_parser("summarize-json")
    summarize_parser.add_argument("--max-len", type=int, default=20000)
    summarize_parser.add_argument("--http-code", default="")
    summarize_parser.add_argument("--ak", default="")

    args = parser.parse_args()
    try:
        if args.command == "detect-local-image":
            return _cmd_detect_local_image(args.path)
        if args.command == "summarize-json":
            return _cmd_summarize_json(args.max_len, args.http_code, args.ak)
        return _cmd_redact_json(args.max_len, args.http_code, args.ak)
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
