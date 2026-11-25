"""Deterministic, secret-free manifest encoding utilities."""

from __future__ import annotations

import hashlib
import json
from typing import Any

MANIFEST_SCHEMA = "api-to-typemcp.manifest"
MANIFEST_VERSION = 1


def canonical_json(value: Any) -> bytes:
    """Encode contract values deterministically (sorted keys, compact UTF-8 JSON)."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def add_digest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Return a copy with its SHA-256 over every field except ``digest``."""
    value = dict(manifest)
    value.pop("digest", None)
    value["digest"] = "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()
    return value
