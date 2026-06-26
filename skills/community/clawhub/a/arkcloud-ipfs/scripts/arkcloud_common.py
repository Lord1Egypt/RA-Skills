#!/usr/bin/env python3
"""Shared helpers for the ARKCloud IPFS skill scripts."""

from __future__ import annotations

import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://file.arklink.hk"
DEFAULT_HEADERS = {
    "User-Agent": "ARKCloud-IPFS-Skill/0.1.6 (+https://github.com/djanngau/arkcloud-ipfs-skill)",
    "Accept": "application/json",
}


def base_url(value: str | None = None) -> str:
    return (value or os.environ.get("ARKCLOUD_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def fail(message: str, *, code: int = 1, **extra: Any) -> None:
    payload = {"ok": False, "error": message}
    payload.update(extra)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    body: bytes | None = None,
    timeout: int = 120,
) -> dict[str, Any] | list[Any]:
    request_headers = {**DEFAULT_HEADERS, **(headers or {})}
    req = Request(url, data=body, method=method.upper(), headers=request_headers)
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            if not raw:
                return {}
            return json.loads(raw.decode("utf-8"))
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(raw)
        except json.JSONDecodeError:
            detail = raw
        fail(
            f"ARKCloud API returned HTTP {exc.code}",
            status=exc.code,
            detail=detail,
        )
    except URLError as exc:
        fail(f"Could not reach ARKCloud API: {exc.reason}")
    except TimeoutError:
        fail("Timed out while contacting ARKCloud API")
    except json.JSONDecodeError as exc:
        fail(f"ARKCloud API returned invalid JSON: {exc}")


def require_env(name: str, message: str | None = None) -> str:
    value = os.environ.get(name)
    if not value:
        fail(message or f"Missing {name}")
    return value


def endpoint(root: str, path: str) -> str:
    return urljoin(root.rstrip("/") + "/", path.lstrip("/"))


def print_json(payload: Any) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
