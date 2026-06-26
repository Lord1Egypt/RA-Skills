#!/usr/bin/env python3
"""
DriftWatch — Agent Identity Drift Monitor
==========================================
Tracks changes to agent identity files in an OpenClaw workspace using git history.
Diffs them across commits, analyzes semantic drift with Claude, and generates
a weekly review report for the human.

Usage:
    python3 driftwatch.py                    # Full report, last 30 days
    python3 driftwatch.py --days 7           # Last 7 days only
    python3 driftwatch.py --since 2026-02-24 # Since a specific date
    python3 driftwatch.py --files SOUL.md    # Single file focus
    python3 driftwatch.py --no-llm           # Skip LLM analysis (faster)
"""

import subprocess
import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ── Configuration ──────────────────────────────────────────────────────────────

WORKSPACE = Path(__file__).parent.parent.parent  # two levels up from nightly/build/

# Files to track — these define who your agents are
TRACKED_FILES = [
    "SOUL.md",
    "IDENTITY.md",
    "USER.md",
    "AGENTS.md",
    "TOOLS.md",
    "agents/jet/MEMORY-INDEX.md",
    "agents/forge/MEMORY-INDEX.md",
    "agents/quill/MEMORY-INDEX.md",
    "agents/scout/MEMORY-INDEX.md",
    "agents/oracle/MEMORY-INDEX.md",
    "agents/atlas/MEMORY-INDEX.md",
    "agents/pixel/MEMORY-INDEX.md",
    "agents/render/MEMORY-INDEX.md",
    "agents/cipher/MEMORY-INDEX.md",
]

# Drift severity thresholds (lines changed)
THRESHOLD_MINOR = 5     # < this: likely formatting / typo fix
THRESHOLD_MODERATE = 20  # < this: meaningful change, worth reviewing
# >= MODERATE: significant drift, flag for mandatory review

OUTPUT_DIR = Path(__file__).parent

# ── Git Helpers ──────────────────────────────────────────────────────────────

def git(cmd: list[str], cwd: Path = WORKSPACE) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git"] + cmd,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def get_commits_for_files(files: list[str], since: str) -> list[dict]:
    """Get all commits that touched any of the tracked files."""
    args = [
        "log",
        f"--since={since}",
        "--format=%H|%ad|%an|%s",
        "--date=iso-strict",
        "--",
    ] + files

    raw = git(args)
    if not raw:
        return []

    commits = []
    for line in raw.splitlines():
        if "|" not in line:
            continue
        parts = line.split("|", 3)
        if len(parts) < 4:
            continue
        commits.append({
            "hash": parts[0],
            "date": parts[1],
            "author": parts[2],
            "message": parts[3],
        })
    return commits


def get_file_diff(file: str, commit_hash: str, parent_hash: Optional[str]) -> dict:
    """Get the diff for a specific file between two commits."""
    if parent_hash is None:
        # First commit — diff against empty
        diff = git(["show", f"{commit_hash}:{file}"])
        lines_added = len(diff.splitlines())
        lines_removed = 0
        raw_diff = f"[NEW FILE — {lines_added} lines]\n{diff}"
    else:
        raw_diff = git(["diff", parent_hash, commit_hash, "--", file])
        if not raw_diff:
            return None

        lines_added = sum(1 for l in raw_diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
        lines_removed = sum(1 for l in raw_diff.splitlines() if l.startswith("-") and not l.startswith("---"))

    total_change = lines_added + lines_removed

    if total_change < THRESHOLD_MINOR:
        severity = "minor"
    elif total_change < THRESHOLD_MODERATE:
        severity = "moderate"
    else:
        severity = "significant"

    return {
        "file": file,
        "lines_added": lines_added,
        "lines_removed": lines_removed,
        "total_change": total_change,
        "severity": severity,
        "diff": raw_diff[:3000],  # Cap at 3k chars for LLM
    }


def get_current_content(file: str) -> str:
    """Get current file content."""
    path = WORKSPACE / file
    if path.exists():
        return path.read_text()
    return ""


def get_historical_content(file: str, commit_hash: str) -> str:
    """Get file content at a specific commit."""
    content = git(["show", f"{commit_hash}:{file}"])
    return content


# ── LLM Analysis ────────────────────────────────────────────────────────────

def analyze_all_changes_with_llm(changes: list[dict]) -> list[dict]:
    """Batch-analyze all changes in a single Claude CLI call. Much faster than per-change calls."""
    if not changes:
        return changes

    # Build a compact batch prompt
    items = []
    for i, c in enumerate(changes):
        diff_snippet = c.get("diff", "")[:800]  # Keep each snippet small
        items.append(f"""CHANGE_{i}:
File: {c['file']}
Commit: {c['message']}
Lines +{c['lines_added']}/-{c['lines_removed']}
Diff snippet:
{diff_snippet}
""")

    batch_text = "\n---\n".join(items)

    prompt = f"""You are a security reviewer analyzing git changes to AI agent identity files.
For each CHANGE below, determine semantic meaning and any concerns.

GUIDELINES:
- feat:/chore:/fix: commits = human-approved (human_approved: true)
- Softening constraints, expanding autonomy, removing deferential language = concern
- Typos/formatting = concern_level: "none"
- Agent self-modification without human intent = human_approved: false

{batch_text}

Respond ONLY with a JSON array of objects, one per CHANGE in order:
[
  {{
    "summary": "1-2 sentence description",
    "category": "personality|behavior_rule|constraint|scope|preference|identity|compliance|autonomy|formatting",
    "human_approved": true,
    "concern_level": "none|low|medium|high",
    "concern_reason": ""
  }},
  ...
]"""

    try:
        result = subprocess.run(
            ["claude", "--print", "--model", "claude-haiku-4-5", prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout.strip()
        import re
        # Find the JSON array
        json_match = re.search(r'\[.*\]', output, re.DOTALL)
        if json_match:
            analyses = json.loads(json_match.group())
            # Merge back into changes
            for i, change in enumerate(changes):
                if i < len(analyses):
                    change["analysis"] = analyses[i]
                else:
                    change["analysis"] = _default_analysis()
            return changes
    except Exception as e:
        print(f"  ⚠️  LLM batch analysis failed: {e}. Using heuristics.")

    # Fallback: heuristic analysis
    for change in changes:
        change["analysis"] = _heuristic_analysis(change)
    return changes


def _default_analysis() -> dict:
    return {"summary": "", "category": "unknown", "human_approved": True, "concern_level": "none", "concern_reason": ""}


def _heuristic_analysis(change: dict) -> dict:
    """Simple heuristic analysis when LLM is unavailable."""
    msg = change.get("message", "").lower()
    diff = change.get("diff", "").lower()

    # Commit message heuristics
    human_prefixes = ("feat:", "fix:", "chore:", "docs:", "refactor:", "hail-mary:", "team:", "agents:")
    human_approved = any(msg.startswith(p) for p in human_prefixes)

    # Drift heuristics
    concern_level = "none"
    concern_reason = ""

    danger_phrases = ["remove constraint", "no longer", "can now", "permission to", "autonomy", "without asking", "on my own"]
    for phrase in danger_phrases:
        if phrase in diff:
            concern_level = "medium"
            concern_reason = f"Diff contains '{phrase}' — may indicate autonomy expansion"
            break

    return {
        "summary": f"Modified {change['file']}: +{change['lines_added']}/-{change['lines_removed']} lines",
        "category": "unknown",
        "human_approved": human_approved,
        "concern_level": concern_level,
        "concern_reason": concern_reason,
    }


# ── Report Generation ─────────────────────────────────────────────────────────

def generate_report(changes: list[dict], since: str, use_llm: bool) -> str:
    """Generate a markdown report from all detected changes."""
    now = datetime.now()
    total_changes = len(changes)
    significant = [c for c in changes if c.get("severity") == "significant"]
    concerns = [c for c in changes if c.get("analysis", {}).get("concern_level") in ("medium", "high")]
    high_concern = [c for c in changes if c.get("analysis", {}).get("concern_level") == "high"]

    # Summary flags
    if high_concern:
        flag = "🔴 REVIEW REQUIRED"
    elif concerns:
        flag = "🟡 CHANGES TO REVIEW"
    elif significant and not use_llm:
        flag = "🟠 SIGNIFICANT CHANGES — run with LLM enabled for semantic analysis"
    elif significant:
        flag = "🟠 SIGNIFICANT CHANGES — reviewed, no concerns flagged"
    else:
        flag = "🟢 ALL CLEAR"

    lines = [
        f"# DriftWatch Identity Report",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')} ACST",
        f"**Period:** {since} → now",
        f"**Status:** {flag}",
        f"",
        f"## Summary",
        f"- **{total_changes}** total changes across identity files",
        f"- **{len(significant)}** significant diffs (≥{THRESHOLD_MODERATE} lines)",
        f"- **{len(concerns)}** flagged for review" + (" ← human attention needed" if concerns else ""),
        f"",
    ]

    if not changes:
        lines += [
            "No changes detected in tracked identity files during this period.",
            "Your agents' identities are stable. ✓",
        ]
        return "\n".join(lines)

    lines += ["## Changes by File", ""]

    # Group by file
    by_file = {}
    for c in changes:
        f = c["file"]
        by_file.setdefault(f, []).append(c)

    for file, file_changes in sorted(by_file.items()):
        total_lines = sum(c["total_change"] for c in file_changes)
        lines += [f"### `{file}` — {len(file_changes)} commits, {total_lines} lines changed", ""]

        for change in file_changes:
            analysis = change.get("analysis", {})
            concern = analysis.get("concern_level", "none")
            concern_icon = {"none": "✓", "low": "💛", "medium": "🟡", "high": "🔴"}.get(concern, "?")
            approved_icon = "👤" if analysis.get("human_approved", True) else "🤖"

            lines += [
                f"**{change['date'][:10]}** — `{change['commit'][:8]}` {concern_icon} {approved_icon}",
                f"_{change['message']}_",
                f"+{change['lines_added']} / -{change['lines_removed']} lines ({change['severity']})",
            ]

            if analysis.get("summary"):
                lines.append(f"> {analysis['summary']}")

            if analysis.get("concern_reason"):
                lines.append(f"> ⚠️ **{analysis['concern_reason']}**")

            if analysis.get("category"):
                lines.append(f"> Category: `{analysis['category']}`")

            lines.append("")

    # Diff appendix for significant changes
    sig_with_diffs = [c for c in changes if c.get("severity") == "significant" and c.get("raw_diff")]
    if sig_with_diffs:
        lines += ["---", "## Significant Diffs (for manual review)", ""]
        for c in sig_with_diffs[:3]:  # Cap at 3 to keep report readable
            lines += [
                f"### `{c['file']}` @ {c['commit'][:8]} ({c['date'][:10]})",
                "```diff",
                c["raw_diff"][:2000],
                "```",
                "",
            ]

    lines += [
        "---",
        "## Legend",
        "- 👤 = likely human-approved change",
        "- 🤖 = possible agent self-modification (review recommended)",
        "- ✓ = no concern | 💛 = low | 🟡 = medium | 🔴 = high concern",
        "",
        "_DriftWatch — keeping agents honest since 2026-03-06_",
    ]

    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="DriftWatch — Agent Identity Drift Monitor")
    parser.add_argument("--days", type=int, default=30, help="Look back N days (default: 30)")
    parser.add_argument("--since", type=str, help="Look back since date (YYYY-MM-DD), overrides --days")
    parser.add_argument("--files", nargs="+", help="Specific files to track (overrides defaults)")
    parser.add_argument("--no-llm", action="store_true", help="Skip LLM semantic analysis")
    parser.add_argument("--output", type=str, help="Output file path (default: auto-named)")
    parser.add_argument("--json", action="store_true", help="Also output JSON data file")
    parser.add_argument("--cron", action="store_true", help="Silent mode: only output report path if concerns found (for cron use)")
    args = parser.parse_args()

    use_llm = not args.no_llm
    cron_mode = args.cron
    if cron_mode:
        use_llm = True  # Always use LLM in cron mode for accurate analysis
    tracked = args.files or TRACKED_FILES

    if args.since:
        since = args.since
    else:
        since_date = datetime.now() - timedelta(days=args.days)
        since = since_date.strftime("%Y-%m-%d")

    if not cron_mode:
        print(f"🔍 DriftWatch scanning from {since} → now")
    print(f"📁 Workspace: {WORKSPACE}")
    print(f"📋 Tracking {len(tracked)} files")
    print(f"🤖 LLM analysis: {'enabled' if use_llm else 'disabled'}")
    print()

    # Get all commits touching tracked files
    commits = get_commits_for_files(tracked, since)
    print(f"Found {len(commits)} commits touching identity files")

    if not commits:
        print("No changes detected. Your agents are stable.")
        report = generate_report([], since, use_llm)
        out_path = OUTPUT_DIR / f"drift-report-{datetime.now().strftime('%Y-%m-%d')}.md"
        out_path.write_text(report)
        print(f"\n📄 Report written to: {out_path}")
        return

    # For each commit, find which tracked files changed
    all_changes = []

    for i, commit in enumerate(commits):
        hash_ = commit["hash"]
        # Get parent commit
        parent = git(["log", "--pretty=%P", "-n1", hash_]).split()[0] if git(["log", "--pretty=%P", "-n1", hash_]) else None

        # Find which tracked files changed in this commit
        changed_in_commit = git(["diff", "--name-only", f"{parent}..{hash_}" if parent else hash_]).splitlines()

        for file in tracked:
            if file in changed_in_commit:
                diff_info = get_file_diff(file, hash_, parent)
                if diff_info:
                    entry = {
                        "file": file,
                        "commit": hash_,
                        "date": commit["date"],
                        "message": commit["message"],
                        "author": commit["author"],
                        **diff_info,
                        "raw_diff": diff_info.get("diff", ""),
                    }

                    entry["analysis"] = _default_analysis()
                    all_changes.append(entry)

    print(f"\n📊 Found {len(all_changes)} file-level changes")

    # Batch LLM analysis (single call for all changes)
    if use_llm and all_changes:
        print(f"  🧠 Running batch LLM analysis ({len(all_changes)} changes in one call)...")
        all_changes = analyze_all_changes_with_llm(all_changes)
    else:
        # Heuristic fallback for each change
        for change in all_changes:
            change["analysis"] = _heuristic_analysis(change)

    # Generate report
    report = generate_report(all_changes, since, use_llm)

    # Write report
    out_name = f"drift-report-{datetime.now().strftime('%Y-%m-%d')}.md"
    out_path = OUTPUT_DIR / (args.output or out_name)
    out_path.write_text(report)
    print(f"\n📄 Report: {out_path}")

    # Write JSON if requested
    if args.json:
        json_path = out_path.with_suffix(".json")
        # Make JSON serializable
        safe = []
        for c in all_changes:
            safe.append({k: v for k, v in c.items() if k != "raw_diff"})
        json_path.write_text(json.dumps({"since": since, "changes": safe}, indent=2))
        if not cron_mode:
            print(f"📊 JSON: {json_path}")

    # In cron mode: only output if there are concerns
    if cron_mode:
        concerns = [c for c in all_changes if c.get("analysis", {}).get("concern_level") in ("medium", "high")]
        if concerns:
            print(f"⚠️ DriftWatch: {len(concerns)} identity concerns detected → {out_path}")
            for c in concerns:
                print(f"  [{c['analysis']['concern_level'].upper()}] {c['file']}: {c['analysis'].get('concern_reason', '')}")
        # Silent exit if no concerns
        return

    # Print quick summary
    concerns = [c for c in all_changes if c.get("analysis", {}).get("concern_level") in ("medium", "high")]
    high = [c for c in all_changes if c.get("analysis", {}).get("concern_level") == "high"]
    self_mods = [c for c in all_changes if not c.get("analysis", {}).get("human_approved", True)]

    print("\n" + "="*50)
    print("DRIFT SUMMARY")
    print("="*50)
    print(f"  Total changes: {len(all_changes)}")
    print(f"  Flagged (medium+): {len(concerns)}")
    print(f"  High concern: {len(high)}")
    print(f"  Possible self-modifications: {len(self_mods)}")

    if high:
        print("\n🔴 HIGH CONCERN ITEMS:")
        for c in high:
            print(f"   {c['file']} @ {c['commit'][:8]}: {c['analysis'].get('concern_reason', 'unknown')}")
    elif concerns:
        print("\n🟡 ITEMS TO REVIEW:")
        for c in concerns:
            print(f"   {c['file']} @ {c['commit'][:8]}: {c['analysis'].get('summary', '')[:80]}")
    else:
        print("\n🟢 No significant concerns. Agents looking stable.")


if __name__ == "__main__":
    main()
