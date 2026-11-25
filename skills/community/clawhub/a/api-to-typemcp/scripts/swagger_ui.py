"""Bounded Swagger UI configuration discovery.

This module examines only user-supplied Swagger UI HTML in memory. It never
fetches a page, follows links, or enumerates an origin.
"""
from __future__ import annotations

import re
from typing import Any

MAX_SWAGGER_UI_BYTES = 2 * 1024 * 1024
MAX_CONFIG_BYTES = 65_536
MAX_BUNDLE_ATTEMPTS = 32


class SwaggerUIError(ValueError):
    """User-safe error for invalid or oversized Swagger UI input."""


_URL_RE = re.compile(r"(?:^|[,\n])\s*url\s*:\s*(['\"])(?P<url>[^'\"\s<>]{1,2048})\1")


def extract_spec_reference(html: str) -> dict[str, Any] | None:
    """Return one explicit spec reference from supplied Swagger UI HTML.

    Scanning is deterministic and attempt-capped: each candidate checks at
    most ``MAX_CONFIG_BYTES`` bytes, and no regular expression scans the full
    document once per potential bundle prefix. No I/O is performed.
    """
    if not isinstance(html, str):
        raise SwaggerUIError("Swagger UI input must be text")
    if len(html.encode("utf-8")) > MAX_SWAGGER_UI_BYTES:
        raise SwaggerUIError(f"Swagger UI input exceeds {MAX_SWAGGER_UI_BYTES} byte limit")

    marker = "SwaggerUIBundle"
    cursor = 0
    for _ in range(MAX_BUNDLE_ATTEMPTS):
        start = html.find(marker, cursor)
        if start < 0:
            return None
        open_paren = html.find("(", start + len(marker), start + len(marker) + 128)
        if open_paren < 0:
            cursor = start + len(marker)
            continue
        open_brace = html.find("{", open_paren + 1, open_paren + 256)
        if open_brace < 0:
            cursor = start + len(marker)
            continue
        close_brace = html.find("}", open_brace + 1, open_brace + 1 + MAX_CONFIG_BYTES)
        if close_brace < 0:
            cursor = start + len(marker)
            continue
        config = html[open_brace + 1:close_brace]
        url = _URL_RE.search(config)
        if url:
            return {"source_kind": "swagger-ui-config", "spec_url": url.group("url")}
        cursor = close_brace + 1
    return None
