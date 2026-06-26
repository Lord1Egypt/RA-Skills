#!/usr/bin/env python3
"""
Bounty Hunter Agent — bounty_scan.py

Scans GitHub for bounty-labeled issues, evaluates competition,
scores by payout and viability, and outputs a ranked list.

Pure Python stdlib — no external dependencies.
"""

import json
import os
import subprocess
import sys
import re
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration (env overrides)
# ---------------------------------------------------------------------------
MIN_PAYOUT = int(os.environ.get("BOUNTY_MIN_PAYOUT", "25"))
MAX_COMPETITION = int(os.environ.get("BOUNTY_MAX_COMPETITION", "5"))
SCAN_LIMIT = int(os.environ.get("BOUNTY_SCAN_LIMIT", "100"))
STATE_DIR = Path(
    os.environ.get(
        "BOUNTY_STATE_DIR",
        Path.home() / ".agents" / "skills" / "bounty-hunter-agent" / "state",
    )
)

# Scoring weights (sum to 100)
W_PAYOUT = 50
W_COMPETITION = 35
W_FRESHNESS = 15

# Labels that indicate a bounty
BOUNTY_LABELS = [
    "bounty",
    "💰",
    "reward",
    "paid",
    "algora",
    "opire",
    "cash",
    "prize",
]

# GitHub search queries
SEARCH_QUERIES = [
    'label:bounty state:open',
    'label:"💰" state:open',
    '"bounty" in:title state:open is:issue',
    '"algora" in:comments state:open is:issue',
    'label:reward state:open',
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def gh_api(endpoint: str, method: str = "GET", paginate: bool = False) -> any:
    """Call GitHub API via gh CLI."""
    cmd = ["gh", "api", endpoint, "--method", method]
    if paginate:
        cmd.append("--paginate")
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout) if result.stdout.strip() else None
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def gh_search_issues(query: str, limit: int = 50) -> list:
    """Search GitHub issues using gh CLI."""
    cmd = [
        "gh", "search", "issues",
        query,
        "--limit", str(limit),
        "--json", "repository,number,title,labels,url,createdAt,comments",
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            return []
        return json.loads(result.stdout) if result.stdout.strip() else []
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return []


def extract_payout(issue: dict) -> int:
    """Extract USD payout amount from labels and title."""
    payout = 0
    text_sources = [issue.get("title", "")]

    for label in issue.get("labels", []):
        name = label.get("name", "") if isinstance(label, dict) else str(label)
        text_sources.append(name)

    for text in text_sources:
        # Match patterns like "$200", "200 USD", "💰 200", "bounty: $500"
        matches = re.findall(
            r'\$\s*(\d[\d,]*(?:\.\d{2})?)'
            r'|(\d[\d,]*(?:\.\d{2})?)\s*(?:USD|usd|\$)'
            r'|💰\s*(\d[\d,]*)',
            text
        )
        for groups in matches:
            for g in groups:
                if g:
                    val = int(g.replace(",", "").split(".")[0])
                    payout = max(payout, val)

    return payout


def count_competing_prs(repo: str, issue_number: int) -> int:
    """Count open PRs that reference this issue."""
    # Check linked PRs via timeline events
    endpoint = f"repos/{repo}/issues/{issue_number}/timeline"
    events = gh_api(endpoint)
    if not events or not isinstance(events, list):
        return 0

    pr_count = 0
    for event in events:
        if isinstance(event, dict):
            source = event.get("source", {})
            issue_data = source.get("issue", {}) if isinstance(source, dict) else {}
            if isinstance(issue_data, dict) and issue_data.get("pull_request"):
                state = issue_data.get("state", "")
                if state == "open":
                    pr_count += 1

    return pr_count


def score_bounty(payout: int, competing_prs: int, age_days: float) -> float:
    """Score a bounty opportunity (0-100). Higher is better."""
    # Normalize payout (cap at $1000 for scaling)
    payout_score = min(payout / 1000.0, 1.0) * W_PAYOUT

    # Competition penalty (0 PRs = full score, MAX_COMPETITION+ = 0)
    if competing_prs >= MAX_COMPETITION:
        comp_score = 0
    else:
        comp_score = (1 - competing_prs / MAX_COMPETITION) * W_COMPETITION

    # Freshness (newer = better, cap at 90 days)
    max_age = 90.0
    if age_days >= max_age:
        fresh_score = 0
    else:
        fresh_score = (1 - age_days / max_age) * W_FRESHNESS

    return round(payout_score + comp_score + fresh_score, 1)


def load_state() -> dict:
    """Load persisted state."""
    state_file = STATE_DIR / "bounties.json"
    if state_file.exists():
        try:
            with open(state_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"scanned_at": None, "bounties": [], "dismissed": []}


def save_state(state: dict) -> None:
    """Persist state to JSON."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_file = STATE_DIR / "bounties.json"
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2, default=str)


# ---------------------------------------------------------------------------
# Main scan
# ---------------------------------------------------------------------------
def scan() -> list:
    """Run the full bounty scan pipeline."""
    print("🔍 Bounty Hunter Agent — Scanning for opportunities...\n")

    # Verify gh auth
    auth_check = subprocess.run(
        ["gh", "auth", "status"], capture_output=True, text=True
    )
    if auth_check.returncode != 0:
        print("❌ gh CLI not authenticated. Run: gh auth login")
        sys.exit(1)

    # Collect unique issues from all search queries
    seen = set()  # (repo, number)
    raw_issues = []

    for query in SEARCH_QUERIES:
        print(f"  Searching: {query}")
        results = gh_search_issues(query, limit=SCAN_LIMIT // len(SEARCH_QUERIES))
        for issue in results:
            repo_data = issue.get("repository", {})
            if isinstance(repo_data, dict):
                repo = repo_data.get("nameWithOwner", "")
            else:
                repo = str(repo_data)

            number = issue.get("number", 0)
            key = (repo, number)
            if key not in seen and repo and number:
                seen.add(key)
                issue["_repo"] = repo
                raw_issues.append(issue)

    print(f"\n📋 Found {len(raw_issues)} unique bounty-labeled issues\n")

    # Load previous state for dismissed issues
    state = load_state()
    dismissed = set(tuple(d) for d in state.get("dismissed", []))

    # Evaluate each issue
    bounties = []
    for i, issue in enumerate(raw_issues):
        repo = issue["_repo"]
        number = issue["number"]

        if (repo, number) in dismissed:
            continue

        # Extract payout
        payout = extract_payout(issue)
        if payout < MIN_PAYOUT:
            continue

        # Calculate age
        created = issue.get("createdAt", "")
        try:
            created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - created_dt).days
        except (ValueError, AttributeError):
            age_days = 30  # default

        # Check competition (rate-limit friendly: brief pause)
        print(f"  [{i+1}/{len(raw_issues)}] {repo}#{number}: ${payout} — checking competition...")
        competing_prs = count_competing_prs(repo, number)
        if competing_prs >= MAX_COMPETITION:
            print(f"    ⏭️  Skipping — {competing_prs} competing PRs")
            continue

        # Score it
        score = score_bounty(payout, competing_prs, age_days)

        bounties.append({
            "repo": repo,
            "issue": number,
            "title": issue.get("title", ""),
            "payout_usd": payout,
            "competing_prs": competing_prs,
            "score": score,
            "url": issue.get("url", f"https://github.com/{repo}/issues/{number}"),
            "labels": [
                (l.get("name", "") if isinstance(l, dict) else str(l))
                for l in issue.get("labels", [])
            ],
            "age_days": age_days,
            "created_at": created,
        })

        # Be nice to the API
        time.sleep(0.5)

    # Sort by score descending
    bounties.sort(key=lambda b: b["score"], reverse=True)

    # Add rank
    for i, b in enumerate(bounties):
        b["rank"] = i + 1

    # Save state
    state["scanned_at"] = datetime.now(timezone.utc).isoformat()
    state["bounties"] = bounties
    save_state(state)

    return bounties


def print_report(bounties: list) -> None:
    """Print a human-readable report."""
    if not bounties:
        print("\n😐 No actionable bounties found above threshold.")
        print(f"   (min payout: ${MIN_PAYOUT}, max competition: {MAX_COMPETITION} PRs)")
        return

    print(f"\n{'='*70}")
    print(f" 🏆 BOUNTY HUNTER REPORT — {len(bounties)} actionable opportunities")
    print(f"{'='*70}\n")

    for b in bounties[:20]:  # Top 20
        comp_indicator = "🟢" if b["competing_prs"] == 0 else (
            "🟡" if b["competing_prs"] <= 2 else "🔴"
        )
        print(f"  #{b['rank']:>2}  Score: {b['score']:>5.1f}  |  ${b['payout_usd']:>4}  |  "
              f"{comp_indicator} {b['competing_prs']} PRs  |  {b['age_days']}d old")
        print(f"       {b['repo']}#{b['issue']}")
        print(f"       {b['title'][:65]}")
        print(f"       {b['url']}")
        print()

    state_path = STATE_DIR / "bounties.json"
    print(f"📁 Full results saved to: {state_path}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    bounties = scan()
    print_report(bounties)
