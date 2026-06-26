#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent

from memory_os_common import (
    MANAGED_HEARTBEAT_BLOCK_END,
    MANAGED_HEARTBEAT_BLOCK_START,
    load_settings,
    upsert_marked_block,
)


def render_block(settings: dict) -> str:
    return dedent(
        f"""
        {MANAGED_HEARTBEAT_BLOCK_START}
        ## Better Memory V2

        If there are 3 or more new structured L1 entries since the last daily review, or daily review has not run in 24h:
        1. Run `python3 skills/better-memory/scripts/refine_memory.py --workspace .`
        2. If needed, run `python3 skills/better-memory/scripts/run_weekly_rollup.py --workspace .`.
        3. Check `.openclaw-memory-os/reviews/` for contradiction or stale candidates.
        4. If there is nothing actionable, reply `HEARTBEAT_OK`.

        Monthly hygiene:
        - At least once per month run:
          `python3 skills/better-memory/scripts/run_monthly_review.py --workspace .`
        - Review the generated report with the user before any cleanup edits.
        - If approved, enable actions in monthly plan JSON, then run:
          `python3 skills/better-memory/scripts/apply_monthly_cleanup.py --workspace . --rerollup`

        During heartbeat review, inspect recent raw daily notes for durable signals:
        - experience (how to think/say/do)
        - value (what is good/bad)
        - standard (what is right/wrong)
        If a signal is not represented yet, capture first, then run daily review.

        Respect current settings:
        - `daily_review_time={settings["daily_review_time"]}`
        - `weekly_rollup_day={settings["weekly_rollup_day"]}`
        - `weekly_rollup_time={settings["weekly_rollup_time"]}`
        - `monthly_review_day={settings["monthly_review_day"]}`
        - `monthly_review_time={settings["monthly_review_time"]}`
        - `l1_entry_threshold={settings["l1_entry_threshold"]}`
        - `stale_days={settings["stale_days"]}`

        This heartbeat block is advisory. Do not auto-clean memory on monthly review.
        Do not rewrite non-managed sections of `HEARTBEAT.md`.
        {MANAGED_HEARTBEAT_BLOCK_END}
        """
    ).strip()

def main() -> int:
    parser = argparse.ArgumentParser(description="Install an additive Memory OS block into HEARTBEAT.md.")
    parser.add_argument("--workspace", default=".", help="Workspace path (default: current directory)")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    settings = load_settings(workspace)
    heartbeat_path = workspace / "HEARTBEAT.md"
    original = heartbeat_path.read_text(encoding="utf-8") if heartbeat_path.exists() else "# HEARTBEAT.md\n\n"
    updated = upsert_marked_block(
        original,
        MANAGED_HEARTBEAT_BLOCK_START,
        MANAGED_HEARTBEAT_BLOCK_END,
        render_block(settings),
    )
    heartbeat_path.write_text(updated, encoding="utf-8")

    print(f"Workspace: {workspace}")
    print(f"Updated heartbeat integration: {heartbeat_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
