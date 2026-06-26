#!/usr/bin/env python3
"""
fitness-status — View workout history, summaries, and export reports.

Usage:
    fitness-status                  Last 7 entries (compact)
    fitness-status --week           Weekly summary with stats
    fitness-status --month          Monthly summary with stats
    fitness-status --days 14        Custom period summary
    fitness-status --all            All entries (capped at 50)
    fitness-status --export         Export last 30 days as Markdown file
    fitness-status --export 60      Export last 60 days
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fitness_skill import FitnessSkill

MAX_DISPLAY = 50


def print_entries(entries: list, limit: int = MAX_DISPLAY):
    if not entries:
        print("No workouts logged yet. Use `fitness-log` to record one.")
        return

    shown = entries[-limit:] if len(entries) > limit else entries
    truncated = len(entries) - len(shown)
    if truncated > 0:
        print(f"  ({truncated} older entries omitted, use --export for full report)\n")

    for e in shown:
        ex_str = ""
        if e.get("exercises"):
            names = [x["name"] for x in e["exercises"][:4]]
            if len(e["exercises"]) > 4:
                names.append(f"+{len(e['exercises'])-4} more")
            ex_str = ", ".join(names)
        feel = f"  [{e['feeling']}]" if e.get("feeling") else ""
        dur = f"{e.get('duration_min', 0):3d} min" if e.get("duration_min") else "  ? min"
        session_tag = "  [session]" if e.get("session_meta") else ""
        print(f"  {e['date']}  {e.get('type','other'):8s}  {dur}  {ex_str}{feel}{session_tag}")


def print_summary(summary: dict):
    label = summary.get("period", "?")
    print(f"=== Summary ({label}) ===\n")
    print(f"  Sessions:      {summary['sessions']}")
    print(f"  Total time:    {summary['total_minutes']} min")
    print(f"  Avg / session: {summary['avg_minutes_per_session']} min")
    if summary["type_breakdown"]:
        breakdown = ", ".join(f"{k}: {v}" for k, v in summary["type_breakdown"].items())
        print(f"  Breakdown:     {breakdown}")
    if summary["recovery_advice"]:
        print(f"\n  {summary['recovery_advice']}")
    else:
        print("\n  Looking good — keep it up!")


def main():
    skill = FitnessSkill()
    args = sys.argv[1:]

    if args and args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return

    if "--export" in args:
        idx = args.index("--export")
        days = 30
        if idx + 1 < len(args) and args[idx + 1].isdigit():
            days = int(args[idx + 1])
        path = skill.export_to_file(days=days)
        print(f"Exported to: {path}")
        return

    if "--month" in args:
        print_summary(skill.monthly_summary())
        return

    if "--days" in args:
        idx = args.index("--days")
        days = int(args[idx + 1]) if idx + 1 < len(args) and args[idx + 1].isdigit() else 30
        print_summary(skill._period_summary(days))
        return

    if "--week" in args:
        print_summary(skill.weekly_summary())
        return

    if "--all" in args:
        print("=== All Workout Entries ===\n")
        print_entries(skill.log.get("entries", []), limit=MAX_DISPLAY)
        return

    print("=== Recent Workouts (last 7) ===\n")
    print_entries(skill.get_recent_entries(7))


if __name__ == "__main__":
    main()
