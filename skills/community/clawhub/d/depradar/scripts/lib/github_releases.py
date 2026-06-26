"""GitHub Releases API backend for /depradar.

Primary data source: fetches release notes and CHANGELOG.md for packages.
Free: 60 req/hr unauth, 5000 req/hr with GITHUB_TOKEN.
"""
from __future__ import annotations

import base64
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
import importlib.util as _ilu
if "_depradar_http" not in sys.modules:
    _http_spec = _ilu.spec_from_file_location("_depradar_http", str(Path(__file__).parent / "http.py"))
    _http_mod = _ilu.module_from_spec(_http_spec)   # type: ignore[arg-type]
    sys.modules["_depradar_http"] = _http_mod
    _http_spec.loader.exec_module(_http_mod)         # type: ignore[union-attr]
_http_mod = sys.modules["_depradar_http"]
get_json       = _http_mod.get_json
get_text       = _http_mod.get_text
RateLimitError = _http_mod.RateLimitError
NotFoundError  = _http_mod.NotFoundError
HttpError      = _http_mod.HttpError
from schema import PackageUpdate
from semver import bump_type, newer_versions, latest_stable, parse as parse_ver
from dates import days_ago, today_utc, recency_score
import cache


GITHUB_API = "https://api.github.com"
RAW_GITHUB = "https://raw.githubusercontent.com"

# CHANGELOG filenames to try in order
CHANGELOG_FILENAMES = [
    "CHANGELOG.md", "CHANGELOG", "HISTORY.md", "HISTORY",
    "RELEASES.md", "CHANGES.md", "CHANGES", "NEWS.md",
]

DEPTH_CONFIG = {
    "quick":   {"max_releases": 3,   "max_releases_major": 50},
    "default": {"max_releases": 10,  "max_releases_major": 100},
    "deep":    {"max_releases": 20,  "max_releases_major": 300},
}


def _collect_intermediate_bodies(
    releases: List[Dict[str, Any]],
    current_version: str,
    latest_version: str,
) -> str:
    """Concatenate release notes for ALL versions strictly newer than current up to latest.

    For a jump like openai 0.28.0→1.35.0 this returns the release bodies from every
    intermediate release (v0.29, v1.0, v1.1 ... v1.35), separated by section headers,
    so changelog_parser can extract breaking changes from each individual release.

    Returns empty string if no bodies are available.
    """
    current_v = parse_ver(current_version)
    latest_v  = parse_ver(latest_version)

    sections: List[str] = []
    for rel in releases:
        tag = (rel.get("tag_name") or "").lstrip("v")
        v = parse_ver(tag)
        if v is None:
            continue
        # Include releases strictly newer than current, up to and including latest
        if current_v is not None and v <= current_v:
            continue
        if latest_v is not None and v > latest_v:
            continue
        body = (rel.get("body") or "").strip()
        if body:
            sections.append(f"## Release {tag}\n\n{body}")

    return "\n\n---\n\n".join(sections)


def fetch_package_updates(
    package: str,
    current_version: str,
    github_repo: Optional[str],
    ecosystem: str = "npm",
    days: int = 30,
    depth: str = "default",
    token: Optional[str] = None,
) -> Optional[PackageUpdate]:
    """
    1. If github_repo is None, try to resolve it from npm/pypi metadata
    2. Fetch all releases via GET /repos/{owner}/{repo}/releases
    3. Filter to releases newer than current_version
    4. Find latest stable
    5. Fetch release body (release notes) for the latest
    6. Try to fetch CHANGELOG.md for additional context
    7. Return PackageUpdate with release_notes_snippet populated
       (breaking_changes filled later by changelog_parser)
    """
    cfg = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])
    max_releases: int = cfg["max_releases"]

    # For multi-major version jumps (e.g. 0.8.0→1.47.0) raise the release cap
    # so _collect_intermediate_bodies() can see all intermediate releases.
    try:
        cur_major = int(current_version.split(".")[0].lstrip("v"))
    except (ValueError, AttributeError):
        cur_major = None
    _is_multi_major_jump = False  # resolved below once we know latest


    # Step 1: resolve repo if not given
    repo = github_repo
    if not repo:
        if ecosystem in ("npm",):
            repo = resolve_repo_from_npm(package)
        elif ecosystem in ("pypi",):
            repo = resolve_repo_from_pypi(package)

    if not repo:
        return None

    # Parse owner/repo
    parts = repo.split("/")
    if len(parts) != 2:
        return None
    owner, repo_name = parts[0], parts[1]

    # Cache check
    ck = cache.cache_key("gh_releases", owner, repo_name, current_version, days, depth)
    cached = cache.load(ck, ttl_hours=cache.REGISTRY_TTL_HOURS, namespace="gh_releases")
    if cached is not None:
        return PackageUpdate.from_dict(cached)

    since_date = days_ago(days)

    # Step 2: fetch releases — use stop_at_version so we always collect back
    # to current_version even for large jumps like 0.8.0→1.47.0.
    try:
        releases = fetch_releases(
            owner, repo_name, since_date, max_releases, token,
            stop_at_version=current_version,
        )
    except (RateLimitError, HttpError, NotFoundError):
        return None

    if not releases:
        return None

    # Step 3: filter to versions newer than current
    all_tag_versions = [r.get("tag_name", "").lstrip("v") for r in releases]
    newer = newer_versions(all_tag_versions, current_version)

    if not newer:
        return None

    # Detect multi-major jump; if so, re-fetch with higher limit so intermediate
    # releases between current and latest are all present for changelog analysis.
    try:
        latest_candidate = latest_stable(newer) or newer[0]
        lat_major = int(latest_candidate.split(".")[0].lstrip("v"))
        _is_multi_major_jump = (cur_major is not None and lat_major > cur_major)
    except (ValueError, AttributeError):
        _is_multi_major_jump = False

    if _is_multi_major_jump:
        major_cap = cfg.get("max_releases_major", max_releases * 10)
        if len(releases) >= max_releases:
            # We hit the low cap; re-fetch with the higher major-jump cap
            try:
                releases = fetch_releases(
                    owner, repo_name, since_date, major_cap, token,
                    stop_at_version=current_version,
                )
                # Rebuild newer list from the expanded set
                all_tag_versions = [r.get("tag_name", "").lstrip("v") for r in releases]
                newer = newer_versions(all_tag_versions, current_version)
                if not newer:
                    return None
            except (RateLimitError, HttpError, NotFoundError):
                pass  # fall through with what we already have

    # Step 4: find latest stable
    latest = latest_stable(newer)
    if not latest:
        latest = newer[0]  # fallback to newest pre-release

    # Find the release object matching latest
    latest_release: Optional[Dict[str, Any]] = None
    for rel in releases:
        tag = rel.get("tag_name", "").lstrip("v")
        if tag == latest:
            latest_release = rel
            break

    if not latest_release:
        latest_release = releases[0]
        latest = latest_release.get("tag_name", "").lstrip("v")

    # Step 5: release notes — collect ALL intermediate release bodies for multi-version jumps
    # (e.g. openai 0.28→1.35 gets bodies from every release between those versions)
    release_body = _collect_intermediate_bodies(releases, current_version, latest)
    if not release_body:
        # Fallback: at minimum use the latest release body
        release_body = (latest_release.get("body") or "").strip()
    # For major version jumps, use a larger snippet to capture multi-release content
    snippet_limit = 8000 if bump_type(current_version, latest) == "major" else 400
    release_notes_snippet = release_body[:snippet_limit].strip() if release_body else None

    # Release date
    published_at = latest_release.get("published_at") or latest_release.get("created_at")
    release_date: Optional[str] = None
    if published_at:
        release_date = published_at[:10]

    # Changelog URL
    changelog_url = latest_release.get("html_url")

    # Step 6: fetch CHANGELOG.md and extract version sections.
    # For multi-major jumps (e.g. starknet v7→v9) extract ALL intermediate
    # sections (v8.0.0, v9.0.0) — not just the latest — so changelog_parser
    # has the full picture of every breaking release in the range.
    changelog_text: Optional[str] = None
    changelog_section: Optional[str] = None
    try:
        changelog_text = fetch_changelog_md(owner, repo_name, token)
        if changelog_text:
            try:
                from changelog_parser import parse_all_version_sections
                changelog_section = parse_all_version_sections(
                    changelog_text, current_version, latest
                )
            except Exception:
                # Fallback: extract only the latest section
                try:
                    from changelog_parser import parse_version_section
                    changelog_section = parse_version_section(changelog_text, latest)
                except Exception:
                    pass
    except Exception:
        pass

    # Combine changelog section + release body for maximum extraction coverage.
    # Changelog (structured, authoritative) comes first; release body follows
    # for Conventional Commit markers the CHANGELOG may not repeat.
    if changelog_section and release_notes_snippet:
        combined = f"{changelog_section}\n\n---\n\n{release_notes_snippet}"
        release_notes_snippet = combined[:snippet_limit].strip()
    elif changelog_section:
        release_notes_snippet = changelog_section[:snippet_limit].strip()
    elif not release_notes_snippet and changelog_text:
        # Last resort: use raw CHANGELOG beginning so the parser has something to work with
        release_notes_snippet = changelog_text[:600].strip()

    # Determine semver bump type
    bump = bump_type(current_version, latest)

    # Build the PackageUpdate
    update = PackageUpdate(
        id="",  # caller assigns
        package=package,
        ecosystem=ecosystem,
        current_version=current_version,
        latest_version=latest,
        semver_type=bump,
        has_breaking_changes=(bump == "major"),
        breaking_changes=[],
        changelog_url=changelog_url,
        release_date=release_date,
        release_notes_snippet=release_notes_snippet,
        impact_locations=[],
        impact_confidence="not_scanned",
        github_repo=f"{owner}/{repo_name}",
        subs=None,
        score=0,
        cross_refs=[],
    )

    cache.save(ck, update.to_dict(), namespace="gh_releases")
    return update


def fetch_changelog_md(
    owner: str,
    repo: str,
    token: Optional[str] = None,
) -> Optional[str]:
    """Try to fetch CHANGELOG.md (or alternatives) from the repo.

    Tries raw.githubusercontent.com first (faster), falls back to API.
    Tries main branch, then master.
    Returns raw markdown text or None.
    """
    headers = _github_headers(token)

    for branch in ("main", "master"):
        for filename in CHANGELOG_FILENAMES:
            raw_url = f"{RAW_GITHUB}/{owner}/{repo}/{branch}/{filename}"
            try:
                text = get_text(raw_url, headers=headers)
                if text:
                    return text
            except NotFoundError:
                continue
            except HttpError:
                continue

    # Fallback: try GitHub API contents endpoint
    for branch in ("main", "master"):
        for filename in CHANGELOG_FILENAMES:
            api_url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{filename}"
            try:
                data = get_json(api_url, headers=headers, params={"ref": branch})
                if isinstance(data, dict) and data.get("content"):
                    content_b64 = data["content"].replace("\n", "")
                    try:
                        return base64.b64decode(content_b64).decode("utf-8", errors="replace")
                    except Exception:
                        pass
            except (NotFoundError, HttpError):
                continue

    return None


def fetch_releases(
    owner: str,
    repo: str,
    since_date: str,
    max_count: int = 10,
    token: Optional[str] = None,
    stop_at_version: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Fetch GitHub releases since since_date.

    Args:
        stop_at_version: When set, stop paginating as soon as a release tag
            is <= this version (after stripping 'v' prefix). This ensures
            multi-version jumps (e.g. 0.8.0→1.47.0) collect all intermediate
            releases instead of stopping after max_count newest ones.
        max_count: Hard upper bound on total releases fetched (API budget cap).

    Returns list of raw release dicts (newest first).
    """
    headers = _github_headers(token)
    url = f"{GITHUB_API}/repos/{owner}/{repo}/releases"

    stop_v = parse_ver(stop_at_version) if stop_at_version else None

    releases: List[Dict[str, Any]] = []
    page = 1
    per_page = min(max(max_count, 30), 100)  # fetch up to 100/page when cap is large

    while len(releases) < max_count:
        try:
            page_data = get_json(
                url,
                headers=headers,
                params={"per_page": per_page, "page": page},
            )
        except (RateLimitError, NotFoundError, HttpError):
            break

        if not isinstance(page_data, list) or not page_data:
            break

        for rel in page_data:
            # Date filter: releases are newest-first; once we pass since_date we can stop
            pub = rel.get("published_at") or rel.get("created_at") or ""
            if pub and pub[:10] < since_date:
                return releases

            releases.append(rel)

            # Version filter: stop once we reach a release at or before stop_at_version
            if stop_v is not None:
                tag = (rel.get("tag_name") or "").lstrip("v")
                rel_v = parse_ver(tag)
                if rel_v is not None and rel_v <= stop_v:
                    return releases

            if len(releases) >= max_count:
                return releases

        if len(page_data) < per_page:
            break  # no more pages
        page += 1

    return releases


def resolve_repo_from_npm(package: str) -> Optional[str]:
    """Fallback: query npm registry to find the GitHub repo."""
    npm_url = f"https://registry.npmjs.org/{package}/latest"
    try:
        data = get_json(npm_url)
    except HttpError:
        return None

    repo_info = data.get("repository", {})
    if isinstance(repo_info, str):
        return _parse_repo_url(repo_info)
    if isinstance(repo_info, dict):
        url = repo_info.get("url", "")
        return _parse_repo_url(url)

    # Also check homepage
    homepage = data.get("homepage", "")
    if homepage:
        parsed = _parse_repo_url(homepage)
        if parsed:
            return parsed

    return None


def resolve_repo_from_pypi(package: str) -> Optional[str]:
    """Fallback: query PyPI JSON API to find the GitHub repo."""
    pypi_url = f"https://pypi.org/pypi/{package}/json"
    try:
        data = get_json(pypi_url)
    except HttpError:
        return None

    info = data.get("info", {})

    # Check project_urls first (most reliable)
    project_urls = info.get("project_urls") or {}
    for key in ("Source", "Source Code", "Repository", "Homepage", "Code"):
        url = project_urls.get(key, "")
        if url:
            parsed = _parse_repo_url(url)
            if parsed:
                return parsed

    # Fallback to home_page
    home_page = info.get("home_page", "")
    if home_page:
        return _parse_repo_url(home_page)

    return None


def _parse_repo_url(url: str) -> Optional[str]:
    """Extract 'owner/repo' from various GitHub URL formats."""
    if not url:
        return None

    # Normalize git+https:// or git:// prefixes
    url = re.sub(r"^git\+", "", url)
    url = re.sub(r"^git://", "https://", url)
    url = url.rstrip("/").rstrip(".git")

    # Match github.com URLs
    match = re.search(r"github\.com[:/]([^/]+)/([^/\s#?]+)", url)
    if match:
        owner = match.group(1)
        repo = match.group(2).rstrip(".git")
        return f"{owner}/{repo}"

    return None


def _github_headers(token: Optional[str]) -> Dict[str, str]:
    hdrs = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        hdrs["Authorization"] = f"Bearer {token}"
    return hdrs
