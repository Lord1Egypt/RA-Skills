"""
client.py - HTTP request wrapper module

Responsibilities:
  - Wrap GET / POST requests
  - Auto inject auth_token header
  - Auto refresh and retry once when token expires
"""

import sys

import requests as _requests

from common.auth import get_token, refresh_token
from common.config import config


def _build_headers(token: str) -> dict:
    """Build common headers with auth_token"""
    return {
        "Content-Type": "application/json",
        "auth_token": token,
    }


def _is_auth_failure(resp: _requests.Response) -> bool:
    """
    Check if response is authentication failure.
    - HTTP 401
    - Or response JSON has success=false and contains token-related error
    """
    if resp.status_code == 401:
        return True
    try:
        data = resp.json()
        if not data.get("success"):
            msg = str(data.get("message", "")).lower()
            if "token" in msg or "auth" in msg or "login" in msg or "unauthorized" in msg:
                return True
    except Exception:
        pass
    return False


def get(path: str, params: dict | None = None) -> dict:
    """
    Send GET request.

    Args:
        path: Relative path, e.g., /drapi/ai/instanceMessage
        params: Query parameters dict
    Returns:
        Parsed JSON response dict
    """
    url = f"{config.base_url}{path}"
    token = get_token()
    resp = _requests.get(url, params=params, headers=_build_headers(token), verify=False, timeout=30)

    # Refresh and retry once when token expires
    if _is_auth_failure(resp):
        print("Token expired. Re-authentication required...", file=sys.stderr)
        token = refresh_token()
        resp = _requests.get(url, params=params, headers=_build_headers(token), verify=False, timeout=30)

    resp.raise_for_status()
    return resp.json()


def post(path: str, params: dict | None = None, json_body: dict | None = None) -> dict:
    """
    Send POST request.

    Args:
        path: Relative path, e.g., /drapi/sqlAudit/submit
        params: URL query parameters dict
        json_body: Request body dict
    Returns:
        Parsed JSON response dict
    """
    url = f"{config.base_url}{path}"
    token = get_token()
    resp = _requests.post(url, params=params, json=json_body, headers=_build_headers(token), verify=False, timeout=30)

    # Refresh and retry once when token expires
    if _is_auth_failure(resp):
        print("Token expired. Re-authentication required...", file=sys.stderr)
        token = refresh_token()
        resp = _requests.post(url, params=params, json=json_body, headers=_build_headers(token), verify=False, timeout=30)

    resp.raise_for_status()
    return resp.json()
