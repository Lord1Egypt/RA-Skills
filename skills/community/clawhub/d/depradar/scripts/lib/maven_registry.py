"""Maven Central REST API backend for /depradar.

No auth required. API: https://search.maven.org/solrsearch/select
Supports artifact IDs in 'groupId:artifactId' or plain 'artifactId' format.
"""
from __future__ import annotations

# ── http import bootstrap ─────────────────────────────────────────────────────
# lib/http.py shadows Python's stdlib 'http' package.  urllib.request does
# 'import http.client' internally; when lib/ is on sys.path[0] that fails.
# Fix: temporarily remove any lib/ entry from sys.path, load urllib (which
# caches it in sys.modules), restore the path, then load local http.py
# by absolute file path so it never goes through the 'http' name lookup.
import importlib.util as _ilu
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_lib_dir = str(Path(__file__).parent)
_lib_dir_resolved = str(Path(__file__).parent.resolve())


def _same_path(a: str, b_resolved: str) -> bool:
    try:
        return str(Path(a).resolve()) == b_resolved
    except Exception:
        return a == b_resolved or a == ""


# Pop lib dir from path (covers '' CWD==lib, forward-slash, and backslash variants)
_popped: list = []
while sys.path and (sys.path[0] == "" or _same_path(sys.path[0], _lib_dir_resolved)):
    _popped.append(sys.path.pop(0))

import urllib.error    # noqa: F401 — loaded cleanly without lib/ shadowing
import urllib.request  # noqa: F401 — loads http.client from stdlib

for _p in reversed(_popped):  # restore in original order
    sys.path.insert(0, _p)

# Now lib/ is back and urllib is cached — load our local http.py by file path.
# Share the instance via sys.modules so all modules use the same exception classes.
if "_depradar_http" not in sys.modules:
    _http_spec = _ilu.spec_from_file_location(
        "_depradar_http", str(Path(__file__).parent / "http.py")
    )
    _http_mod = _ilu.module_from_spec(_http_spec)   # type: ignore[arg-type]
    sys.modules["_depradar_http"] = _http_mod
    _http_spec.loader.exec_module(_http_mod)         # type: ignore[union-attr]
_http_mod = sys.modules["_depradar_http"]
get_json      = _http_mod.get_json
NotFoundError = _http_mod.NotFoundError
HttpError     = _http_mod.HttpError

sys.path.insert(0, _lib_dir)

from schema import PackageUpdate
from semver import bump_type, latest_stable
from dates import today_utc

try:
    import cache as _cache
    _CACHE_AVAILABLE = True
except ImportError:
    _CACHE_AVAILABLE = False


# ── Constants ─────────────────────────────────────────────────────────────────

MAVEN_SEARCH_API = "https://search.maven.org/solrsearch/select"
_CACHE_NS        = "maven_registry"
_CACHE_TTL       = 6.0   # hours
_ROWS            = 50    # docs per page (was 20 — too low for active artifacts)
_MAX_TOTAL_ROWS  = 200   # absolute cap to avoid excessive pagination


# ── Public API ────────────────────────────────────────────────────────────────

def fetch_package_info(artifact_id: str) -> Optional[Dict[str, Any]]:
    """Query Maven Central for the first page of versions of *artifact_id*.

    Accepts formats:
    - "com.google.guava:guava"   (fully qualified)
    - "guava"                     (artifactId only — best effort search)

    Returns the raw Solr response dict for the first page, or None on error.
    Use get_all_versions() for paginated retrieval.
    Cached for 6 hours.
    """
    cache_key = _make_cache_key("info", artifact_id)

    if _CACHE_AVAILABLE:
        cached = _cache.load(cache_key, ttl_hours=_CACHE_TTL, namespace=_CACHE_NS)
        if cached is not None:
            return cached

    group_id, artifact = _parse_artifact_id(artifact_id)

    # Build Solr query
    if group_id:
        q = f"g:{group_id}+AND+a:{artifact}"
    else:
        q = f"a:{artifact}"

    params: Dict[str, Any] = {
        "q":    q,
        "core": "gav",
        "rows": _ROWS,
        "wt":   "json",
    }

    try:
        data = get_json(MAVEN_SEARCH_API, params=params, timeout=20)
    except NotFoundError:
        return None
    except HttpError:
        return None

    if _CACHE_AVAILABLE and data:
        _cache.save(cache_key, data, namespace=_CACHE_NS)

    return data


def _fetch_page(artifact_id: str, start: int = 0, rows: int = _ROWS) -> Optional[Dict[str, Any]]:
    """Fetch one page of Maven Central results starting at *start* offset."""
    group_id, artifact = _parse_artifact_id(artifact_id)
    q = f"g:{group_id}+AND+a:{artifact}" if group_id else f"a:{artifact}"
    params: Dict[str, Any] = {
        "q":    q,
        "core": "gav",
        "rows": rows,
        "start": start,
        "wt":   "json",
    }
    try:
        return get_json(MAVEN_SEARCH_API, params=params, timeout=20)
    except (NotFoundError, HttpError):
        return None


def get_all_versions(artifact_id: str) -> List[Dict[str, Any]]:
    """Return all version docs from Maven Central for *artifact_id*.

    Paginates through results to retrieve more than _ROWS versions.
    Each doc has at minimum: {'v': '1.2.3', 'timestamp': 1234567890000}
    """
    # Use cache for the full paginated result
    cache_key = _make_cache_key("versions", artifact_id)
    if _CACHE_AVAILABLE:
        cached = _cache.load(cache_key, ttl_hours=_CACHE_TTL, namespace=_CACHE_NS)
        if cached is not None:
            return cached

    all_docs: List[Dict[str, Any]] = []
    start = 0
    while start < _MAX_TOTAL_ROWS:
        page = _fetch_page(artifact_id, start=start, rows=_ROWS)
        if not page:
            break
        response = page.get("response") or {}
        docs = response.get("docs") or []
        valid = [d for d in docs if isinstance(d, dict) and d.get("v")]
        all_docs.extend(valid)
        total = response.get("numFound", 0)
        start += _ROWS
        if start >= total or len(valid) < _ROWS:
            break   # no more pages

    if _CACHE_AVAILABLE and all_docs:
        _cache.save(cache_key, all_docs, namespace=_CACHE_NS)

    return all_docs


def get_latest_version(artifact_id: str) -> Optional[str]:
    """Return the highest stable version from Maven Central."""
    docs = get_all_versions(artifact_id)
    if not docs:
        return None
    version_strings = [d["v"] for d in docs if d.get("v")]
    return latest_stable(version_strings)


def get_version_history(artifact_id: str) -> Dict[str, str]:
    """Return {version: published_at_iso} using Unix-ms timestamps from Solr docs."""
    docs = get_all_versions(artifact_id)
    history: Dict[str, str] = {}
    for doc in docs:
        version = doc.get("v", "")
        ts_ms   = doc.get("timestamp")
        if not version:
            continue
        if ts_ms is not None:
            history[version] = _ms_to_iso(ts_ms)
        else:
            history[version] = ""
    return history


def get_github_repo(artifact_id: str) -> Optional[str]:
    """Maven Central does not expose VCS URLs directly.

    Returns None — callers should resolve via GitHub search or pom.xml.
    """
    return None


def get_changelog_url(artifact_id: str, version: str) -> Optional[str]:
    """Return a best-guess Maven Central search URL for the given artifact."""
    group_id, artifact = _parse_artifact_id(artifact_id)
    if group_id and artifact:
        return (
            f"https://search.maven.org/artifact/{group_id}/{artifact}/{version}/jar"
        )
    return None


def build_package_update(
    artifact_id: str,
    current_version: str,
    idx: int = 1,
) -> Optional[PackageUpdate]:
    """Full pipeline: fetch Maven Central metadata, compute semver bump, return PackageUpdate.

    *artifact_id* may be "com.google.guava:guava" or plain "guava".
    """
    latest = get_latest_version(artifact_id)
    if not latest:
        return None

    btype = bump_type(current_version, latest)
    if btype == "none":
        return None  # Already up to date

    version_history = get_version_history(artifact_id)
    release_date = _format_date(version_history.get(latest, ""))

    group_id, artifact = _parse_artifact_id(artifact_id)
    # Build a human-readable display name
    display_name = artifact_id if ":" in artifact_id else artifact_id

    changelog_url = get_changelog_url(artifact_id, latest)

    return PackageUpdate(
        id=f"P{idx}",
        package=display_name,
        ecosystem="maven",
        current_version=current_version,
        latest_version=latest,
        semver_type=btype,
        changelog_url=changelog_url,
        release_date=release_date,
        release_notes_snippet=None,
        github_repo=None,
    )


# ── Internal helpers ──────────────────────────────────────────────────────────

def _parse_artifact_id(artifact_id: str) -> Tuple[Optional[str], str]:
    """Split 'groupId:artifactId' into (group_id, artifact).

    If no colon is present, returns (None, artifact_id).

    Examples:
        "com.google.guava:guava"  → ("com.google.guava", "guava")
        "guava"                   → (None, "guava")
        "org.springframework:spring-core" → ("org.springframework", "spring-core")
    """
    if ":" in artifact_id:
        parts = artifact_id.split(":", 1)
        return parts[0].strip(), parts[1].strip()
    return None, artifact_id.strip()


def _ms_to_iso(ts_ms: Any) -> str:
    """Convert a Unix millisecond timestamp to YYYY-MM-DD ISO string."""
    try:
        ts_sec = int(ts_ms) / 1000.0
        dt = datetime.fromtimestamp(ts_sec, tz=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError, OSError):
        return ""


def _format_date(date_str: Optional[str]) -> Optional[str]:
    """Return YYYY-MM-DD from an ISO timestamp, or None."""
    if not date_str:
        return None
    m = re.match(r"(\d{4}-\d{2}-\d{2})", date_str)
    return m.group(1) if m else None


def _make_cache_key(*parts: str) -> str:
    """Build a cache key string from parts."""
    if _CACHE_AVAILABLE:
        return _cache.cache_key(*parts)
    import hashlib
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]
