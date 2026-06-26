#!/usr/bin/env python3
"""Shared helpers for Bitrix24 skill scripts."""

from __future__ import annotations

import json
import os
import re
import stat
from pathlib import Path

WEBHOOK_RE = re.compile(r"^https://(?P<host>[^/]+)/rest/(?P<user_id>\d+)/(?P<secret>[^/]+)/?$")
DEFAULT_CACHE_PATH = Path.home() / ".config" / "bitrix24-skill" / "cache_user_timezone.json"


def normalize_url(value: str) -> str:
    return value.strip().strip('"').strip("'").rstrip("/") + "/"


def validate_url(value: str) -> str:
    normalized = normalize_url(value)
    if not WEBHOOK_RE.match(normalized):
        raise ValueError("Webhook format is invalid. Expected https://<host>/rest/<user_id>/<secret>/")
    return normalized


def mask_url(value: str) -> str:
    match = WEBHOOK_RE.match(value)
    if not match:
        return value
    secret = match.group("secret")
    if len(secret) <= 4:
        masked = "*" * len(secret)
    else:
        masked = f"{secret[:2]}***{secret[-2:]}"
    return f"https://{match.group('host')}/rest/{match.group('user_id')}/{masked}/"


def load_url() -> tuple[str | None, str]:
    """Load webhook URL from BITRIX24_WEBHOOK_URL env var."""
    url = os.environ.get("BITRIX24_WEBHOOK_URL")
    if url and url.strip():
        return url.strip(), "env:BITRIX24_WEBHOOK_URL"
    return None, "missing"


def _read_cache(path: Path = DEFAULT_CACHE_PATH) -> dict:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _write_cache(data: dict, path: Path = DEFAULT_CACHE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    try:
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def get_cached_user() -> dict | None:
    """Return cached user data (user_id, timezone) or None."""
    data = _read_cache()
    user_id = data.get("user_id")
    if user_id is not None:
        return {"user_id": user_id, "timezone": data.get("timezone", "")}
    return None


def cache_user_data(user_id: int, timezone: str = "") -> None:
    """Save user_id and timezone to cache for reuse."""
    data = _read_cache()
    data["user_id"] = user_id
    if timezone:
        data["timezone"] = timezone
    _write_cache(data)
