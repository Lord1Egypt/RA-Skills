#!/usr/bin/env python3
"""
check_updates.py — Check Docker Hub / GHCR for newer image versions.

Reads JSON from scan_containers.py (stdin or file arg), queries registries,
and outputs JSON with update status for each container.

Usage:
    python3 scan_containers.py | python3 check_updates.py
    python3 check_updates.py containers.json
"""

import json
import sys
import os
import re
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone


DOCKERHUB_API = "https://hub.docker.com/v2"
GHCR_API = "https://ghcr.io/v2"
REQUEST_TIMEOUT = 15
RATE_LIMIT_SLEEP = 2  # seconds between requests to avoid 429s


def _is_pure_version_tag(tag):
    """
    Return True only for tags that are purely version numbers (with optional 'v' prefix).
    Accepts: 1, 1.2, 1.2.3, v1.2.3, 1.2.3.4
    Rejects: 1.2.3-alpine, 1-slim, 32bit, latest-alpine, 1.2.3rc1
    """
    return bool(re.match(r'^v?\d+(\.\d+)*$', tag))


def fetch_json(url, headers=None, timeout=REQUEST_TIMEOUT):
    """Fetch URL and return parsed JSON, or None on error."""
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return {"_rate_limited": True}
        if e.code == 404:
            return {"_not_found": True}
        if e.code in (401, 403):
            return {"_private": True}
        return {"_error": f"HTTP {e.code}"}
    except urllib.error.URLError as e:
        return {"_error": str(e.reason)}
    except Exception as e:
        return {"_error": str(e)}


def parse_semver(tag):
    """
    Extract (major, minor, patch) from a tag string.
    Returns None if not parseable as semver-like.
    """
    # Strip leading 'v'
    t = tag.lstrip("v")
    m = re.match(r'^(\d+)(?:\.(\d+))?(?:\.(\d+))?', t)
    if not m:
        return None
    major = int(m.group(1))
    minor = int(m.group(2)) if m.group(2) is not None else 0
    patch = int(m.group(3)) if m.group(3) is not None else 0
    return (major, minor, patch)


def is_newer(candidate_tag, current_tag):
    """Return True if candidate_tag is a newer semver than current_tag."""
    c = parse_semver(candidate_tag)
    cur = parse_semver(current_tag)
    if c is None or cur is None:
        return False
    return c > cur


def version_bump_type(current_tag, latest_tag):
    """Return 'major', 'minor', 'patch', or 'unknown'."""
    c = parse_semver(current_tag)
    l = parse_semver(latest_tag)
    if c is None or l is None:
        return "unknown"
    if l[0] > c[0]:
        return "major"
    if l[1] > c[1]:
        return "minor"
    if l[2] > c[2]:
        return "patch"
    return "same"


def get_all_dockerhub_tags(namespace, repo, max_pages=10):
    """
    Fetch multiple pages of Docker Hub tags and return all results.
    Docker Hub's tag ordering is not reliable for semver — scan multiple pages
    to find the highest version tag regardless of sort order.
    """
    all_results = []
    # Use last_updated ordering to get recently updated tags first (more likely to be recent versions)
    url = (
        f"{DOCKERHUB_API}/repositories/{namespace}/{repo}/tags/"
        f"?page_size=100&ordering=-last_updated"
    )
    for _ in range(max_pages):
        if not url:
            break
        data = fetch_json(url)
        if data is None or "_error" in data or "_rate_limited" in data or "_not_found" in data or "_private" in data:
            return all_results, data
        results = data.get("results", [])
        all_results.extend(results)
        url = data.get("next")  # None when no more pages
        if not url:
            break
        time.sleep(0.3)  # be polite between pages
    return all_results, None


def get_dockerhub_tags(namespace, repo, current_tag):
    """
    Query Docker Hub for tags. Returns dict with update info.
    """
    all_tags, err_data = get_all_dockerhub_tags(namespace, repo)

    if err_data is not None:
        if "_rate_limited" in err_data:
            return {"status": "rate_limited"}
        if "_not_found" in err_data:
            return {"status": "not_found"}
        if "_private" in err_data:
            return {"status": "private"}
        return {"status": "error", "error": err_data.get("_error", "unknown")}

    if not all_tags:
        return {"status": "no_tags"}

    # Filter to tags that look like pure versions (not sha digests, not 'latest' etc.)
    SKIP_TAGS = {"latest", "stable", "edge", "nightly", "dev", "beta", "alpha",
                 "slim", "alpine", "bullseye", "buster", "focal", "jammy", "noble"}
    versioned = [
        r for r in all_tags
        if _is_pure_version_tag(r.get("name", ""))
        and r.get("name", "") not in SKIP_TAGS
    ]

    # Also grab the full tag list names for reference
    all_tag_names = [r["name"] for r in all_tags[:25]]

    # Find the best "latest" candidate by highest semver
    best = None
    best_parsed = None

    for r in versioned:
        tag_name = r.get("name", "")
        parsed = parse_semver(tag_name)
        if parsed is None:
            continue
        if best_parsed is None or parsed > best_parsed:
            best = r
            best_parsed = parsed

    # Find source repo URL if available
    source_url = None
    repo_data_url = f"{DOCKERHUB_API}/repositories/{namespace}/{repo}/"
    repo_data = fetch_json(repo_data_url)
    if repo_data and "_error" not in repo_data and "_rate_limited" not in repo_data:
        full_desc = repo_data.get("full_description", "") or ""
        # Look for GitHub links
        gh_match = re.search(r'github\.com/[\w.-]+/[\w.-]+', full_desc)
        if gh_match:
            source_url = "https://" + gh_match.group(0)

    if best is None:
        return {
            "status": "up_to_date",
            "current_tag": current_tag,
            "latest_tag": current_tag,
            "all_tags": all_tag_names[:10],
            "source_url": source_url,
        }

    latest_tag = best["name"]
    last_updated = best.get("last_updated", "")

    if latest_tag == current_tag or not is_newer(latest_tag, current_tag):
        status = "up_to_date"
        bump = "same"
    else:
        status = "update_available"
        bump = version_bump_type(current_tag, latest_tag)

    # Calculate days behind
    days_behind = None
    if last_updated and status == "update_available":
        try:
            # Docker Hub returns ISO8601
            dt = datetime.fromisoformat(last_updated.rstrip("Z")).replace(tzinfo=timezone.utc)
            days_behind = (datetime.now(timezone.utc) - dt).days
        except Exception:
            pass

    return {
        "status": status,
        "current_tag": current_tag,
        "latest_tag": latest_tag,
        "bump_type": bump,
        "days_behind": days_behind,
        "last_updated": last_updated,
        "all_tags": all_tag_names[:10],
        "source_url": source_url,
    }


def check_container(container):
    """Check a single container for updates. Returns enriched container dict."""
    registry = container.get("registry")
    namespace = container.get("namespace", "library")
    repo = container.get("repo", "")
    tag = container.get("tag", "latest")

    result = container.copy()

    # Skip non-DockerHub registries we can't check (GHCR requires auth for private)
    if registry and registry not in ("docker.io", "registry-1.docker.io"):
        result["update_check"] = {
            "status": "skipped",
            "reason": f"Registry '{registry}' not supported (only Docker Hub supported without auth)",
        }
        return result

    # Skip sha256 digests as tags
    if tag.startswith("sha256:"):
        result["update_check"] = {
            "status": "skipped",
            "reason": "Image pinned by digest — cannot compare versions",
        }
        return result

    # Skip tags that aren't version-like (e.g. "latest" alone)
    if tag == "latest":
        result["update_check"] = {
            "status": "skipped",
            "reason": "Tag is 'latest' — cannot determine if update is available",
        }
        return result

    update_info = get_dockerhub_tags(namespace, repo, tag)
    result["update_check"] = update_info
    return result


def main():
    # Read input
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

    containers = data.get("containers", [])
    if not containers:
        print(json.dumps({"error": None, "results": [], "message": "No containers to check."}))
        sys.exit(0)

    results = []
    for i, container in enumerate(containers):
        if i > 0:
            time.sleep(RATE_LIMIT_SLEEP)
        checked = check_container(container)
        results.append(checked)

    output = {
        "error": None,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
