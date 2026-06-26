#!/usr/bin/env python3
"""Shared helpers for local TOTP handling."""

from __future__ import annotations

import base64
import hashlib
import hmac
import struct
import time


KEYCHAIN_SERVICE = "openclaw.auto-authenticator"


def normalize_seed(seed: str) -> str:
    compact = "".join(seed.strip().split()).upper()
    if not compact:
        raise ValueError("Seed must not be empty.")
    padding = "=" * ((8 - len(compact) % 8) % 8)
    try:
        base64.b32decode(compact + padding, casefold=True)
    except Exception as exc:  # pragma: no cover - exact exception type is not useful here
        raise ValueError("Seed must be valid Base32.") from exc
    return compact


def generate_totp(seed: str, digits: int = 6, period: int = 30, for_time: int | None = None) -> tuple[str, int]:
    if for_time is None:
        for_time = int(time.time())
    counter = int(for_time // period)
    padding = "=" * ((8 - len(seed) % 8) % 8)
    key = base64.b32decode(seed + padding, casefold=True)
    msg = struct.pack(">Q", counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code_int = struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
    code = str(code_int % (10**digits)).zfill(digits)
    expires_in = period - (for_time % period)
    return code, expires_in
