#!/usr/bin/env python3
"""Small dependency-free Dataify HTTP client for standalone workflow skills."""

from __future__ import annotations

import json
import os
import re
import random
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request
from urllib.parse import urlsplit


SERP_ENDPOINT = "https://scraperapi.dataify.com/request"
UNLOCKER_ENDPOINT = "https://webunlocker.dataify.com/request"
TOKEN_MESSAGE = (
    "DATAIFY_API_TOKEN is not configured. Sign in at "
    "https://dashboard.dataify.com/login?utm_source=skill. "
    "New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed."
)


def token_from_environment(environ: dict[str, str] | None = None) -> str:
    token = (environ or os.environ).get("DATAIFY_API_TOKEN", "").strip()
    if not token:
        raise RuntimeError(TOKEN_MESSAGE)
    return token.removeprefix("Bearer ").strip()


def normalize_url(value: str) -> str:
    value = value.strip()
    parts = urlsplit(value)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise ValueError("A public HTTP(S) URL is required")
    if parts.username or parts.password or not re.fullmatch(r"[A-Za-z0-9.-]+(?::\d+)?", parts.netloc):
        raise ValueError("URL credentials or invalid host names are not allowed")
    return value


def retry_delay(attempt: int, retry_after: str | None = None) -> float:
    if retry_after:
        try:
            return min(30.0, max(0.0, float(retry_after)))
        except ValueError:
            pass
    return min(8.0, 0.5 * (2 ** max(0, attempt - 1))) + random.uniform(0, 0.25)


def _post(url: str, token: str, data: bytes, content_type: str, timeout: float, max_attempts: int = 3) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Authorization": "Bearer {}".format(token), "Content-Type": content_type},
        method="POST",
    )
    for attempt in range(1, max_attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8", errors="replace")
                payload = parse_json(body)
                if isinstance(payload, dict) and (payload.get('error') or payload.get('success') is False or isinstance(payload.get('code'), int) and payload['code'] >= 400):
                    return {'ok':False, 'status':int(getattr(response, 'status', 200)), 'body':body, 'error':{'category':'application_error', 'message':'API returned a business error'}, 'attempts':attempt}
                return {"ok": True, "status": int(getattr(response, "status", 200)), "body": body, "error": None, "attempts": attempt}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            category = "invalid_credentials" if exc.code in {401, 403} else "insufficient_balance" if exc.code == 402 else "rate_limited" if exc.code == 429 else "http_error"
            if exc.code not in {429, 500, 502, 503, 504} or attempt == max_attempts:
                return {"ok": False, "status": exc.code, "body": "", "error": {"category": category, "message": detail or "HTTP {}".format(exc.code)}, "attempts": attempt}
            time.sleep(retry_delay(attempt, exc.headers.get("Retry-After")))
        except urllib.error.URLError as exc:
            if attempt == max_attempts:
                return {"ok": False, "status": None, "body": "", "error": {"category": "network", "message": str(exc.reason)}, "attempts": attempt}
            time.sleep(retry_delay(attempt))
        except TimeoutError:
            if attempt == max_attempts:
                return {"ok": False, "status": None, "body": "", "error": {"category": "timeout", "message": "Request timed out"}, "attempts": attempt}
            time.sleep(retry_delay(attempt))


def search(query: str, token: str, geography: str = "us", timeout: float = 120) -> dict[str, Any]:
    params = {"engine": "google", "q": query, "json": "1"}
    if re.fullmatch(r"[A-Za-z]{2}", geography.strip()):
        params["gl"] = geography.lower()
    return _post(SERP_ENDPOINT, token, urllib.parse.urlencode(params).encode("utf-8"), "application/x-www-form-urlencoded", timeout)


def unlock(url: str, token: str, geography: str = "us", clean_content: bool = True, timeout: float = 120) -> dict[str, Any]:
    payload = {
        "url": normalize_url(url), "type": "html", "js_render": "True",
        "clean_content": "true" if clean_content else "false",
        "country": geography.lower(), "follow_redirect": "True", "isjson": "1",
    }
    return _post(UNLOCKER_ENDPOINT, token, json.dumps(payload).encode("utf-8"), "application/json", timeout)


def parse_json(text: str) -> Any:
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None


def content_from_response(text: str) -> str:
    payload = parse_json(text)
    if payload is None:
        return text
    candidates = ("content", "html", "body", "result", "data")
    current: Any = payload
    for _ in range(4):
        if isinstance(current, str):
            return current
        if isinstance(current, dict):
            next_value = next((current[key] for key in candidates if key in current), None)
            if next_value is None:
                break
            current = next_value
        else:
            break
    return json.dumps(payload, ensure_ascii=False)


def urls_from_search(text: str) -> list[str]:
    payload = parse_json(text)
    found: list[str] = []

    # Dataify SERP responses expose ranked natural results under `organic`.
    # Prefer that collection so metadata URLs (AI loader, pagination and
    # redirects) cannot consume a research workflow's fetch budget.
    if isinstance(payload, dict) and isinstance(payload.get("organic"), list):
        for item in payload["organic"]:
            if not isinstance(item, dict) or not isinstance(item.get("link"), str):
                continue
            try:
                normalized = normalize_url(item["link"])
            except ValueError:
                continue
            if normalized not in found:
                found.append(normalized)
        return found

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key.lower() in {"link", "url", "href"} and isinstance(item, str):
                    try:
                        normalized = normalize_url(item)
                    except ValueError:
                        pass
                    else:
                        if normalized not in found:
                            found.append(normalized)
                else:
                    visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(payload)
    return found
