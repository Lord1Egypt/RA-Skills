"""Sanitization for API-sourced strings before rendering or shell use."""

from __future__ import annotations

import re

# Strips:
#  - control characters (NUL through 0x1f, plus DEL)
#  - markdown image syntax: ![alt](url) — including nested parens
#  - markdown links with `javascript:` URIs
_UNSAFE_PATTERN = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]"
    r"|!\[[^\]]*\]\((?:[^()]*|\([^()]*\))*\)"
    r"|\[[^\]]*\]\(javascript:(?:[^()]*|\([^()]*\))*\)"
)


def sanitize(value: str, max_len: int = 500) -> str:
    """Strip control characters and markdown injection patterns from API data."""
    if value is None:
        return ""
    cleaned = _UNSAFE_PATTERN.sub("", str(value))
    return cleaned[:max_len]
