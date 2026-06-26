#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from refine_memory import run_daily_review


def main() -> int:
    parser = argparse.ArgumentParser(description="Run daily L1 -> L2 memory review.")
    parser.add_argument("--workspace", default=".", help="Workspace path (default: current directory)")
    parser.add_argument("--stale-days", type=int, help="Override stale_days")
    parser.add_argument("--entry-threshold", type=int, help="Override l1_entry_threshold")
    parser.add_argument("--threshold-only", action="store_true", help="Skip if new L1 entries are below threshold")
    parser.add_argument("--apply-stale", action="store_true", help="Mark old active entries as stale in L1")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    result = run_daily_review(
        workspace,
        stale_days=args.stale_days,
        entry_threshold=args.entry_threshold,
        threshold_only=args.threshold_only,
        apply_stale=args.apply_stale,
    )

    print(f"Workspace: {workspace}")
    if not result["executed"]:
        print("Daily review skipped.")
        print(f"Reason: {result['reason']}")
        print(f"New entries: {result['new_entries']}")
        print(f"Entry threshold: {result['entry_threshold']}")
        return 0

    print(f"Daily review executed: {result['executed']}")
    print(f"New entries: {result['new_entries']}")
    print(f"Threshold triggered: {result['threshold_triggered']}")
    print(f"Stale statuses changed: {result['stale_statuses_changed']}")
    print("L2 files:")
    for path in result["l2_files"]:
        print(f"- {path}")
    print(f"Review file: {result['review_file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
