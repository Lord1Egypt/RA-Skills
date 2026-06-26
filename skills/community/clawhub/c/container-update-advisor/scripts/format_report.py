#!/usr/bin/env python3
"""
format_report.py — Generate a prioritized markdown update report.

Reads JSON from fetch_changelog.py (stdin or file arg).
Produces a markdown report with risk assessment for each container.

Risk rules:
  - Major version bump → "review first"
  - "breaking" in changelog notes → "review first"
  - Minor bump → "review first" (may have breaking API changes)
  - Patch bump → "safe to update"
  - Unknown bump → "review first"

Usage:
    python3 fetch_changelog.py updates.json | python3 format_report.py
    python3 format_report.py changelogs.json
    python3 format_report.py changelogs.json > report.md
"""

import json
import sys
import re
from datetime import datetime, timezone


def assess_risk(container):
    """
    Return ('safe to update' | 'review first', reason_str).
    """
    update_check = container.get("update_check", {})
    changelog = container.get("changelog", {})

    bump = update_check.get("bump_type", "unknown")
    current = update_check.get("current_tag", "?")
    latest = update_check.get("latest_tag", "?")

    reasons = []

    if bump == "major":
        reasons.append("major version bump")
    elif bump == "minor":
        reasons.append("minor version bump (may include API changes)")

    # Scan changelog text for "breaking"
    if changelog.get("status") == "found":
        releases = changelog.get("releases", [])
        for r in releases:
            body = (r.get("body") or "").lower()
            if "breaking" in body or "breaking change" in body or "deprecat" in body:
                if "breaking change" not in reasons:
                    reasons.append("changelog mentions breaking changes")
                break

    if bump in ("major", "unknown") and not reasons:
        reasons.append("version bump type unclear")

    if reasons:
        return "🔴 review first", "; ".join(reasons)
    return "🟢 safe to update", f"patch-level update ({current} → {latest})"


def summarize_changelog(changelog, bump_type):
    """
    Produce a concise plain-text summary from changelog data.
    Caps at ~400 chars per release, max 3 releases shown.
    """
    status = changelog.get("status", "unknown")

    if status == "skipped":
        return "_No update — changelog not fetched._"
    if status == "rate_limited":
        return "_GitHub API rate limited. Set GITHUB_TOKEN for higher limits._"
    if status in ("not_found", "no_source", "no_releases"):
        reason = changelog.get("reason", "")
        return f"_No changelog available. {reason}_"
    if status == "error":
        return f"_Error fetching changelog: {changelog.get('error', 'unknown')}_"
    if status == "found":
        releases = changelog.get("releases", [])
        if not releases:
            return "_No release notes found._"

        lines = []
        for r in releases[:3]:
            tag = r.get("tag", "?")
            name = r.get("name", tag)
            body = r.get("body", "").strip()

            # Extract first meaningful paragraph
            if body:
                # Remove markdown headers, HTML tags
                body = re.sub(r'<[^>]+>', '', body)
                # Get first non-empty lines up to 400 chars
                paras = [p.strip() for p in body.split("\n") if p.strip()]
                snippet = " ".join(paras)[:400]
                if len(" ".join(paras)) > 400:
                    snippet += "…"
            else:
                snippet = "_No release notes._"

            label = f"**{tag}**" if name == tag else f"**{tag}** ({name})"
            lines.append(f"- {label}: {snippet}")

        if len(releases) > 3:
            lines.append(f"- _…and {len(releases) - 3} more release(s)_")

        return "\n".join(lines)

    return "_Changelog status unknown._"


def format_container_section(container):
    """Format a single container as a markdown section."""
    name = container.get("name", "unknown")
    image_raw = container.get("image_raw", "")
    update_check = container.get("update_check", {})
    changelog = container.get("changelog", {})

    status = update_check.get("status", "unknown")

    if status == "up_to_date":
        return f"### ✅ `{name}` — Up to date\n- Image: `{image_raw}`\n"

    if status in ("skipped", "error", "rate_limited", "not_found", "private", "no_tags"):
        reason = update_check.get("reason") or update_check.get("error") or status
        return f"### ⚪ `{name}` — Skipped\n- Image: `{image_raw}`\n- Reason: {reason}\n"

    if status != "update_available":
        return f"### ❓ `{name}` — Unknown status: {status}\n- Image: `{image_raw}`\n"

    current = update_check.get("current_tag", "?")
    latest = update_check.get("latest_tag", "?")
    bump = update_check.get("bump_type", "unknown")
    days_behind = update_check.get("days_behind")
    source_url = update_check.get("source_url", "")
    gh_repo = changelog.get("repo", "")

    risk_label, risk_reason = assess_risk(container)
    changelog_summary = summarize_changelog(changelog, bump)

    days_str = f" · {days_behind}d old" if days_behind is not None else ""
    bump_str = f" · `{bump}` bump" if bump != "unknown" else ""

    lines = [
        f"### {risk_label} `{name}`",
        f"- **Image:** `{image_raw}`",
        f"- **Update:** `{current}` → `{latest}`{bump_str}{days_str}",
        f"- **Risk:** {risk_reason}",
    ]

    if source_url or gh_repo:
        url = source_url or f"https://github.com/{gh_repo}"
        lines.append(f"- **Source:** <{url}>")

    lines.append("")
    lines.append("**Changelog:**")
    lines.append(changelog_summary)

    return "\n".join(lines)


def main():
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1]) as f:
                data = json.load(f)
        except Exception as e:
            print(f"# Container Update Report\n\n**Error:** Could not read input: {e}")
            sys.exit(1)
    else:
        try:
            data = json.load(sys.stdin)
        except Exception as e:
            print(f"# Container Update Report\n\n**Error:** Could not parse stdin: {e}")
            sys.exit(1)

    if "error" in data and data["error"]:
        print(f"# Container Update Report\n\n**Error:** {data['error']}")
        sys.exit(1)

    results = data.get("results", [])
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Separate containers by status
    needs_review = []
    safe_to_update = []
    up_to_date = []
    skipped = []

    for c in results:
        status = c.get("update_check", {}).get("status", "unknown")
        if status == "up_to_date":
            up_to_date.append(c)
        elif status == "update_available":
            risk, _ = assess_risk(c)
            if "review" in risk:
                needs_review.append(c)
            else:
                safe_to_update.append(c)
        else:
            skipped.append(c)

    total_updates = len(needs_review) + len(safe_to_update)

    lines = [
        "# 🐳 Container Update Report",
        f"_Generated: {now}_",
        "",
        "## Summary",
        f"- **Total containers checked:** {len(results)}",
        f"- **Updates available:** {total_updates}",
        f"  - 🔴 Review first: {len(needs_review)}",
        f"  - 🟢 Safe to update: {len(safe_to_update)}",
        f"- **Up to date:** {len(up_to_date)}",
        f"- **Skipped / unknown:** {len(skipped)}",
        "",
    ]

    if not results:
        lines.append("_No containers found._")
        print("\n".join(lines))
        return

    if needs_review:
        lines.append("---")
        lines.append("")
        lines.append("## 🔴 Review First")
        lines.append("_These containers have updates that may include breaking changes._")
        lines.append("")
        for c in needs_review:
            lines.append(format_container_section(c))
            lines.append("")

    if safe_to_update:
        lines.append("---")
        lines.append("")
        lines.append("## 🟢 Safe to Update")
        lines.append("_Patch-level updates with no detected breaking changes._")
        lines.append("")
        for c in safe_to_update:
            lines.append(format_container_section(c))
            lines.append("")

    if up_to_date:
        lines.append("---")
        lines.append("")
        lines.append("## ✅ Up to Date")
        lines.append("")
        for c in up_to_date:
            lines.append(format_container_section(c))

    if skipped:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## ⚪ Skipped")
        lines.append("_Containers skipped due to digest pinning, private images, or unsupported registries._")
        lines.append("")
        for c in skipped:
            lines.append(format_container_section(c))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
