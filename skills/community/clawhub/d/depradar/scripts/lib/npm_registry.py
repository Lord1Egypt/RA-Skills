"""npm Registry API backend — fetch version history and repo URL.

No authentication required. Free for any use.
Endpoint: https://registry.npmjs.org/{package}
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

NPM_REGISTRY = "https://registry.npmjs.org"
_CACHE_NS    = "npm_registry"
_CACHE_TTL   = 6.0   # hours


# ── Public API ────────────────────────────────────────────────────────────────

def fetch_package_info(
    package: str,
    registry_url: str = NPM_REGISTRY,
) -> Optional[Dict[str, Any]]:
    """GET {registry}/{package} → full metadata dict. Cached 6h."""
    cache_key = _make_cache_key("info", package, registry_url)

    if _CACHE_AVAILABLE:
        cached = _cache.load(cache_key, ttl_hours=_CACHE_TTL, namespace=_CACHE_NS)
        if cached is not None:
            return cached

    try:
        url  = f"{registry_url.rstrip('/')}/{_encode_package(package)}"
        data = get_json(url, timeout=20)
    except NotFoundError:
        return None
    except HttpError:
        return None

    if _CACHE_AVAILABLE and data:
        _cache.save(cache_key, data, namespace=_CACHE_NS)

    return data


def fetch_version_manifest(
    package: str,
    version: str,
    registry_url: str = NPM_REGISTRY,
) -> Optional[Dict[str, Any]]:
    """GET {registry}/{package}/{version} → per-version manifest. Cached 6h."""
    cache_key = _make_cache_key("version_manifest", package, version, registry_url)

    if _CACHE_AVAILABLE:
        cached = _cache.load(cache_key, ttl_hours=_CACHE_TTL, namespace=_CACHE_NS)
        if cached is not None:
            return cached

    try:
        url  = f"{registry_url.rstrip('/')}/{_encode_package(package)}/{version}"
        data = get_json(url, timeout=15)
    except (NotFoundError, HttpError):
        return None

    if _CACHE_AVAILABLE and data:
        _cache.save(cache_key, data, namespace=_CACHE_NS)

    return data


def detect_esm_cjs_transition(
    package: str,
    old_version: str,
    new_version: str,
    registry_url: str = NPM_REGISTRY,
) -> Optional[Any]:
    """Detect if a package switched from CommonJS to ESM-only between versions.

    Returns a BreakingChange if a CJS→ESM transition is detected, else None.
    This catches the chalk v5 / pure-ESM problem that keyword scanning misses.
    """
    from schema import BreakingChange

    old_manifest = fetch_version_manifest(package, old_version, registry_url)
    new_manifest = fetch_version_manifest(package, new_version, registry_url)
    if not old_manifest or not new_manifest:
        return None

    old_type = old_manifest.get("type", "commonjs")
    new_type = new_manifest.get("type", "commonjs")

    # CJS → ESM transition
    if old_type != "module" and new_type == "module":
        # Check if new version provides a CJS export via the exports map
        new_exports = new_manifest.get("exports") or {}
        has_cjs_compat = False
        if isinstance(new_exports, dict):
            # Look for "require" key anywhere in exports map
            exports_str = str(new_exports)
            has_cjs_compat = '"require"' in exports_str or "'require'" in exports_str
        elif new_manifest.get("main") and not new_manifest.get("type"):
            has_cjs_compat = True

        if not has_cjs_compat:
            # Derive a sensible JS import alias from the package name:
            #   @noble/hashes  → hashes   (strip scope)
            #   react-dom      → reactDom  (kebab → camelCase)
            #   chalk          → chalk     (unchanged)
            _pkg_base = package.lstrip("@").split("/")[-1]
            _alias = re.sub(r"-([a-zA-Z])", lambda m: m.group(1).upper(), _pkg_base)
            return BreakingChange(
                symbol="module type",
                change_type="behavior_changed",
                description=(
                    f"{package} v{new_version} is ESM-only "
                    f"(\"type\": \"module\" in package.json). "
                    f"CommonJS require('{package}') will throw ERR_REQUIRE_ESM. "
                    f"Previous version ({old_version}) was CommonJS-compatible."
                ),
                migration_note=(
                    f"Switch to `import {_alias} from '{package}'` syntax. "
                    f"For a CJS/ESM bridge use dynamic: "
                    f"`const {_alias} = (await import('{package}')).default`. "
                    f"If you're on an older Node.js version or a CJS-only bundler, "
                    f"you cannot upgrade to v{new_version} yet."
                ),
                source="npm_registry",
                confidence="high",
                source_excerpt=f"package.json: {{\"type\": \"module\"}} (v{new_version})",
            )

    return None


def get_latest_version(package: str, registry_url: str = NPM_REGISTRY) -> Optional[str]:
    """Return latest stable version tag."""
    info = fetch_package_info(package, registry_url=registry_url)
    if not info:
        return None
    # Try dist-tags.latest first (fastest, most reliable)
    dist_tags = info.get("dist-tags", {})
    if dist_tags.get("latest"):
        return dist_tags["latest"]
    # Fall back: compute from time keys
    versions = list((info.get("versions") or {}).keys())
    return latest_stable(versions)


def get_version_history(package: str, registry_url: str = NPM_REGISTRY) -> Dict[str, str]:
    """Return {version: published_at_iso} for all versions."""
    info = fetch_package_info(package, registry_url=registry_url)
    if not info:
        return {}
    time_map: Dict[str, str] = info.get("time", {})
    # Remove non-version keys
    return {
        ver: ts
        for ver, ts in time_map.items()
        if ver not in ("created", "modified") and re.match(r"^\d", ver)
    }


def get_github_repo(package: str, registry_url: str = NPM_REGISTRY) -> Optional[str]:
    """Extract GitHub 'owner/repo' from registry metadata."""
    info = fetch_package_info(package, registry_url=registry_url)
    if not info:
        return None
    return _extract_github_repo_from_info(info)


def get_changelog_url(package: str, version: str, registry_url: str = NPM_REGISTRY) -> Optional[str]:
    """Best-guess changelog URL from registry metadata."""
    info = fetch_package_info(package, registry_url=registry_url)
    if not info:
        return None

    repo = _extract_github_repo_from_info(info)
    if repo:
        # Most npm packages use GitHub releases or CHANGELOG.md
        return f"https://github.com/{repo}/releases/tag/v{version}"

    # Check homepage for changelog hints
    homepage = info.get("homepage", "") or ""
    if "github.com" in homepage:
        repo_m = re.search(r"github\.com/([^/]+/[^/\s#?]+)", homepage)
        if repo_m:
            repo_path = repo_m.group(1).rstrip(".git")
            return f"https://github.com/{repo_path}/releases/tag/v{version}"

    return None


def build_package_update(
    package: str,
    current_version: str,
    idx: int = 1,
    registry_url: str = NPM_REGISTRY,
) -> Optional[PackageUpdate]:
    """Full pipeline: fetch metadata, compute semver bump, return PackageUpdate."""
    info = fetch_package_info(package, registry_url=registry_url)
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

    # Release notes snippet from latest version's description
    versions_meta = info.get("versions", {})
    latest_meta   = versions_meta.get(latest, {})
    description   = latest_meta.get("description") or info.get("description") or ""
    snippet       = description[:400] if description else None

    github_repo = _extract_github_repo_from_info(info)
    changelog_url = get_changelog_url(package, latest)

    # Newer versions between current and latest
    all_versions  = list(version_history.keys())
    _newer = newer_versions(all_versions, current_version)

    update = PackageUpdate(
        id=f"P{idx}",
        package=package,
        ecosystem="npm",
        current_version=current_version,
        latest_version=latest,
        semver_type=btype,
        changelog_url=changelog_url,
        release_date=_format_date(release_date),
        release_notes_snippet=snippet,
        github_repo=github_repo,
    )

    # ESM/CJS transition detection (first-class, not reliant on keyword scan)
    esm_change = detect_esm_cjs_transition(package, current_version, latest, registry_url)
    if esm_change is not None:
        update.has_breaking_changes = True
        update.breaking_changes.append(esm_change)

    return update


# ── Internal helpers ──────────────────────────────────────────────────────────

def _encode_package(package: str) -> str:
    """URL-encode scoped package names: @scope/name → %40scope%2Fname."""
    if package.startswith("@"):
        # Encode the leading @ and the /
        return package.replace("@", "%40").replace("/", "%2F")
    return package


def _extract_github_repo_from_info(info: Dict[str, Any]) -> Optional[str]:
    """Parse GitHub owner/repo from npm registry metadata."""
    # 1. repository field
    repo_field = info.get("repository")
    if isinstance(repo_field, dict):
        url = repo_field.get("url", "")
    elif isinstance(repo_field, str):
        url = repo_field
    else:
        url = ""

    if url:
        m = re.search(r"github\.com[/:]([^/\s]+/[^/\s\.]+?)(?:\.git)?(?:\s|$|/)", url)
        if m:
            return m.group(1)

    # 2. bugs field
    bugs = info.get("bugs", {})
    if isinstance(bugs, dict):
        bugs_url = bugs.get("url", "")
    elif isinstance(bugs, str):
        bugs_url = bugs
    else:
        bugs_url = ""

    if bugs_url:
        m = re.search(r"github\.com/([^/]+/[^/\s#?]+)", bugs_url)
        if m:
            return m.group(1).rstrip(".git")

    # 3. homepage
    homepage = info.get("homepage", "") or ""
    if "github.com" in homepage:
        m = re.search(r"github\.com/([^/]+/[^/\s#?]+)", homepage)
        if m:
            return m.group(1).rstrip(".git")

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
