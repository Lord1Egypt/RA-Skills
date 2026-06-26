"""crates.io Registry API backend for /depradar.

No auth required. API: https://crates.io/api/v1/crates/{crate}
crates.io requires a User-Agent header or returns 403.
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
from pathlib import Path
from typing import Any, Dict, List, Optional

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
from semver import bump_type, latest_stable, newer_versions
from dates import today_utc, days_ago

try:
    import cache as _cache
    _CACHE_AVAILABLE = True
except ImportError:
    _CACHE_AVAILABLE = False


# ── Constants ─────────────────────────────────────────────────────────────────

CRATES_API  = "https://crates.io/api/v1/crates"
_CACHE_NS   = "crates_registry"
_CACHE_TTL  = 6.0   # hours

# crates.io requires a descriptive User-Agent or returns 403
_USER_AGENT = "depradar-skill/1.0 (contact@depradar.dev)"


# ── Public API ────────────────────────────────────────────────────────────────

def fetch_package_info(crate: str) -> Optional[Dict[str, Any]]:
    """GET crates.io/api/v1/crates/{crate} → full metadata dict. Cached 6h.

    Returns None on 404 or network error.
    """
    cache_key = _make_cache_key("info", crate)

    if _CACHE_AVAILABLE:
        cached = _cache.load(cache_key, ttl_hours=_CACHE_TTL, namespace=_CACHE_NS)
        if cached is not None:
            return cached

    try:
        url  = f"{CRATES_API}/{crate}"
        data = get_json(
            url,
            headers={"User-Agent": _USER_AGENT},
            timeout=20,
        )
    except NotFoundError:
        return None
    except HttpError:
        return None

    if _CACHE_AVAILABLE and data:
        _cache.save(cache_key, data, namespace=_CACHE_NS)

    return data


def get_latest_version(crate: str) -> Optional[str]:
    """Return the latest stable version string from crates.io."""
    info = fetch_package_info(crate)
    if not info:
        return None

    # .crate.max_stable_version is the canonical latest stable field
    crate_meta = info.get("crate", {})
    max_stable = crate_meta.get("max_stable_version")
    if max_stable:
        return max_stable

    # Fallback: compute from versions list
    versions = _extract_version_strings(info)
    return latest_stable(versions)


def get_version_history(crate: str) -> Dict[str, str]:
    """Return {version: created_at_iso} for all published versions.

    Skips yanked versions.
    """
    info = fetch_package_info(crate)
    if not info:
        return {}

    history: Dict[str, str] = {}
    for ver in (info.get("versions") or []):
        if not isinstance(ver, dict):
            continue
        if ver.get("yanked"):
            continue
        num = ver.get("num", "")
        created_at = ver.get("created_at", "")
        if num:
            history[num] = created_at

    return history


def get_github_repo(crate: str) -> Optional[str]:
    """Extract GitHub 'owner/repo' from crates.io metadata."""
    info = fetch_package_info(crate)
    if not info:
        return None
    crate_meta = info.get("crate", {})
    return _parse_github_repo(crate_meta.get("repository") or "")


def get_changelog_url(crate: str, version: str) -> Optional[str]:
    """Best-guess changelog URL from crates.io metadata."""
    info = fetch_package_info(crate)
    if not info:
        return None

    crate_meta = info.get("crate", {})

    # Explicit changelog link in metadata
    changelog = crate_meta.get("changelog") or ""
    if changelog:
        return changelog

    # Derive from repository URL
    repo = _parse_github_repo(crate_meta.get("repository") or "")
    if repo:
        return f"https://github.com/{repo}/releases/tag/v{version}"

    return None


def build_package_update(
    crate: str,
    current_version: str,
    idx: int = 1,
) -> Optional[PackageUpdate]:
    """Full pipeline: fetch crates.io metadata, compute semver bump, return PackageUpdate."""
    info = fetch_package_info(crate)
    if not info:
        return None

    latest = get_latest_version(crate)
    if not latest:
        return None

    btype = bump_type(current_version, latest)
    if btype == "none":
        return None  # Already up to date

    version_history = get_version_history(crate)
    release_date = _format_date(version_history.get(latest))

    # Release notes snippet from the crate's description
    crate_meta = info.get("crate", {})
    description = crate_meta.get("description") or ""
    snippet = description[:400] if description else None

    github_repo   = _parse_github_repo(crate_meta.get("repository") or "")
    changelog_url = get_changelog_url(crate, latest)

    all_versions = list(version_history.keys())
    _newer = newer_versions(all_versions, current_version)

    return PackageUpdate(
        id=f"P{idx}",
        package=crate,
        ecosystem="cargo",
        current_version=current_version,
        latest_version=latest,
        semver_type=btype,
        changelog_url=changelog_url,
        release_date=release_date,
        release_notes_snippet=snippet,
        github_repo=github_repo,
    )


# ── Internal helpers ──────────────────────────────────────────────────────────

def _extract_version_strings(info: Dict[str, Any]) -> List[str]:
    """Extract all non-yanked version strings from a crates.io response."""
    result: List[str] = []
    for ver in (info.get("versions") or []):
        if isinstance(ver, dict) and not ver.get("yanked"):
            num = ver.get("num", "")
            if num:
                result.append(num)
    return result


def _parse_github_repo(url: str) -> Optional[str]:
    """Extract 'owner/repo' from a GitHub repository URL."""
    if not url:
        return None
    m = re.search(
        r"github\.com[/:]([^/\s]+/[^/\s\.]+?)(?:\.git)?(?:/|$|\s)",
        url,
    )
    if m:
        return m.group(1)
    return None


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
