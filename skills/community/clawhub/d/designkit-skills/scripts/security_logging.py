#!/usr/bin/env python3
"""Shared helpers for safe request logging."""

from __future__ import annotations

import json
import os
import pathlib
import re
import shlex
import urllib.parse
from typing import Any, Mapping, Optional


DEFAULT_REQUEST_LOG = "0"
REDACTED = "<redacted>"
SENSITIVE_HEADER_NAMES = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-openclaw-ak",
    "x-api-key",
    "api-key",
}
SENSITIVE_FIELD_NAMES = {
    "access_key",
    "ak",
    "api_key",
    "authorization",
    "key",
    "policy_signed_url",
    "secret",
    "secret_key",
    "token",
    "upload_url",
    "x_openclaw_ak",
}
SENSITIVE_KEY_PARTS = ("token", "secret", "authorization", "cookie")


def request_log_enabled(env: Optional[Mapping[str, str]] = None) -> bool:
    values = os.environ if env is None else env
    raw = str(values.get("OPENCLAW_REQUEST_LOG", DEFAULT_REQUEST_LOG)).strip().lower()
    return raw not in {"", "0", "false", "no", "off"}


def _normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")


def _is_sensitive_name(name: str) -> bool:
    normalized = _normalize_name(name)
    if normalized in SENSITIVE_FIELD_NAMES or normalized in SENSITIVE_HEADER_NAMES:
        return True
    if normalized.endswith("_key"):
        return True
    return any(part in normalized for part in SENSITIVE_KEY_PARTS)


def redact_header_value(name: str, value: str) -> str:
    return REDACTED if _is_sensitive_name(name) else value


def sanitize_url_for_log(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    query = "<redacted-query>" if parsed.query else ""
    fragment = ""
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, query, fragment))


def sanitize_text_for_log(text: str) -> str:
    sanitized = text
    sanitized = re.sub(r"(X-Openclaw-AK:\s*)([^\s'\"\\\\]+)", r"\1<redacted>", sanitized, flags=re.I)
    sanitized = re.sub(r'("?(?:token|key|authorization|ak|x-openclaw-ak)"?\s*[:=]\s*")([^"]+)(")', r"\1<redacted>\3", sanitized, flags=re.I)
    return sanitized


def sanitize_json_payload(value: Any, key_hint: Optional[str] = None) -> Any:
    if key_hint and _is_sensitive_name(key_hint):
        return REDACTED
    if isinstance(value, dict):
        return {key: sanitize_json_payload(item, str(key)) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_json_payload(item, key_hint) for item in value]
    if isinstance(value, str):
        if key_hint and _normalize_name(key_hint) in {"upload_url", "policy_signed_url"}:
            return sanitize_url_for_log(value)
        return sanitize_text_for_log(value)
    return value


def sanitize_request_body(body: Any) -> Optional[str]:
    if body in (None, b"", ""):
        return None
    if isinstance(body, bytes):
        text = body.decode("utf-8", errors="replace")
    else:
        text = str(body)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return sanitize_text_for_log(text)
    return json.dumps(sanitize_json_payload(parsed), ensure_ascii=False)


def format_curl_command(
    method: str,
    url: str,
    headers: Mapping[str, str],
    body: Any = None,
    *,
    max_time: Optional[int] = None,
    include_http_code: bool = False,
) -> str:
    parts = ["curl", "-s"]
    if include_http_code:
        parts.extend(["-w", "\n%{http_code}"])
    upper_method = method.upper()
    if upper_method not in {"GET", "HEAD"}:
        parts.extend(["-X", upper_method])
    for key, value in headers.items():
        parts.extend(["-H", f"{key}: {redact_header_value(key, value)}"])
    redacted_body = sanitize_request_body(body)
    if redacted_body:
        parts.extend(["-d", redacted_body])
    if max_time is not None:
        parts.extend(["--max-time", str(max_time)])
    parts.append(sanitize_url_for_log(url))
    return shlex.join(parts)


def format_multipart_curl(
    upload_url: str,
    *,
    file_path: str,
    mime: str,
    form_fields: Optional[Mapping[str, str]] = None,
    headers: Optional[Mapping[str, str]] = None,
    max_time: Optional[int] = None,
) -> str:
    parts = ["curl", "-s"]
    if max_time is not None:
        parts.extend(["--max-time", str(max_time)])
    parts.extend(["-X", "POST"])
    for key, value in (headers or {}).items():
        parts.extend(["-H", f"{key}: {redact_header_value(key, value)}"])
    for key, value in (form_fields or {}).items():
        rendered_value = REDACTED if _is_sensitive_name(key) else value
        parts.extend(["-F", f"{key}={rendered_value}"])
    file_name = pathlib.Path(file_path).name or "local-file"
    parts.extend(["-F", f"file=@{file_name};type={mime}"])
    parts.append(sanitize_url_for_log(upload_url))
    return shlex.join(parts)


def format_json_log(
    label: str,
    text: str,
    *,
    max_len: int = 20000,
    http_code: Optional[Any] = None,
) -> str:
    display_text = text
    truncated = False
    if len(display_text) > max_len:
        display_text = display_text[:max_len]
        truncated = True
    try:
        payload: Any = json.loads(text)
        payload = sanitize_json_payload(payload)
        if http_code not in (None, ""):
            envelope: Any = {"http_code": int(http_code), "body": payload}
        else:
            envelope = payload
    except (json.JSONDecodeError, ValueError, TypeError):
        raw_body = sanitize_text_for_log(display_text)
        if truncated:
            raw_body += "...(truncated)"
        if http_code not in (None, ""):
            try:
                http_code_value: Any = int(http_code)
            except (TypeError, ValueError):
                http_code_value = http_code
            envelope = {"http_code": http_code_value, "_raw": raw_body}
        else:
            envelope = {"_raw": raw_body}

    pretty = json.dumps(envelope, ensure_ascii=False, indent=2)
    if truncated and "_raw" not in pretty:
        pretty += "\n...(truncated)"
    return f"[REQUEST] {label} (JSON):\n{pretty}"
