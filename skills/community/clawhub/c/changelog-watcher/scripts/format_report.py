#!/usr/bin/env python3
"""
format_report.py - Format new releases JSON into a clean markdown report.

Usage:
    python3 format_report.py [input.json]
    cat new_releases.json | python3 format_report.py

Output: Markdown report on stdout.
"""

import json
import sys
import os
from datetime import datetime, timezone


BREAKING_KEYWORDS = [
    "breaking change", "breaking:", "breaking!", "⚠️", "!important",
    "deprecat", "removed", "dropped support", "no longer supported",
    "migration required", "migration guide", "upgrade guide",
    "incompatible", "API change", "major change",
]


def detect_breaking_changes(body: str) -> list[str]:
    """Extract lines/sections that look like breaking changes."""
    if not body:
        return []
    lines = body.splitlines()
    breaking = []
    for line in lines:
        lower = line.lower()
        if any(kw.lower() in lower for kw in BREAKING_KEYWORDS):
            clean = line.strip().lstrip("#-*> ").strip()
            if clean and len(clean) > 3:
                breaking.append(clean)
    return breaking


def summarize_body(body: str, max_lines: int = 8) -> str:
    """Return first meaningful lines of release body, trimmed."""
    if not body or not body.strip():
        return ""
    lines = [l.rstrip() for l in body.splitlines() if l.strip()]
    return "\n".join(lines[:max_lines])


def format_date(iso: str) -> str:
    if not iso:
        return "Unknown date"
    try:
        # Handle both Z and +00:00 suffixes
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return iso[:10] if len(iso) >= 10 else iso


def format_release(r: dict) -> str:
    source = r.get("source", "")
    display_name = r.get("display_name", r.get("package", r.get("repo", "Unknown")))
    tag = r.get("tag", "")
    prev = r.get("previous_version", "")
    date = format_date(r.get("published_at", ""))
    url = r.get("url", "")
    body = r.get("body", "") or ""
    prerelease = r.get("prerelease", False)

    # Header
    pre_badge = " *(pre-release)*" if prerelease else ""
    version_line = f"`{prev}` → `{tag}`" if prev else f"`{tag}`"
    lines = [
        f"## {display_name}{pre_badge}",
        f"**Version:** {version_line}  ",
        f"**Released:** {date}  ",
    ]
    if url:
        lines.append(f"**Release page:** {url}  ")
    lines.append("")

    # Breaking changes
    breaking = detect_breaking_changes(body)
    if breaking:
        lines.append("### ⚠️ Breaking Changes")
        for b in breaking:
            lines.append(f"- {b}")
        lines.append("")

    # Summary
    summary = summarize_body(body)
    if summary:
        lines.append("### What's New")
        lines.append(summary)
        lines.append("")
    else:
        lines.append("*No release notes provided.*")
        lines.append("")

    return "\n".join(lines)


def format_report(releases: list) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if not releases:
        return f"# Changelog Report — {now}\n\nNo new releases since last check.\n"

    # Group by source for the header count
    github_count = sum(1 for r in releases if r.get("source") == "github")
    npm_count = sum(1 for r in releases if r.get("source") == "npm")

    parts = [f"# Changelog Report — {now}\n"]

    counts = []
    if github_count:
        counts.append(f"{github_count} GitHub")
    if npm_count:
        counts.append(f"{npm_count} npm")
    parts.append(f"**{len(releases)} new release{'s' if len(releases) != 1 else ''}** ({', '.join(counts)})\n")
    parts.append("---\n")

    for r in releases:
        parts.append(format_release(r))
        parts.append("---\n")

    return "\n".join(parts)


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        path = sys.argv[1]
        if not os.path.exists(path):
            print(f"[error] File not found: {path}", file=sys.stderr)
            sys.exit(1)
        with open(path, "r") as f:
            data = json.load(f)
    else:
        try:
            raw = sys.stdin.read()
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"[error] Invalid JSON input: {e}", file=sys.stderr)
            sys.exit(1)

    if not isinstance(data, list):
        print("[error] Expected a JSON array of releases", file=sys.stderr)
        sys.exit(1)

    report = format_report(data)
    print(report)


if __name__ == "__main__":
    main()
