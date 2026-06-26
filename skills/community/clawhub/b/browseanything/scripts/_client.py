"""Minimal stdlib HTTP client for the Browse Anything v1 API.

Zero pip dependencies on purpose so the skill installs anywhere `python3`
is available (Claude Code, OpenClaw, Codex, Cursor, Gemini, etc.).

Environment variables:
  BROWSEANYTHING_API_KEY   Required. ba_live_... key from the dashboard.
  BROWSEANYTHING_API_URL   Optional. Defaults to https://platform.browseanything.io
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_BASE_URL = "https://platform.browseanything.io"


class ApiError(RuntimeError):
    def __init__(self, status: int, body: Any):
        super().__init__(f"HTTP {status}: {body}")
        self.status = status
        self.body = body


def _api_key() -> str:
    key = os.environ.get("BROWSEANYTHING_API_KEY", "").strip()
    if not key:
        sys.stderr.write(
            "ERROR: BROWSEANYTHING_API_KEY is not set.\n"
            "Get a key from https://platform.browseanything.io (Settings > API Keys)\n"
            "and export it: export BROWSEANYTHING_API_KEY=ba_live_...\n"
        )
        sys.exit(2)
    return key


def _base_url() -> str:
    return os.environ.get("BROWSEANYTHING_API_URL", DEFAULT_BASE_URL).rstrip("/")


def request(
    method: str,
    path: str,
    body: dict | None = None,
    raw: bool = False,
    timeout: int = 60,
) -> Any:
    """Perform a single HTTP request against the API.

    Returns the parsed JSON body unless raw=True, in which case the raw
    bytes are returned (used for screenshots).
    """
    url = f"{_base_url()}{path}"
    data = None
    headers = {
        "Authorization": f"Bearer {_api_key()}",
        "Accept": "application/json",
        "User-Agent": "browse-anything-skill/1.0 (+https://browseanything.io)",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = resp.read()
            if raw:
                return payload, dict(resp.headers)
            if not payload:
                return {}
            return json.loads(payload.decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        try:
            parsed = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            parsed = {"raw": raw_body}
        raise ApiError(e.code, parsed) from None
    except urllib.error.URLError as e:
        sys.stderr.write(f"ERROR: cannot reach {url}: {e.reason}\n")
        sys.exit(3)


def print_json(obj: Any) -> None:
    json.dump(obj, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")
