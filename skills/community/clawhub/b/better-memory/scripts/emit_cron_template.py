#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from memory_os_common import load_settings, sidecar_dir

WEEKDAY_TO_CRON = {
    "SUN": "0",
    "MON": "1",
    "TUE": "2",
    "WED": "3",
    "THU": "4",
    "FRI": "5",
    "SAT": "6",
}


def hhmm_to_pair(raw: str) -> tuple[int, int]:
    hour, minute = raw.split(":")
    return int(hour), int(minute)


def emit_cron_template(workspace: Path) -> Path:
    settings = load_settings(workspace)

    daily_hour, daily_minute = hhmm_to_pair(settings["daily_review_time"])
    weekly_hour, weekly_minute = hhmm_to_pair(settings["weekly_rollup_time"])
    monthly_hour, monthly_minute = hhmm_to_pair(settings["monthly_review_time"])
    weekly_day = WEEKDAY_TO_CRON[settings["weekly_rollup_day"]]

    cron_lines = [
        "# Better Memory V2 cron template",
        "# Review timezone before enabling these lines.",
        f"# workspace={workspace}",
        "",
        "# 1) Catch-up run: every 2 hours, only execute when new L1 entries >= threshold",
        f"{daily_minute} */2 * * * cd {workspace} && python3 skills/better-memory/scripts/run_daily_review.py --workspace . --threshold-only",
        "",
        "# 2) Daily L1 -> L2 review (always run)",
        f"{daily_minute} {daily_hour} * * * cd {workspace} && python3 skills/better-memory/scripts/run_daily_review.py --workspace .",
        "",
        "# 3) Weekly L2 -> L3 rollup",
        f"{weekly_minute} {weekly_hour} * * {weekly_day} cd {workspace} && python3 skills/better-memory/scripts/run_weekly_rollup.py --workspace .",
        "",
        "# 4) Monthly advisory review report (no auto cleanup)",
        f"{monthly_minute} {monthly_hour} {settings['monthly_review_day']} * * cd {workspace} && python3 skills/better-memory/scripts/run_monthly_review.py --workspace .",
        "",
    ]

    output_path = sidecar_dir(workspace) / "cron-template.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(cron_lines), encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit cron template for Better Memory V2.")
    parser.add_argument("--workspace", default=".", help="Workspace path (default: current directory)")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    output_path = emit_cron_template(workspace)

    print(f"Workspace: {workspace}")
    print(f"Cron template: {output_path}")
    print("Generated tasks: catch-up daily, daily review, weekly rollup, monthly review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
