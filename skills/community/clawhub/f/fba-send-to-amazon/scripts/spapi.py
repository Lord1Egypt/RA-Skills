#!/usr/bin/env python3
"""Minimal SP-API client: LWA token exchange + retrying JSON requests.

Zero third-party dependencies — stdlib only. If you already have a SP-API
client (python-amazon-sp-api, etc.), replace this module; the rest of the
scripts only need `access_token()`, `ENDPOINT` and `MARKETPLACE`.

Credentials are read, in order of precedence:

  1. Environment variables
         LWA_CLIENT_ID, LWA_CLIENT_SECRET, SPAPI_REFRESH_TOKEN
         SPAPI_ENDPOINT        (default https://sellingpartnerapi-na.amazon.com)
         SPAPI_MARKETPLACE_ID  (default ATVPDKIKX0DER, Amazon US)
  2. A JSON file at ~/.config/sp-api/credentials.json with the same keys
     (lowercased), e.g.
         {"lwa_client_id": "...", "lwa_client_secret": "...",
          "refresh_token": "...", "marketplace_id": "ATVPDKIKX0DER"}

Never commit credentials. This file reads them, it does not store them.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CONFIG_FILE = Path.home() / ".config" / "sp-api" / "credentials.json"
LWA_URL = "https://api.amazon.com/auth/o2/token"

_cfg_cache: dict | None = None
_token: tuple[str, float] | None = None   # (access_token, expires_at_epoch)


def _config() -> dict:
    global _cfg_cache
    if _cfg_cache is None:
        _cfg_cache = {}
        if CONFIG_FILE.exists():
            try:
                _cfg_cache = json.loads(CONFIG_FILE.read_text())
            except Exception as e:                       # noqa: BLE001
                raise RuntimeError(f"cannot parse {CONFIG_FILE}: {e}") from None
    return _cfg_cache


def _setting(env_key: str, file_key: str, default: str | None = None) -> str:
    val = os.environ.get(env_key) or _config().get(file_key) or default
    if not val:
        raise RuntimeError(
            f"missing SP-API setting: set ${env_key} or '{file_key}' in {CONFIG_FILE}")
    return val


ENDPOINT = os.environ.get("SPAPI_ENDPOINT") or _config().get(
    "endpoint", "https://sellingpartnerapi-na.amazon.com")
MARKETPLACE = os.environ.get("SPAPI_MARKETPLACE_ID") or _config().get(
    "marketplace_id", "ATVPDKIKX0DER")


def access_token() -> str:
    """Return a cached LWA access token, refreshing ~1 min before expiry."""
    global _token
    if _token and time.time() < _token[1]:
        return _token[0]

    body = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": _setting("SPAPI_REFRESH_TOKEN", "refresh_token"),
        "client_id": _setting("LWA_CLIENT_ID", "lwa_client_id"),
        "client_secret": _setting("LWA_CLIENT_SECRET", "lwa_client_secret"),
    }).encode()

    req = urllib.request.Request(
        LWA_URL, data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"LWA token exchange failed: {e.read().decode()[:300]}") from None

    _token = (data["access_token"], time.time() + int(data.get("expires_in", 3600)) - 60)
    return _token[0]


def headers() -> dict:
    return {"x-amz-access-token": access_token(), "Content-Type": "application/json"}


def request(method: str, url: str, body=None, params=None, retries: int = 6):
    """JSON request with retry on transient failures.

    ALWAYS surfaces the HTTP response body on error. SP-API puts the real
    reason there; the status line alone ("HTTP Error 403:") is useless and is
    what makes people misdiagnose parameter errors as permission errors.
    """
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None

    last: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers=headers(), method=method)
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            text = e.read().decode()
            if e.code in (429, 500, 502, 503, 504):          # transient
                last = RuntimeError(f"{method} {url} HTTP {e.code}: {text}")
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"{method} {url} HTTP {e.code}: {text}") from None
        except (urllib.error.URLError, OSError) as e:        # SSL / socket drop
            last = RuntimeError(f"{method} {url} network error: {e}")
            time.sleep(2 ** attempt)
    raise last or RuntimeError(f"{method} {url} failed")


if __name__ == "__main__":
    print(f"endpoint    {ENDPOINT}")
    print(f"marketplace {MARKETPLACE}")
    print(f"token       {access_token()[:12]}… ok")
