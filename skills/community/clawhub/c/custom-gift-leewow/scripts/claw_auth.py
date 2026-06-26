"""Claw API HMAC-SHA256 signing utility.

Supports CLAW_PATH_PREFIX env var (e.g. "/v2") for proxied environments:
- Request URL: {CLAW_BASE_URL}{CLAW_PATH_PREFIX}/claw/templates
- Sign path:   /claw/templates  (what Java actually receives)

Preview page token exchange (browser → GET /claw/preview/auth) matches
ClawPreviewAuthController: only query params skid + sig, with
sig = hex(HMAC-SHA256(key=full_sk, message="claw-preview:" + skid)).

Claw API calls use X-Claw-* headers; payload format is defined in ClawSkAuthFilter.
"""

import hashlib
import hmac
import os
import time
import uuid
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

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
        return path[len(CLAW_PATH_PREFIX) :]
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


def build_preview_auth_params(sk: str) -> dict:
    """skid + sig for GET /claw/preview/auth — matches ClawPreviewAuthController.exchangeToken."""
    key_id = _parse_key_id(sk)
    message = f"claw-preview:{key_id}"
    sig = hmac.new(
        sk.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return {"skid": key_id, "sig": sig}


def sign_url(sk: str, url: str) -> str:
    """Append skid & sig query params for preview / purchase links.

    Java verifies with:
      expectedSig = hmacSha256(fullSk, \"claw-preview:\" + skid)  // hex, lowercase

    Do not use X-Claw header signing (ts/nonce/path) here — preview auth only accepts skid+sig.
    """
    auth = build_preview_auth_params(sk)
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["skid"] = auth["skid"]
    query["sig"] = auth["sig"]
    new_query = urlencode(query)
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
