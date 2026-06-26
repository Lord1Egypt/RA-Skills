#!/usr/bin/env python3
"""Score .learnings/LEARNINGS.md entries for retention, archival, or deletion.

Usage:
  python3 scripts/retention_scorer.py [--learnings PATH] [--dry-run]

Reads LEARNINGS.md, scores each entry, and outputs keep/archive/delete decisions.
With --dry-run, prints decisions without modifying files.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path


ENTRY_RE = re.compile(r"^- \[(\d{4}-\d{2}-\d{2})\] \[([^\]]+)\]: (.+)$")
DEFAULT_LEARNINGS = Path(".learnings/LEARNINGS.md")
DEFAULT_ARCHIVE = Path(".learnings/ARCHIVE.md")


@dataclass
class ScoredEntry:
    line: str
    entry_date: date
    category: str
    takeaway: str
    score: int
    action: str  # "keep", "archive", "delete"


def parse_date(s: str) -> date:
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d))


def score_entry(
    entry_date: date,
    category: str,
    takeaway: str,
    today: date | None = None,
    active_categories: set[str] | None = None,
    category_counts: dict[str, int] | None = None,
) -> int:
    today = today or date.today()
    active_categories = active_categories or set()
    category_counts = category_counts or {}
    score = 0

    age_days = (today - entry_date).days

    # Referenced or applied in last 30 days (heuristic: recent entries)
    if age_days <= 30:
        score += 3

    # Matches active project context
    if category in active_categories:
        score += 2

    # Direct correction from Omar
    if category.lower() == "correction":
        score += 2

    # Has prevented a repeat error (heuristic: category appears 2+ times)
    if category_counts.get(category, 0) >= 2:
        score += 3

    # Env/config still valid (heuristic: env entries get +1)
    if category.lower() == "env":
        score += 1

    # Superseded check would need content comparison — skip for now

    # Old and likely stale
    if age_days > 90:
        score -= 3

    return score


def classify(score: int) -> str:
    if score >= 2:
        return "keep"
    if score >= 0:
        return "archive"
    return "delete"


def score_file(
    learnings_path: Path,
    today: date | None = None,
    active_categories: set[str] | None = None,
) -> list[ScoredEntry]:
    today = today or date.today()
    lines = learnings_path.read_text().splitlines()

    # First pass: count categories
    category_counts: dict[str, int] = {}
    entries_raw: list[tuple[str, date, str, str]] = []
    for line in lines:
        m = ENTRY_RE.match(line.strip())
        if m:
            d = parse_date(m.group(1))
            cat = m.group(2)
            take = m.group(3)
            category_counts[cat] = category_counts.get(cat, 0) + 1
            entries_raw.append((line, d, cat, take))

    # Second pass: score
    results: list[ScoredEntry] = []
    for raw_line, entry_date, category, takeaway in entries_raw:
        s = score_entry(
            entry_date,
            category,
            takeaway,
            today=today,
            active_categories=active_categories,
            category_counts=category_counts,
        )
        results.append(ScoredEntry(
            line=raw_line,
            entry_date=entry_date,
            category=category,
            takeaway=takeaway,
            score=s,
            action=classify(s),
        ))

    return results


def apply_decisions(
    learnings_path: Path,
    archive_path: Path,
    scored: list[ScoredEntry],
    dry_run: bool = False,
) -> dict[str, int]:
    keep_lines: list[str] = []
    archive_lines: list[str] = []
    counts = {"keep": 0, "archive": 0, "delete": 0}

    # Preserve header lines from learnings file
    original = learnings_path.read_text().splitlines()
    header_lines = [line for line in original if not ENTRY_RE.match(line.strip())]

    for entry in scored:
        counts[entry.action] += 1
        if entry.action == "keep":
            keep_lines.append(entry.line)
        elif entry.action == "archive":
            archive_lines.append(entry.line)
        # "delete" entries are simply dropped

    if dry_run:
        return counts

    # Write back learnings
    learnings_path.write_text("\n".join(header_lines + keep_lines) + "\n")

    # Append to archive
    if archive_lines:
        existing_archive = archive_path.read_text() if archive_path.exists() else "# ARCHIVE.md — Scored-out learnings\n"
        archive_path.write_text(existing_archive.rstrip() + "\n" + "\n".join(archive_lines) + "\n")

    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Score learnings for retention")
    parser.add_argument("--learnings", type=Path, default=DEFAULT_LEARNINGS)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.learnings.exists():
        print(f"No file at {args.learnings}")
        return

    scored = score_file(args.learnings)
    for entry in scored:
        print(f"[{entry.action:>7}] (score={entry.score:>3}) {entry.line.strip()[:80]}")

    counts = apply_decisions(args.learnings, args.archive, scored, dry_run=args.dry_run)
    print(f"\nResult: keep={counts['keep']} archive={counts['archive']} delete={counts['delete']}")
    if args.dry_run:
        print("(dry run — no files changed)")


if __name__ == "__main__":
    main()
