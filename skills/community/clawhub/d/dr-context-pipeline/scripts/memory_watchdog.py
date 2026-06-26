#!/usr/bin/env python3
"""Memory freshness watchdog for dr-context-pipeline."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List


@dataclass
class CheckResult:
    status: str
    issues: List[str]
    details: dict


def iso_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def find_daily_files(memory_dir: Path, target_date: datetime) -> List[Path]:
    prefix = iso_date(target_date)
    return sorted(memory_dir.glob(f"{prefix}*.md"))


def check_daily_file(paths: List[Path], freshness_minutes: int, min_bytes: int) -> CheckResult:
    issues: List[str] = []
    now = datetime.now(timezone.utc)

    if not paths:
        issues.append("Missing daily log for today")
        return CheckResult("GAP", issues, {"files_checked": []})

    newest = None
    newest_age = None
    details = []
    for p in paths:
        stat = p.stat()
        mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
        age_minutes = (now - mtime).total_seconds() / 60
        size = stat.st_size
        details.append({
            "path": str(p),
            "modified_utc": mtime.isoformat(),
            "age_minutes": round(age_minutes, 2),
            "bytes": size,
        })
        if newest is None or mtime > newest:
            newest = mtime
            newest_age = age_minutes
        if size < min_bytes:
            issues.append(f"File {p} is only {size} bytes (<{min_bytes})")

    if newest_age is not None and newest_age > freshness_minutes:
        issues.append(f"Newest daily note is {round(newest_age, 1)} min old (> {freshness_minutes} min)")

    status = "OK" if not issues else "GAP"
    return CheckResult(status, issues, {"files_checked": details})


def main() -> int:
    script_path = Path(__file__).resolve()
    workspace_root = script_path.parents[3]
    memory_dir_default = workspace_root / "memory"

    parser = argparse.ArgumentParser(description="Ensure memory daily logs are fresh and non-empty")
    parser.add_argument("--memory-dir", default=str(memory_dir_default), help="Path to the memory directory")
    parser.add_argument("--freshness-minutes", type=int, default=120, help="Max minutes since the latest daily log edit")
    parser.add_argument("--min-bytes", type=int, default=200, help="Minimum acceptable size for the daily log")
    parser.add_argument("--timezone", default="UTC", help="Display timezone label (informational only)")
    args = parser.parse_args()

    memory_dir = Path(args.memory_dir).resolve()
    if not memory_dir.exists():
        print(json.dumps({
            "status": "GAP",
            "issues": [f"Memory directory missing: {memory_dir}"],
            "details": {}
        }, indent=2))
        return 1

    today = datetime.now(timezone.utc)
    files = find_daily_files(memory_dir, today)
    result = check_daily_file(files, args.freshness_minutes, args.min_bytes)
    payload = {
        "status": result.status,
        "issues": result.issues,
        "details": result.details,
        "freshness_minutes": args.freshness_minutes,
        "min_bytes": args.min_bytes,
        "timezone": args.timezone,
        "today": iso_date(today),
    }
    print(json.dumps(payload, indent=2))
    return 0 if result.status == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
