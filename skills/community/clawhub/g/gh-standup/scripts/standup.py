#!/usr/bin/env python3
"""
gh-standup: Generate a standup summary from GitHub PRs and commits.

Usage:
  python3 standup.py --repo ORG/REPO [--standup-days Friday] [--author @me]
  python3 standup.py --org ORG [--standup-days Monday,Thursday] [--author username]
"""

import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone

WEEKDAYS = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6,
}

def last_standup_date(standup_days: list[str]) -> date:
    """Return the most recent past standup day (not today)."""
    today = date.today()
    day_nums = sorted([WEEKDAYS[d.lower()] for d in standup_days])
    best = None
    for offset in range(1, 8):
        candidate = today - timedelta(days=offset)
        if candidate.weekday() in day_nums:
            best = candidate
            break
    return best or (today - timedelta(days=7))


def gh_api_simple(endpoint: str) -> list | dict:
    """Single-page gh api call (no --paginate)."""
    result = subprocess.run(["gh", "api", endpoint], capture_output=True, text=True)
    if result.returncode != 0:
        return []
    try:
        return json.loads(result.stdout.strip())
    except Exception:
        return []


def gh_api(endpoint: str, params: dict = None) -> list | dict:
    # Build query string directly in URL to avoid gh -f treating as POST body
    url = endpoint
    if params:
        qs = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{endpoint}?{qs}"
    cmd = ["gh", "api", "--paginate", url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[gh error] {result.stderr.strip()}", file=sys.stderr)
        return []
    raw = result.stdout.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        import re
        chunks = re.findall(r'\[.*?\]', raw, re.DOTALL)
        combined = []
        for chunk in chunks:
            try:
                combined.extend(json.loads(chunk))
            except Exception:
                pass
        return combined


def get_author_login(author_arg: str) -> str:
    if author_arg != "@me":
        return author_arg
    result = subprocess.run(["gh", "api", "user", "--jq", ".login"],
                            capture_output=True, text=True)
    return result.stdout.strip() or "@me"


def get_repos(org: str) -> list[str]:
    data = gh_api(f"orgs/{org}/repos", {"type": "all", "per_page": "100"})
    return [r["full_name"] for r in data if isinstance(r, dict)]


def fetch_prs(repo: str, author: str, since_iso: str) -> list[dict]:
    data = gh_api(
        f"repos/{repo}/pulls",
        {"state": "closed", "sort": "updated", "direction": "desc", "per_page": "100"}
    )
    results = []
    for pr in data:
        if not isinstance(pr, dict):
            continue
        merged_at = pr.get("merged_at")
        if not merged_at or merged_at < since_iso:
            continue
        login = pr.get("user", {}).get("login", "")
        if author != "@me" and login != author:
            continue
        results.append(pr)
    return results


def fetch_commits(repo: str, author: str, since_iso: str) -> list[dict]:
    params = {"since": since_iso, "per_page": "100"}
    if author != "@me":
        params["author"] = author
    data = gh_api(f"repos/{repo}/commits", params)
    return [c for c in data if isinstance(c, dict)]


def format_pr(pr: dict) -> str:
    num = pr.get("number", "?")
    title = pr.get("title", "")
    url = pr.get("html_url", "")
    return f"  • PR #{num}: {title}\n    {url}"


def format_commit(c: dict) -> str:
    sha = c.get("sha", "")[:7]
    msg = c.get("commit", {}).get("message", "").split("\n")[0]
    return f"  • `{sha}` {msg}"


def main():
    parser = argparse.ArgumentParser(description="Generate standup summary from GitHub")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--repo", help="GitHub repo (e.g. org/repo)")
    group.add_argument("--org", help="GitHub organization (all repos)")
    parser.add_argument("--standup-days", default="Friday",
                        help="Comma-separated weekday(s), e.g. Monday,Thursday (default: Friday)")
    parser.add_argument("--author", default="@me",
                        help="GitHub username or @me (default: @me)")
    args = parser.parse_args()

    standup_days = [d.strip() for d in args.standup_days.split(",")]
    since_date = last_standup_date(standup_days)
    since_iso = since_date.isoformat() + "T00:00:00Z"
    today_str = date.today().isoformat()

    author = get_author_login(args.author)

    repos = [args.repo] if args.repo else get_repos(args.org)
    if not repos:
        print("No repos found.", file=sys.stderr)
        sys.exit(1)

    all_prs = []
    all_commits = []

    for repo in repos:
        prs = fetch_prs(repo, author, since_iso)
        commits = fetch_commits(repo, author, since_iso)
        for pr in prs:
            pr["_repo"] = repo
        for c in commits:
            c["_repo"] = repo
        all_prs.extend(prs)
        all_commits.extend(commits)

    # De-dup commits that are part of merged PRs (by SHA or message pattern)
    pr_shas = set()
    pr_numbers = {pr["number"] for pr in all_prs}
    for pr in all_prs:
        repo = pr["_repo"]
        pr_num = pr["number"]
        data = gh_api_simple(f"repos/{repo}/pulls/{pr_num}/commits")
        for c in data:
            if isinstance(c, dict):
                pr_shas.add(c.get("sha", ""))

    import re as _re
    def _is_pr_merge_commit(c: dict) -> bool:
        msg = c.get("commit", {}).get("message", "").split("\n")[0]
        # Match "... (#NNN)" pattern where NNN is a known PR
        m = _re.search(r'\(#(\d+)\)$', msg)
        if m and int(m.group(1)) in pr_numbers:
            return True
        # Match "Merge pull request #NNN"
        m2 = _re.search(r'Merge pull request #(\d+)', msg)
        if m2 and int(m2.group(1)) in pr_numbers:
            return True
        return False

    standalone_commits = [
        c for c in all_commits
        if c.get("sha") not in pr_shas and not _is_pr_merge_commit(c)
    ]

    # Output
    print(f"## 📊 Standup Summary ({since_date} → {today_str})\n")
    print(f"**Author:** {author}  |  **Repos:** {', '.join(repos)}\n")

    if all_prs:
        print(f"### ✅ Merged PRs ({len(all_prs)})\n")
        for pr in all_prs:
            repo_label = f"[{pr['_repo']}] " if len(repos) > 1 else ""
            print(f"{repo_label}{format_pr(pr)}")
        print()

    if standalone_commits:
        print(f"### 🔧 Direct Commits ({len(standalone_commits)})\n")
        for c in standalone_commits:
            repo_label = f"[{c['_repo']}] " if len(repos) > 1 else ""
            print(f"{repo_label}{format_commit(c)}")
        print()

    if not all_prs and not standalone_commits:
        print("_No activity found in this period._")


if __name__ == "__main__":
    main()
