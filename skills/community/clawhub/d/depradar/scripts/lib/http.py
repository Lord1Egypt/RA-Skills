"""HTTP client with retry, timeout, and error handling for /depradar."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlencode


class HttpError(Exception):
    """Raised when an HTTP request fails after all retries."""

    def __init__(self, url: str, status: int, body: str) -> None:
        self.url = url
        self.status = status
        self.body = body
        super().__init__(f"HTTP {status} for {url}")


class RateLimitError(HttpError):
    """Raised specifically on HTTP 429 / 403 rate-limit responses."""


class NotFoundError(HttpError):
    """Raised on HTTP 404."""


# ── Public API ───────────────────────────────────────────────────────────────

def get_json(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 20,
    retries: int = 3,
    retry_delay: float = 1.5,
    accept: str = "application/json",
) -> Any:
    """Perform a GET request and return the parsed JSON body.

    Raises:
        RateLimitError  — on 429 / 403
        NotFoundError   — on 404
        HttpError       — on other non-2xx status codes
    """
    full_url = _build_url(url, params)
    hdrs = {"Accept": accept, "User-Agent": "depradar-skill/1.0 (github.com/depradar)"}
    if headers:
        hdrs.update(headers)

    last_exc: Optional[Exception] = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(full_url, headers=hdrs, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                return json.loads(raw)
        except urllib.error.HTTPError as exc:
            body = ""
            try:
                body = exc.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            if exc.code == 404:
                raise NotFoundError(full_url, exc.code, body)
            if exc.code in (429, 403):
                raise RateLimitError(full_url, exc.code, body)
            # Retry on 5xx
            if exc.code >= 500 and attempt < retries - 1:
                time.sleep(retry_delay * (attempt + 1))
                last_exc = HttpError(full_url, exc.code, body)
                continue
            raise HttpError(full_url, exc.code, body)
        except (urllib.error.URLError, OSError) as exc:
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(retry_delay * (attempt + 1))
                continue
            raise HttpError(full_url, 0, str(exc)) from exc

    raise HttpError(full_url, 0, str(last_exc))


def get_text(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 15,
    retries: int = 3,
    retry_delay: float = 1.5,
) -> str:
    """Perform a GET request and return the raw text body.

    Raises:
        RateLimitError  — on 429 / 403
        NotFoundError   — on 404
        HttpError       — on other non-2xx status codes
    """
    hdrs = {"User-Agent": "depradar-skill/1.0"}
    if headers:
        hdrs.update(headers)

    last_exc: Optional[Exception] = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=hdrs, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            body = ""
            try:
                body = exc.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            if exc.code == 404:
                raise NotFoundError(url, exc.code, body)
            if exc.code in (429, 403):
                raise RateLimitError(url, exc.code, body)
            # Retry on 5xx
            if exc.code >= 500 and attempt < retries - 1:
                time.sleep(retry_delay * (attempt + 1))
                last_exc = HttpError(url, exc.code, body)
                continue
            raise HttpError(url, exc.code, body)
        except (urllib.error.URLError, OSError) as exc:
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(retry_delay * (attempt + 1))
                continue
            raise HttpError(url, 0, str(exc)) from exc

    raise HttpError(url, 0, str(last_exc))


# ── Internal ─────────────────────────────────────────────────────────────────

def _build_url(base: str, params: Optional[Dict[str, Any]]) -> str:
    if not params:
        return base
    return f"{base}?{urlencode({k: v for k, v in params.items() if v is not None})}"
