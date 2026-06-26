"""Claw API HMAC-SHA256 signing utility.

Supports CLAW_PATH_PREFIX env var (e.g. "/v2") for proxied environments:
- Request URL: {CLAW_BASE_URL}{CLAW_PATH_PREFIX}/claw/templates
- Sign path:   /claw/templates  (what Java actually receives)
"""

import hashlib
import hmac
import os
import time
import uuid
from urllib.parse import urlparse

import requests

CLAW_PATH_PREFIX = os.getenv("CLAW_PATH_PREFIX", "")


def _parse_key_id(sk: str) -> str:
    parts = sk.split("-")
    if len(parts) < 4 or parts[0] != "sk" or parts[1] != "leewow":
        raise ValueError("Invalid SK format. Expected: sk-leewow-{keyId}-{secret}")
    return parts[2]


def _compute_body_hash(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def _compute_signature(sk: str, payload: str) -> str:
    return hmac.new(
        sk.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def _strip_prefix(path: str) -> str:
    """Strip CLAW_PATH_PREFIX from path for signing (Java receives path without prefix)."""
    if CLAW_PATH_PREFIX and path.startswith(CLAW_PATH_PREFIX):
        return path[len(CLAW_PATH_PREFIX):]
    return path


def build_claw_headers(sk: str, method: str, url: str, body: bytes = b"") -> dict:
    key_id = _parse_key_id(sk)
    timestamp = str(int(time.time()))
    nonce = uuid.uuid4().hex[:16]
    raw_path = urlparse(url).path
    sign_path = _strip_prefix(raw_path)
    body_hash = _compute_body_hash(body)
    sign_payload = f"{key_id}\n{timestamp}\n{nonce}\n{method}\n{sign_path}\n{body_hash}"
    signature = _compute_signature(sk, sign_payload)
    return {
        "X-Claw-KeyId": key_id,
        "X-Claw-Timestamp": timestamp,
        "X-Claw-Nonce": nonce,
        "X-Claw-Signature": signature,
    }


def sign_url(sk: str, url: str) -> str:
    """Append skid / ts / nonce / sig query parameters to a URL.

    The preview / purchase page reads these params, sends them to the backend
    which verifies the HMAC and exchanges them for a session JWT.
    Signing payload is identical to the header-based scheme (method=GET, empty body).
    """
    from urllib.parse import urlencode, urlparse, urlunparse, parse_qs, urljoin

    key_id = _parse_key_id(sk)
    timestamp = str(int(time.time()))
    nonce = uuid.uuid4().hex[:16]

    parsed = urlparse(url)
    sign_path = _strip_prefix(parsed.path)
    body_hash = _compute_body_hash(b"")
    sign_payload = f"{key_id}\n{timestamp}\n{nonce}\nGET\n{sign_path}\n{body_hash}"
    signature = _compute_signature(sk, sign_payload)

    sep = "&" if parsed.query else ""
    new_query = (
        f"{parsed.query}{sep}"
        f"skid={key_id}&ts={timestamp}&nonce={nonce}&sig={signature}"
    )
    return urlunparse(parsed._replace(query=new_query))


def claw_get(sk: str, url: str, **kwargs) -> requests.Response:
    headers = build_claw_headers(sk, "GET", url)
    headers.update(kwargs.pop("headers", {}))
    return requests.get(url, headers=headers, **kwargs)


def claw_post(sk: str, url: str, json_data: dict = None, **kwargs) -> requests.Response:
    import json as json_module
    body = json_module.dumps(json_data).encode("utf-8") if json_data else b""
    headers = build_claw_headers(sk, "POST", url, body)
    headers["Content-Type"] = "application/json"
    headers.update(kwargs.pop("headers", {}))
    return requests.post(url, data=body, headers=headers, **kwargs)
