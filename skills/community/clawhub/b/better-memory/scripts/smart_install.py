#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from bootstrap_memory import bootstrap
from emit_cron_template import emit_cron_template
from memory_os_common import DEFAULT_SETTINGS
from promote_legacy_memory import latest_migration_review, prepare_plan


def main() -> int:
    parser = argparse.ArgumentParser(
        description="One-shot smart install for Better Memory V2 (bootstrap + migration plan + cron template)."
    )
    parser.add_argument("--workspace", default=".", help="Workspace path (default: current directory)")
    parser.add_argument("--stale-days", type=int, default=DEFAULT_SETTINGS["stale_days"])
    parser.add_argument("--max-l3-per-kind", type=int, default=DEFAULT_SETTINGS["max_l3_per_kind"])
    parser.add_argument("--min-evidence-for-l3", type=int, default=DEFAULT_SETTINGS["min_evidence_for_l3"])
    parser.add_argument("--migration-days", type=int, default=DEFAULT_SETTINGS["migration_days"])
    parser.add_argument("--daily-entries-soft-limit", type=int, default=DEFAULT_SETTINGS["daily_entries_soft_limit"])
    parser.add_argument("--daily-time", default=DEFAULT_SETTINGS["daily_review_time"])
    parser.add_argument("--weekly-day", default=DEFAULT_SETTINGS["weekly_rollup_day"])
    parser.add_argument("--weekly-time", default=DEFAULT_SETTINGS["weekly_rollup_time"])
    parser.add_argument("--monthly-day", type=int, default=DEFAULT_SETTINGS["monthly_review_day"])
    parser.add_argument("--monthly-time", default=DEFAULT_SETTINGS["monthly_review_time"])
    parser.add_argument("--entry-threshold", type=int, default=DEFAULT_SETTINGS["l1_entry_threshold"])
    parser.add_argument("--force-migration-plan", action="store_true", help="Overwrite existing migration-plan.json")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    settings = {
        "stale_days": args.stale_days,
        "max_l3_per_kind": args.max_l3_per_kind,
        "min_evidence_for_l3": args.min_evidence_for_l3,
        "migration_days": args.migration_days,
        "daily_entries_soft_limit": args.daily_entries_soft_limit,
        "daily_review_time": args.daily_time.strip(),
        "weekly_rollup_day": args.weekly_day.strip().upper(),
        "weekly_rollup_time": args.weekly_time.strip(),
        "monthly_review_day": args.monthly_day,
        "monthly_review_time": args.monthly_time.strip(),
        "l1_entry_threshold": args.entry_threshold,
    }

    changed = bootstrap(workspace, settings)
    cron_path = emit_cron_template(workspace)

    migration_plan_path = None
    migration_plan_note = None
    review_path = latest_migration_review(workspace)
    if review_path is not None and review_path.exists():
        try:
            migration_plan_path = prepare_plan(workspace, review_path, force=args.force_migration_plan)
        except SystemExit as exc:
            migration_plan_note = str(exc)

    print(f"Workspace: {workspace}")
    print("Smart install completed.")
    print("Changed/created paths:")
    for path in changed:
        print(f"- {path}")
    print(f"Cron template: {cron_path}")
    if migration_plan_path is not None:
        print(f"Migration plan: {migration_plan_path}")
    elif migration_plan_note:
        print(f"Migration plan note: {migration_plan_note}")
    else:
        print("Migration plan: skipped (no migration review found)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
