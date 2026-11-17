"""Encode a Python object as JSON safe to embed inside a ``<script>`` tag.

Escapes characters HTML5 disallows inside script content (``<``, ``&``, ``>``)
plus the line/paragraph separators that break JavaScript string parsing.
"""

from __future__ import annotations

import json
from typing import Any


def safe_json_for_script(payload: Any) -> str:
    return (
        json.dumps(payload, ensure_ascii=False)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace(" ", "\\u2028")
        .replace(" ", "\\u2029")
    )
