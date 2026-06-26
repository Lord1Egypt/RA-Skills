#!/usr/bin/env python3
"""
fetch_changelog.py — Fetch release notes for containers with updates available.

Reads JSON from check_updates.py (stdin or file arg).
Attempts to find GitHub source repo from Docker Hub metadata, then fetches
releases via GitHub API (unauthenticated, 60 req/hr limit).

Outputs JSON with changelog text per container.

Usage:
    python3 check_updates.py containers.json | python3 fetch_changelog.py
    python3 fetch_changelog.py updates.json
"""

import json
import sys
import os
import re
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone


GITHUB_API = "https://api.github.com"
REQUEST_TIMEOUT = 15
RATE_LIMIT_SLEEP = 1.5  # be polite to GitHub unauthenticated API


def fetch_json(url, headers=None):
    """Fetch URL and return (data, error_str). data is None on error."""
    default_headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "container-update-advisor/1.0",
    }
    if headers:
        default_headers.update(headers)

    # Inject GitHub token if available
    gh_token = os.environ.get("GITHUB_TOKEN")
    if gh_token:
        default_headers["Authorization"] = f"token {gh_token}"

    req = urllib.request.Request(url, headers=default_headers)
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return None, "rate_limited"
        if e.code == 404:
            return None, "not_found"
        if e.code in (401, 403):
            return None, f"auth_required (HTTP {e.code})"
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, str(e.reason)
    except Exception as e:
        return None, str(e)


def extract_github_repo(source_url):
    """
    Extract 'owner/repo' from a GitHub URL.
    Returns None if not a GitHub URL.
    """
    if not source_url:
        return None
    m = re.search(r'github\.com/([\w.-]+/[\w.-]+)', source_url)
    if m:
        # Strip .git suffix
        return m.group(1).rstrip(".git").rstrip("/")
    return None


def fetch_github_releases(owner_repo, current_tag, latest_tag):
    """
    Fetch GitHub releases between current_tag and latest_tag.
    Returns list of release dicts with name, tag, body.
    """
    url = f"{GITHUB_API}/repos/{owner_repo}/releases?per_page=20"
    data, err = fetch_json(url)
    if err:
        return None, err
    if not isinstance(data, list):
        return None, "unexpected response format"

    # Find releases newer than current_tag
    # We collect releases up to and including latest_tag
    releases = []
    for r in data:
        tag_name = r.get("tag_name", "")
        name = r.get("name", tag_name)
        body = r.get("body", "")
        published = r.get("published_at", "")
        prerelease = r.get("prerelease", False)

        if prerelease:
            continue

        # Include if it's newer than current and <= latest
        from_v = _strip_v(current_tag)
        to_v = _strip_v(latest_tag)
        tag_v = _strip_v(tag_name)

        if _semver_gt(tag_v, from_v) and _semver_lte(tag_v, to_v):
            releases.append({
                "tag": tag_name,
                "name": name,
                "published_at": published,
                "body": body[:3000] if body else "",  # cap size
            })

    return releases, None


def fetch_github_tags_fallback(owner_repo, current_tag, latest_tag):
    """
    Fallback: try /tags endpoint if no releases found.
    Less useful (no body), but at least confirms latest tag exists.
    """
    url = f"{GITHUB_API}/repos/{owner_repo}/tags?per_page=20"
    data, err = fetch_json(url)
    if err:
        return None, err
    if not isinstance(data, list):
        return None, "unexpected"

    tags = [t.get("name", "") for t in data]
    return tags, None


def _strip_v(tag):
    return tag.lstrip("v") if tag else ""


def _parse_ver(s):
    m = re.match(r'^(\d+)(?:\.(\d+))?(?:\.(\d+))?', s or "")
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2) or 0), int(m.group(3) or 0))


def _semver_gt(a, b):
    pa, pb = _parse_ver(a), _parse_ver(b)
    if pa is None or pb is None:
        return False
    return pa > pb


def _semver_lte(a, b):
    pa, pb = _parse_ver(a), _parse_ver(b)
    if pa is None or pb is None:
        return False
    return pa <= pb


def process_container(container):
    """Fetch changelog for a single container. Returns enriched dict."""
    result = container.copy()
    update_check = container.get("update_check", {})
    status = update_check.get("status", "")

    if status != "update_available":
        result["changelog"] = {"status": "skipped", "reason": f"No update available (status: {status})"}
        return result

    source_url = update_check.get("source_url")
    owner_repo = extract_github_repo(source_url)

    if not owner_repo:
        # Try to infer from namespace/repo (many official images map to github.com/namespace/repo)
        namespace = container.get("namespace", "")
        repo = container.get("repo", "")
        if namespace and namespace != "library" and repo:
            owner_repo = f"{namespace}/{repo}"
        elif namespace == "library" and repo:
            # Official images — try docker-library/repo
            owner_repo = f"docker-library/{repo}"

    if not owner_repo:
        result["changelog"] = {
            "status": "no_source",
            "reason": "Could not find GitHub source repository",
        }
        return result

    current_tag = update_check.get("current_tag", "")
    latest_tag = update_check.get("latest_tag", "")

    releases, err = fetch_github_releases(owner_repo, current_tag, latest_tag)

    if err == "not_found":
        # Try alternate repo naming
        result["changelog"] = {
            "status": "not_found",
            "attempted_repo": owner_repo,
            "reason": "GitHub repo not found or has no releases",
        }
        return result

    if err == "rate_limited":
        result["changelog"] = {
            "status": "rate_limited",
            "reason": "GitHub API rate limit reached. Set GITHUB_TOKEN env var for higher limits.",
        }
        return result

    if err:
        result["changelog"] = {"status": "error", "error": err, "repo": owner_repo}
        return result

    if not releases:
        # Try tags fallback
        tags, _ = fetch_github_tags_fallback(owner_repo, current_tag, latest_tag)
        result["changelog"] = {
            "status": "no_releases",
            "repo": owner_repo,
            "reason": "No GitHub releases found between versions. Repo may use tags only.",
            "known_tags": tags[:10] if tags else [],
        }
        return result

    result["changelog"] = {
        "status": "found",
        "repo": owner_repo,
        "releases": releases,
        "release_count": len(releases),
    }
    return result


def main():
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1]) as f:
                data = json.load(f)
        except Exception as e:
            print(json.dumps({"error": f"Could not read input file: {e}", "results": []}))
            sys.exit(1)
    else:
        try:
            data = json.load(sys.stdin)
        except Exception as e:
            print(json.dumps({"error": f"Could not parse stdin JSON: {e}", "results": []}))
            sys.exit(1)

    if "error" in data and data["error"]:
        print(json.dumps({"error": data["error"], "results": []}))
        sys.exit(1)

    results_in = data.get("results", [])
    if not results_in:
        print(json.dumps({"error": None, "results": [], "message": "No containers to process."}))
        sys.exit(0)

    results_out = []
    for i, container in enumerate(results_in):
        if i > 0:
            time.sleep(RATE_LIMIT_SLEEP)
        enriched = process_container(container)
        results_out.append(enriched)

    output = {
        "error": None,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "results": results_out,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
