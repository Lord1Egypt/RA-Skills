#!/usr/bin/env python3
"""
gh-pr-changelog.py — Generate changelog from merged PRs between tags/releases
Usage: python3 gh-pr-changelog.py [--from v1.0] [--to v2.0]

Uses `gh` CLI to fetch merged PRs with conventional commit labels.
"""

import argparse
import json
import subprocess
import sys
from collections import defaultdict


def run_gh(args):
    try:
        result = subprocess.run(["gh"] + args, capture_output=True, text=True, check=True, timeout=30)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"gh error: {e.stderr}", file=sys.stderr)
        return ""


CATEGORIES = {
    "💥 Breaking": ["breaking", "major"],
    "✨ Features": ["feature", "feat", "enhancement"],
    "🐛 Bug Fixes": ["bug", "fix"],
    "📖 Documentation": ["docs", "documentation"],
    "🎨 Refactoring": ["refactor", "refactoring"],
    "🧪 Tests": ["test", "tests", "testing"],
    "⚡ Performance": ["perf", "performance"],
    "🔧 Maintenance": ["chore", "deps", "dependencies", "ci", "build"],
}


def categorize_pr(pr):
    labels = [lbl["name"].lower() for lbl in pr.get("labels", [])]
    for category, keywords in CATEGORIES.items():
        for k in keywords:
            if k in labels:
                return category
    # Fallback: check title prefix
    title = pr.get("title", "")
    for prefix, keywords in {
        "✨ Features": ["feat:", "feature:"],
        "🐛 Bug Fixes": ["fix:", "bugfix:"],
        "📖 Documentation": ["docs:"],
        "🎨 Refactoring": ["refactor:", "refact:"],
        "🧪 Tests": ["test:", "tests:"],
        "⚡ Performance": ["perf:"],
        "🔧 Maintenance": ["chore:", "build:", "ci:", "deps:"],
    }.items():
        for k in keywords:
            if title.lower().startswith(k):
                return prefix
    return "🔧 Maintenance"


def main():
    parser = argparse.ArgumentParser(description="Generate changelog from merged PRs.")
    parser.add_argument("--from", dest="from_ref", help="Starting tag/branch/release")
    parser.add_argument("--to", dest="to_ref", default="HEAD", help="Ending tag/branch/release (default: HEAD)")
    parser.add_argument("--repo", help="GitHub repo (owner/repo, defaults to current)")
    parser.add_argument("--output", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    # Build search query
    repo = args.repo or run_gh(["repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"])
    query = f"repo:{repo} is:pr is:merged sort:updated-desc"
    if args.from_ref:
        from_date = run_gh(["release", "view", args.from_ref, "--json", "publishedAt", "--jq", ".publishedAt"])
        if from_date:
            query += f" merged:>={from_date[:10]}"

    print(f"🔍 Fetching merged PRs: {query}", file=sys.stderr)
    result = run_gh(["pr", "list", "--search", query, "--json",
                     "number,title,url,labels,mergedAt,author,baseRefName",
                     "--limit", "100", "--state", "merged"])

    if not result:
        print("No PRs found.", file=sys.stderr)
        return

    try:
        prs = json.loads(result)
    except json.JSONDecodeError:
        print("Failed to parse PR list", file=sys.stderr)
        return

    grouped = defaultdict(list)
    for pr in prs:
        cat = categorize_pr(pr)
        grouped[cat].append(pr)

    if args.output == "json":
        print(json.dumps(grouped, indent=2))
        return

    # Markdown output
    from_label = args.from_ref or "previous release"
    print(f"# Changelog\n")
    print(f"Changes from {from_label} to {args.to_ref}\n")

    for category, items in CATEGORIES.items():
        prs_in = grouped.get(category, [])
        if not prs_in:
            continue
        print(f"## {category}\n")
        for pr in sorted(prs_in, key=lambda x: x["mergedAt"] or ""):
            title = pr["title"]
            num = pr["number"]
            url = pr["url"]
            author = pr.get("author", {}).get("login", "unknown")
            print(f"- {title} [#{num}]({url}) by @{author}")
        print()

    total = sum(len(v) for v in grouped.values())
    print(f"---\n_{total} changes across {len(grouped)} categories_")


if __name__ == "__main__":
    main()
