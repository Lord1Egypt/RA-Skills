"""Invitation and bind-code helpers for negotiate_safe."""
from __future__ import annotations

import os
import re


BIND_CODE_RE = re.compile(r"(INV-[A-Z0-9]+)", re.IGNORECASE)


def build_invite_url(session_code: str, base_url: str | None = None) -> str:
    """Generate a one-click invite URL, or empty when provisioning is absent."""
    code = (session_code or "").strip()
    if not code:
        return ""
    base = (base_url if base_url is not None else os.environ.get("PROVISION_BASE_URL") or "").strip()
    if not base:
        return ""
    return f"{base.rstrip('/')}/join/{code}"


def extract_bind_code(message: str) -> str | None:
    """Pull the INV-XXXXX code out of a `/bind ...` message body."""
    if not message:
        return None
    match = BIND_CODE_RE.search(message)
    if not match:
        return None
    return match.group(1).upper()
