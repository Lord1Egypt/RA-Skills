"""PyPI JSON API backend — fetch version history and repo URL.

No authentication required. Free for any use.
Endpoint: https://pypi.org/pypi/{package}/json
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

import urllib.error   # noqa: F401 — loaded cleanly without lib/ shadowing
import urllib.request  # noqa: F401 — loads http.client from stdlib

for _p in reversed(_popped):  # restore in original order
    sys.path.insert(0, _p)

# Now lib/ is back and urllib is cached — load our local http.py by file path.
# Share the instance via sys.modules so all modules use the same exception classes.
if "_depradar_http" not in sys.modules:
    _http_spec = _ilu.spec_from_file_location(
        "_depradar_http", str(Path(__file__).parent / "http.py")
    )
    _http_mod = _ilu.module_from_spec(_http_spec)  # type: ignore[arg-type]
    sys.modules["_depradar_http"] = _http_mod
    _http_spec.loader.exec_module(_http_mod)        # type: ignore[union-attr]
_http_mod = sys.modules["_depradar_http"]
get_json      = _http_mod.get_json
NotFoundError = _http_mod.NotFoundError
HttpError     = _http_mod.HttpError

sys.path.insert(0, _lib_dir)

from semver import newer_versions, latest_stable, bump_type
from schema import PackageUpdate
from dates import today_utc, days_ago

try:
    import cache as _cache
    _CACHE_AVAILABLE = True
except ImportError:
    _CACHE_AVAILABLE = False


# ── Constants ─────────────────────────────────────────────────────────────────

PYPI_API    = "https://pypi.org/pypi"
_CACHE_NS   = "pypi_registry"
_CACHE_TTL  = 6.0   # hours


# ── Public API ────────────────────────────────────────────────────────────────

def fetch_package_info(package: str) -> Optional[Dict[str, Any]]:
    """GET pypi.org/pypi/{package}/json → full metadata dict. Cached 6h."""
    cache_key = _make_cache_key("info", package)

    if _CACHE_AVAILABLE:
        cached = _cache.load(cache_key, ttl_hours=_CACHE_TTL, namespace=_CACHE_NS)
        if cached is not None:
            return cached

    try:
        url  = f"{PYPI_API}/{package}/json"
        data = get_json(url, timeout=20)
    except NotFoundError:
        return None
    except HttpError:
        return None

    if _CACHE_AVAILABLE and data:
        _cache.save(cache_key, data, namespace=_CACHE_NS)

    return data


def get_latest_version(package: str) -> Optional[str]:
    """Return latest stable version tag."""
    info = fetch_package_info(package)
    if not info:
        return None
    # PyPI provides info.version as the latest
    pkg_info = info.get("info", {})
    declared = pkg_info.get("version")
    if declared and not _is_prerelease(declared):
        return declared
    # Fall back: find highest stable across all releases
    releases = list((info.get("releases") or {}).keys())
    return latest_stable(releases)


def get_version_history(package: str) -> Dict[str, str]:
    """Return {version: published_at_iso} for all versions.

    Uses the upload_time of the first file in each release.
    """
    info = fetch_package_info(package)
    if not info:
        return {}

    releases: Dict[str, Any] = info.get("releases", {})
    history: Dict[str, str] = {}

    for version, file_list in releases.items():
        if not file_list:
            continue
        # Pick the earliest upload_time in this release
        upload_times = [
            f.get("upload_time_iso_8601") or f.get("upload_time", "")
            for f in file_list
            if isinstance(f, dict)
        ]
        upload_times = [t for t in upload_times if t]
        if upload_times:
            history[version] = sorted(upload_times)[0]

    return history


def get_github_repo(package: str) -> Optional[str]:
    """Extract GitHub 'owner/repo' from PyPI metadata.

    Checks in order:
    1. .info.project_urls['Source Code']
    2. .info.project_urls['Repository']
    3. .info.project_urls['Source']
    4. .info.project_urls['Code']
    5. .info.home_page
    """
    info = fetch_package_info(package)
    if not info:
        return None
    pkg_info = info.get("info", {})
    return _extract_github_repo_from_info(pkg_info)


def build_package_update(
    package: str,
    current_version: str,
    idx: int = 1,
) -> Optional[PackageUpdate]:
    """Full pipeline: fetch metadata, compute semver bump, return PackageUpdate."""
    info = fetch_package_info(package)
    if not info:
        return None

    latest = get_latest_version(package)
    if not latest:
        return None

    btype = bump_type(current_version, latest)
    if btype == "none":
        return None  # Already up to date

    version_history = get_version_history(package)
    release_date    = version_history.get(latest)

    pkg_info  = info.get("info", {})
    summary   = pkg_info.get("summary") or ""
    snippet   = summary[:400] if summary else None

    github_repo   = _extract_github_repo_from_info(pkg_info)
    changelog_url = _guess_changelog_url(pkg_info, github_repo, latest)

    all_versions  = list(version_history.keys())
    _newer        = newer_versions(all_versions, current_version)

    return PackageUpdate(
        id=f"P{idx}",
        package=package,
        ecosystem="pypi",
        current_version=current_version,
        latest_version=latest,
        semver_type=btype,
        changelog_url=changelog_url,
        release_date=_format_date(release_date),
        release_notes_snippet=snippet,
        github_repo=github_repo,
    )


# ── Internal helpers ──────────────────────────────────────────────────────────

def _extract_github_repo_from_info(pkg_info: Dict[str, Any]) -> Optional[str]:
    """Parse GitHub owner/repo from PyPI .info dict."""
    project_urls: Dict[str, str] = pkg_info.get("project_urls") or {}

    # Check known keys in priority order
    url_keys = [
        "Source Code", "Repository", "Source", "Code",
        "GitHub", "Github", "source", "repository",
    ]
    for key in url_keys:
        url = project_urls.get(key, "")
        if url and "github.com" in url:
            m = re.search(r"github\.com/([^/\s]+/[^/\s#?]+?)(?:\.git)?(?:/|$)", url)
            if m:
                return m.group(1)

    # Check home_page
    home_page = pkg_info.get("home_page", "") or ""
    if home_page and "github.com" in home_page:
        m = re.search(r"github\.com/([^/\s]+/[^/\s#?]+?)(?:\.git)?(?:/|$)", home_page)
        if m:
            return m.group(1)

    # Check all project_urls values
    for url in project_urls.values():
        if url and "github.com" in url:
            m = re.search(r"github\.com/([^/\s]+/[^/\s#?]+?)(?:\.git)?(?:/|$)", url)
            if m:
                return m.group(1)

    return None


def _guess_changelog_url(
    pkg_info: Dict[str, Any],
    github_repo: Optional[str],
    version: str,
) -> Optional[str]:
    """Best-guess changelog URL from PyPI metadata."""
    # Check project_urls for an explicit changelog link
    project_urls: Dict[str, str] = pkg_info.get("project_urls") or {}
    for key in ("Changelog", "Change Log", "Changes", "CHANGELOG", "History"):
        url = project_urls.get(key, "")
        if url:
            return url

    # Use GitHub releases page
    if github_repo:
        return f"https://github.com/{github_repo}/releases/tag/v{version}"

    return None


def _is_prerelease(version: str) -> bool:
    """Return True if version string looks like a pre-release."""
    return bool(re.search(r"[a-zA-Z]", version))


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
