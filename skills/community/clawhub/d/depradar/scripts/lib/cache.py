"""6-hour TTL JSON cache for /depradar.

Cache keys are SHA-256 hashes of the request parameters.
Storage: ~/.cache/depradar/{key}.json
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Optional, Tuple


_CACHE_DIR_ENV = "APIWATCH_CACHE_DIR"
_DEFAULT_CACHE_DIR = Path.home() / ".cache" / "depradar"

REGISTRY_TTL_HOURS   = 6    # GitHub releases, npm, PyPI
COMMUNITY_TTL_HOURS  = 24   # Reddit, HN, Stack Overflow
SCAN_TTL_HOURS       = 1    # Usage scan (short — changes with code edits)
REPORT_TTL_HOURS     = 6    # Full report cache


def cache_key(*parts: Any) -> str:
    """Build a 32-char hex cache key from the given parts (128-bit — negligible collision risk)."""
    raw = "|".join(str(p) for p in parts)
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def project_cache_key(project_path: str, *parts: Any) -> str:
    """Build a cache key that includes the project path.

    Use this for scan and report caches that are project-specific (codebase scan
    results differ per project even for the same packages). Registry caches are
    project-agnostic — use cache_key() for those.
    """
    project_hash = hashlib.sha256(
        str(Path(project_path).resolve()).encode()
    ).hexdigest()[:16]
    raw = "|".join([project_hash] + [str(p) for p in parts])
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def save(key: str, data: Any, namespace: str = "report") -> None:
    """Serialise *data* to disk under *key*."""
    path = _path(key, namespace)
    path.parent.mkdir(parents=True, exist_ok=True)
    envelope = {"saved_at": time.time(), "data": data}
    path.write_text(json.dumps(envelope, ensure_ascii=False), encoding="utf-8")


def load(key: str, ttl_hours: float = REPORT_TTL_HOURS,
         namespace: str = "report") -> Optional[Any]:
    """Return cached data if it exists and is younger than *ttl_hours*.

    Returns ``None`` on cache miss or expiry.
    """
    path = _path(key, namespace)
    if not path.is_file():
        return None
    try:
        envelope = json.loads(path.read_text(encoding="utf-8"))
        age_hours = (time.time() - envelope["saved_at"]) / 3600
        if age_hours > ttl_hours:
            return None
        return envelope["data"]
    except (OSError, KeyError, json.JSONDecodeError):
        return None


def load_with_age(
    key: str, ttl_hours: float = REPORT_TTL_HOURS, namespace: str = "report"
) -> Tuple[Optional[Any], Optional[float]]:
    """Like :func:`load` but also returns the age in hours.

    Returns ``(None, None)`` on miss/expiry.
    """
    path = _path(key, namespace)
    if not path.is_file():
        return None, None
    try:
        envelope = json.loads(path.read_text(encoding="utf-8"))
        age_hours = (time.time() - envelope["saved_at"]) / 3600
        if age_hours > ttl_hours:
            return None, None
        return envelope["data"], age_hours
    except (OSError, KeyError, json.JSONDecodeError):
        return None, None


def clear(namespace: str = "report") -> int:
    """Delete all cached files in *namespace*. Returns count deleted."""
    directory = _cache_dir() / namespace
    if not directory.is_dir():
        return 0
    count = 0
    for f in directory.glob("*.json"):
        try:
            f.unlink()
            count += 1
        except OSError:
            pass
    return count


def _cache_dir() -> Path:
    custom = os.environ.get(_CACHE_DIR_ENV)
    if custom:
        return Path(custom)
    try:
        _DEFAULT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        return _DEFAULT_CACHE_DIR
    except OSError:
        fallback = Path("/tmp/depradar/cache")
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


def _path(key: str, namespace: str) -> Path:
    return _cache_dir() / namespace / f"{key}.json"
