#!/usr/bin/env python3

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path


def parse_dt(value):
    text = value.replace("Z", "+00:00")
    if "T" in text:
        return datetime.fromisoformat(text)
    return datetime.fromisoformat(text + "T00:00:00")


def load_events(path):
    payload = json.loads(Path(path).read_text())
    return sorted(payload, key=lambda item: (item["start"], item["end"], item["title"]))


def main():
    parser = argparse.ArgumentParser(
        description="Audit normalized calendar JSON for overlaps, short buffers, and overload."
    )
    parser.add_argument("input", help="Merged JSON file from calendar_merge.py")
    parser.add_argument("--buffer-minutes", type=int, default=20)
    parser.add_argument("--max-events-per-day", type=int, default=6)
    parser.add_argument("--overload-hours", type=float, default=8.0)
    args = parser.parse_args()

    events = load_events(args.input)
    by_day = defaultdict(list)
    for event in events:
        event["_start"] = parse_dt(event["start"])
        event["_end"] = parse_dt(event["end"])
        by_day[event["_start"].date().isoformat()].append(event)

    overlap_issues = []
    buffer_issues = []
    overload_issues = []

    for day, day_events in sorted(by_day.items()):
        total_hours = 0.0
        previous = None
        for event in day_events:
            total_hours += (event["_end"] - event["_start"]).total_seconds() / 3600
            if previous and event["_start"] < previous["_end"]:
                overlap_issues.append(
                    f"- {day}: `{previous['title']}` overlaps with `{event['title']}`"
                )
            if previous:
                gap = event["_start"] - previous["_end"]
                if gap < timedelta(minutes=args.buffer_minutes):
                    minutes = int(gap.total_seconds() // 60)
                    buffer_issues.append(
                        f"- {day}: only {minutes}m between `{previous['title']}` and `{event['title']}`"
                    )
            previous = event

        if len(day_events) > args.max_events_per_day or total_hours > args.overload_hours:
            overload_issues.append(
                f"- {day}: {len(day_events)} events, {total_hours:.1f} scheduled hours"
            )

    print("# Calendar Guard Report")
    print()
    print(f"- Days reviewed: {len(by_day)}")
    print(f"- Overlap issues: {len(overlap_issues)}")
    print(f"- Buffer issues (<{args.buffer_minutes}m): {len(buffer_issues)}")
    print(f"- Overloaded days: {len(overload_issues)}")
    print()

    if overlap_issues:
        print("## Overlaps")
        print("\n".join(overlap_issues))
        print()

    if buffer_issues:
        print("## Buffer failures")
        print("\n".join(buffer_issues))
        print()

    if overload_issues:
        print("## Overloaded days")
        print("\n".join(overload_issues))
        print()

    if not any((overlap_issues, buffer_issues, overload_issues)):
        print("No guardrail failures detected.")


if __name__ == "__main__":
    main()
