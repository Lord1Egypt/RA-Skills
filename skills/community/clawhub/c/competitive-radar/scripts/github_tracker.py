#!/usr/bin/env python3
"""
github_tracker.py — GitHub org tracker for competitor-radar.

Tracks: star velocity, new releases, new repos, contributor delta.
Uses the GitHub API (public endpoints, no auth required for public repos).
If GITHUB_TOKEN env var is set, uses authenticated requests (higher rate limits).

Usage:
  python3 github_tracker.py <slug>
  python3 github_tracker.py --all
"""

from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
COMPETITORS_FILE = DATA_DIR / "competitors.json"

TODAY = date.today().isoformat()
ONE_WEEK_AGO = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

GITHUB_API = "https://api.github.com"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_competitors() -> dict:
    if not COMPETITORS_FILE.exists():
        return {"competitors": []}
    return json.loads(COMPETITORS_FILE.read_text())


def get_competitor(slug: str) -> dict | None:
    data = load_competitors()
    return next((c for c in data["competitors"] if c["slug"] == slug), None)


def github_headers() -> list[str]:
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = ["-H", "Accept: application/vnd.github+json",
               "-H", "X-GitHub-Api-Version: 2022-11-28"]
    if token:
        headers += ["-H", f"Authorization: Bearer {token}"]
    return headers


def gh_get(path: str) -> dict | list | None:
    url = f"{GITHUB_API}{path}"
    headers = github_headers()
    cmd = ["curl", "-sL", "--max-time", "15"] + headers + [url]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if result.returncode != 0 or not result.stdout.strip():
            return None
        data = json.loads(result.stdout)
        if isinstance(data, dict) and data.get("message"):
            print(f"[github] API error: {data['message']}", file=sys.stderr)
            return None
        return data
    except Exception as e:
        print(f"[github] Error: {e}", file=sys.stderr)
        return None


def snapshot_path(slug: str, key: str) -> Path:
    d = SNAPSHOTS_DIR / slug
    d.mkdir(parents=True, exist_ok=True)
    return d / f"github_{key}_{TODAY}.json"


def previous_github_snapshot(slug: str, key: str) -> dict | None:
    d = SNAPSHOTS_DIR / slug
    if not d.exists():
        return None
    files = sorted(d.glob(f"github_{key}_*.json"), reverse=True)
    prev = files[1] if len(files) > 1 else (files[0] if files else None)
    if prev:
        try:
            return json.loads(prev.read_text())
        except Exception:
            return None
    return None


# ---------------------------------------------------------------------------
# Repo stats
# ---------------------------------------------------------------------------

def get_org_repos(org: str) -> list[dict]:
    """Get all public repos for an org, sorted by stars."""
    repos = gh_get(f"/orgs/{org}/repos?type=public&sort=stargazers&per_page=50")
    if not isinstance(repos, list):
        # Try as a user if org lookup failed
        repos = gh_get(f"/users/{org}/repos?type=public&sort=stargazers&per_page=50")
    if not isinstance(repos, list):
        return []
    return [
        {
            "name": r["name"],
            "full_name": r["full_name"],
            "stars": r.get("stargazers_count", 0),
            "forks": r.get("forks_count", 0),
            "description": r.get("description", ""),
            "pushed_at": r.get("pushed_at", ""),
            "created_at": r.get("created_at", ""),
            "topics": r.get("topics", []),
            "language": r.get("language", ""),
        }
        for r in repos
    ]


def get_recent_releases(org: str, repo_name: str, since: str) -> list[dict]:
    """Get releases for a repo published after `since` (ISO date string)."""
    releases = gh_get(f"/repos/{org}/{repo_name}/releases?per_page=10")
    if not isinstance(releases, list):
        return []
    result = []
    for r in releases:
        pub = r.get("published_at", "")
        if pub and pub >= since:
            result.append({
                "tag": r.get("tag_name", ""),
                "name": r.get("name", ""),
                "published_at": pub,
                "body": (r.get("body") or "")[:600],
                "url": r.get("html_url", ""),
            })
    return result


def get_new_repos(current_repos: list[dict], prev_repos: list[dict] | None) -> list[dict]:
    if not prev_repos:
        return []
    prev_names = {r["name"] for r in prev_repos}
    return [r for r in current_repos if r["name"] not in prev_names]


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_github_for_competitor(slug: str) -> dict:
    competitor = get_competitor(slug)
    if not competitor:
        return {"error": f"Competitor '{slug}' not found", "slug": slug}

    org = competitor.get("urls", {}).get("github_org")
    if not org:
        return {"slug": slug, "skipped": True, "reason": "no_github_org_configured"}

    name = competitor["name"]
    print(f"[github] Tracking {org} for {name}...")

    # Current repo list
    current_repos = get_org_repos(org)
    if not current_repos:
        return {"slug": slug, "error": "Could not fetch repos", "org": org}

    # Previous snapshot
    prev_data = previous_github_snapshot(slug, "repos")
    prev_repos = prev_data.get("repos", []) if prev_data else []

    # Star delta
    total_stars_now = sum(r["stars"] for r in current_repos)
    total_stars_prev = sum(r["stars"] for r in prev_repos) if prev_repos else total_stars_now
    star_delta = total_stars_now - total_stars_prev

    # Top repo stars
    top_repo = max(current_repos, key=lambda r: r["stars"], default={})

    # New repos created this week
    new_repos = get_new_repos(current_repos, prev_repos if prev_repos else None)

    # Recent releases on top repos (top 3 by stars)
    top_3 = sorted(current_repos, key=lambda r: r["stars"], reverse=True)[:3]
    all_new_releases: list[dict] = []
    for repo in top_3:
        releases = get_recent_releases(org, repo["name"], ONE_WEEK_AGO)
        for r in releases:
            r["repo"] = repo["name"]
        all_new_releases.extend(releases)

    # Save snapshot
    snap = {
        "org": org,
        "date": TODAY,
        "total_stars": total_stars_now,
        "repos": current_repos,
    }
    snapshot_path(slug, "repos").write_text(json.dumps(snap, indent=2))

    # Build result
    result = {
        "slug": slug,
        "name": name,
        "org": org,
        "total_stars": total_stars_now,
        "star_delta_week": star_delta,
        "star_delta_pct": round(star_delta / max(total_stars_prev, 1) * 100, 1),
        "top_repo": {
            "name": top_repo.get("name", ""),
            "stars": top_repo.get("stars", 0),
            "description": top_repo.get("description", ""),
        },
        "new_repos_this_week": new_repos,
        "new_releases": all_new_releases,
        "has_signals": bool(star_delta > 500 or new_repos or all_new_releases),
    }

    print(
        f"[github] {org}: {total_stars_now:,} stars "
        f"({'+' if star_delta >= 0 else ''}{star_delta:,} this week), "
        f"{len(all_new_releases)} new releases, {len(new_repos)} new repos"
    )
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="competitor-radar github tracker")
    parser.add_argument("slug", nargs="?", help="Competitor slug")
    parser.add_argument("--all", action="store_true", help="Run for all competitors")
    args = parser.parse_args()

    data = load_competitors()
    active = [c for c in data["competitors"] if c.get("active", True)]

    if args.all:
        slugs = [c["slug"] for c in active]
    elif args.slug:
        slugs = [args.slug]
    else:
        parser.print_help()
        sys.exit(1)

    all_results = [run_github_for_competitor(s) for s in slugs]
    print(json.dumps(all_results, indent=2, default=str))


if __name__ == "__main__":
    main()
