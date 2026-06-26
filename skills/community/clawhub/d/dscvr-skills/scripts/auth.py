# /// script
# requires-python = ">=3.10"
# ///
"""HMAC-SHA256 authentication for DSCVR Subscription API.

Generates the three required headers for every authenticated API call:
  - X-API-Key:   the public API key
  - X-Timestamp: current Unix timestamp (seconds)
  - X-Signature: HMAC-SHA256(secret_key, "{api_key}:{timestamp}") hex digest

Usage as a library:
    from auth import generate_auth_headers
    headers = generate_auth_headers(api_key, secret_key)
"""

from __future__ import annotations

import hashlib
import hmac
import time


def compute_signature(secret_key: str, api_key: str, timestamp: str) -> str:
    """Compute HMAC-SHA256 signature for request authentication.

    Args:
        secret_key: The 32-character secret key.
        api_key: The 16-character public API key.
        timestamp: Unix timestamp as a string.

    Returns:
        Hex-encoded HMAC-SHA256 digest.
    """
    message = f"{api_key}:{timestamp}".encode()
    return hmac.new(secret_key.encode(), message, hashlib.sha256).hexdigest()


def generate_auth_headers(api_key: str, secret_key: str) -> dict[str, str]:
    """Generate the full set of authentication headers.

    Args:
        api_key: The 16-character public API key.
        secret_key: The 32-character secret key.

    Returns:
        Dictionary with X-API-Key, X-Timestamp, and X-Signature headers.
    """
    timestamp = str(int(time.time()))
    signature = compute_signature(secret_key, api_key, timestamp)
    return {
        "X-API-Key": api_key,
        "X-Timestamp": timestamp,
        "X-Signature": signature,
    }



