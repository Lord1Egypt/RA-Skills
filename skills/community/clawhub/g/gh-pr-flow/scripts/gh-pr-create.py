#!/usr/bin/env python3
"""
gh-pr-create.py — Interactive helper to create a GitHub PR with gh CLI
Usage: python3 gh-pr-create.py [--title "My Title"] [--base main]

Features:
- Auto-detects current branch and default branch
- Generates title from commit messages if not provided
- Creates PR with extended body from commit log
"""

import argparse
import subprocess
import sys
import re


def run(cmd, capture=True, check=True):
    try:
        result = subprocess.run(cmd, capture_output=capture, text=True, check=check, timeout=30)
        return result.stdout.strip() if capture else result
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {' '.join(cmd)}\n{e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ gh CLI not found. Install: https://cli.github.com")
        sys.exit(1)


def get_current_branch():
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def get_default_branch():
    # Try to get from git remote
    try:
        result = run(["git", "symbolic-ref", "refs/remotes/origin/HEAD"], check=False)
        if result and "/" in result:
            return result.split("/")[-1]
    except Exception:
        pass
    for b in ["main", "master", "develop"]:
        try:
            run(["git", "show-ref", f"refs/heads/{b}"], check=True)
            return b
        except (subprocess.CalledProcessError, SystemExit):
            pass
    return "main"


def get_commit_log(base, head):
    """Get commit messages between base and head."""
    try:
        result = run(["git", "log", f"{base}..{head}", "--oneline"], check=False)
        return result.splitlines() if result else []
    except Exception:
        return []


def generate_title(commits):
    if not commits:
        return ""
    first = re.sub(r"^[\da-f]+\s+", "", commits[0])
    return first.strip()


def generate_body(commits):
    if not commits:
        return ""
    lines = []
    for c in commits:
        clean = re.sub(r"^[\da-f]+\s+", "", c)
        lines.append(f"- {clean}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Create a GitHub PR with auto-generated content.")
    parser.add_argument("--title", help="PR title (optional, auto-detected from commits)")
    parser.add_argument("--base", help="Base branch (optional, auto-detected)")
    parser.add_argument("--draft", action="store_true", help="Create as draft PR")
    parser.add_argument("--label", action="append", help="Add label (can repeat)")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    parser.add_argument("--body", help="PR body (optional, auto-generated from commits)")
    args = parser.parse_args()

    branch = get_current_branch()
    base = args.base or get_default_branch()

    commits = get_commit_log(base, branch)
    title = args.title or generate_title(commits) or f"Changes from {branch}"
    body = args.body or generate_body(commits)

    print(f"📌 Branch:   {branch}")
    print(f"📎 Base:     {base}")
    print(f"📝 Title:    {title}")
    print(f"  Body:\n{body[:500]}{'…' if len(body) > 500 else ''}")
    if commits:
        print(f"  Commits:   {len(commits)} ahead")

    if not args.yes:
        confirm = input("\nCreate this PR? [Y/n] ").strip().lower()
        if confirm and confirm not in ("y", "yes", ""):
            print("❌ Cancelled.")
            return

    cmd = [
        "gh", "pr", "create",
        "--base", base,
        "--head", branch,
        "--title", title,
        "--body", body,
    ]
    if args.draft:
        cmd.append("--draft")
    if args.label:
        for lbl in args.label:
            cmd.extend(["--label", lbl])

    result = run(cmd)
    print(f"\n✅ PR created: {result}")


if __name__ == "__main__":
    main()
