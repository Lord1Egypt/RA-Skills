#!/usr/bin/env python3
"""
Fleet PR Agent — Multi-repo PR triage
Usage: triage.py owner/repo1 [owner/repo2 ...] [--output file.md]
Requires: gh CLI authenticated (gh auth status)
"""

import json
import subprocess
import sys
import argparse
from datetime import datetime, timezone

STALE_DAYS = 5
CI_WEIGHT = 3
MAX_PRS = 50

def gh(args, repo=None):
    cmd = ["gh", "pr", "list", "--repo", repo, "--state", "open",
           "--limit", str(MAX_PRS), "--json",
           "number,title,url,createdAt,updatedAt,isDraft,reviewDecision,statusCheckRollup,labels"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return []
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

def ci_state(pr):
    checks = pr.get("statusCheckRollup") or []
    if not checks:
        return "UNKNOWN"
    failures = [c for c in checks if c.get("conclusion") == "FAILURE"]
    if failures:
        return "FAILURE"
    successes = [c for c in checks if c.get("conclusion") == "SUCCESS"]
    if len(successes) == len(checks):
        return "SUCCESS"
    return "PENDING"

def age_days(created_at):
    try:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        return (now - created).days
    except Exception:
        return 0

def classify(pr):
    c_state = ci_state(pr)
    decision = pr.get("reviewDecision") or "NONE"
    age = age_days(pr.get("createdAt", ""))
    draft = pr.get("isDraft", False)

    if c_state == "FAILURE" and age >= 3:
        return "P0"
    if decision == "APPROVED":
        return "P1"
    if age >= 2 and decision == "REVIEW_REQUIRED":
        return "P1"
    if age >= STALE_DAYS and not draft:
        return "P2"
    return "P3"

def main():
    parser = argparse.ArgumentParser(description="Fleet PR Agent — Multi-repo triage")
    parser.add_argument("repos", nargs="+")
    parser.add_argument("--output", "-o", default=None)
    args = parser.parse_args()

    p0, p1, p2, p3 = [], [], [], []
    total = 0

    for repo in args.repos:
        prs = gh([], repo=repo)
        total += len(prs)
        for pr in prs:
            num = pr.get("number", "?")
            title = pr.get("title", "(no title)")
            url = pr.get("url", "")
            c_state = ci_state(pr)
            decision = pr.get("reviewDecision") or "NONE"
            age = age_days(pr.get("createdAt", ""))
            entry = f"- [#{num} {title}]({url}) — age: {age}d, CI: {c_state}, review: {decision}"

            bucket = {"P0": p0, "P1": p1, "P2": p2, "P3": p3}.get(classify(pr), p3)
            bucket.append(entry)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [f"## PR Triage Report — {today}\n"]

    for label, bucket in [("P0 — Critical", p0), ("P1 — High", p1),
                          ("P2 — Medium", p2), ("P3 — Low", p3)]:
        if bucket:
            lines.append(f"### {label} ({len(bucket)})\n")
            lines.extend(b + "\n" for b in bucket)
            lines.append("\n")

    lines.append("### Summary\n")
    lines.append(f"- Total open PRs: {total}\n")
    lines.append(f"- Needing attention: {len(p0) + len(p1)}\n")
    lines.append(f"- Repos scanned: {len(args.repos)}\n")

    report = "".join(lines)
    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

if __name__ == "__main__":
    main()
