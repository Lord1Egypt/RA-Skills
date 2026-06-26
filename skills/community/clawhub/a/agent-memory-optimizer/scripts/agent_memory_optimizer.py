#!/usr/bin/env python3
"""Archive old daily memory files into month folders.

Default behavior:
- Move memory files older than the current month.
- Source:   <workspace>/memory/*.md
- Target:   <workspace>/memory/archive/YYYY-MM/<filename>
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
from pathlib import Path

DATE_PREFIX = re.compile(r"^(\d{4})-(\d{2})(?:-\d{2})?.*\.md$")


def parse_month(value: str) -> tuple[int, int]:
    try:
        year_str, month_str = value.split("-", 1)
        year = int(year_str)
        month = int(month_str)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Expected YYYY-MM format.") from exc
    if not (1 <= month <= 12):
        raise argparse.ArgumentTypeError("Month must be 01..12.")
    return year, month


def iter_candidates(memory_dir: Path, cutoff: tuple[int, int]) -> list[tuple[Path, str]]:
    cutoff_key = cutoff[0] * 100 + cutoff[1]
    candidates: list[tuple[Path, str]] = []
    for path in sorted(memory_dir.glob("*.md")):
        match = DATE_PREFIX.match(path.name)
        if not match:
            continue
        year = int(match.group(1))
        month = int(match.group(2))
        file_key = year * 100 + month
        if file_key >= cutoff_key:
            continue
        month_folder = f"{year:04d}-{month:02d}"
        candidates.append((path, month_folder))
    return candidates


def archive_files(memory_dir: Path, dry_run: bool, before: tuple[int, int]) -> dict:
    archive_root = memory_dir / "archive"
    candidates = iter_candidates(memory_dir, before)
    moved: list[dict] = []

    for src, month_folder in candidates:
        dst_dir = archive_root / month_folder
        dst = dst_dir / src.name
        moved.append({"from": str(src), "to": str(dst)})
        if dry_run:
            continue
        dst_dir.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            dst.unlink()
        shutil.move(str(src), str(dst))

    return {
        "memory_dir": str(memory_dir),
        "archive_root": str(archive_root),
        "before": f"{before[0]:04d}-{before[1]:02d}",
        "dry_run": dry_run,
        "candidate_count": len(candidates),
        "moved": moved,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive old memory files by month.")
    parser.add_argument(
        "--memory-dir",
        default="~/.openclaw/workspace/memory",
        help="Path to memory directory (default: ~/.openclaw/workspace/memory)",
    )
    parser.add_argument(
        "--before",
        type=parse_month,
        help="Archive months older than this YYYY-MM. Default: current month.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview moves without changing files.",
    )
    args = parser.parse_args()

    memory_dir = Path(args.memory_dir).expanduser().resolve()
    if not memory_dir.exists():
        raise SystemExit(f"Memory directory does not exist: {memory_dir}")
    if not memory_dir.is_dir():
        raise SystemExit(f"Memory path is not a directory: {memory_dir}")
    now = dt.date.today()
    before = args.before or (now.year, now.month)

    result = archive_files(memory_dir=memory_dir, dry_run=args.dry_run, before=before)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
