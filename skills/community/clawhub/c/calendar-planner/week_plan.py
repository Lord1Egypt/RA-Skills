#!/usr/bin/env python3

import argparse
import json
from collections import defaultdict
from datetime import date, datetime, time, timedelta
from pathlib import Path


def parse_dt(value):
    text = value.replace("Z", "+00:00")
    if "T" in text:
        return datetime.fromisoformat(text)
    return datetime.fromisoformat(text + "T00:00:00")


def load_events(path):
    payload = json.loads(Path(path).read_text())
    events = []
    for item in payload:
        item["_start"] = parse_dt(item["start"])
        item["_end"] = parse_dt(item["end"])
        events.append(item)
    return sorted(events, key=lambda entry: (entry["_start"], entry["_end"]))


def largest_gap(events, window_start, window_end):
    cursor = window_start
    best = timedelta()
    for event in events:
        start = max(event["_start"], window_start)
        end = min(event["_end"], window_end)
        if start > cursor and start - cursor > best:
            best = start - cursor
        if end > cursor:
            cursor = end
    if window_end > cursor and window_end - cursor > best:
        best = window_end - cursor
    return best


def main():
    parser = argparse.ArgumentParser(
        description="Create a weekly planning summary from merged normalized calendar JSON."
    )
    parser.add_argument("input", help="Merged JSON file from calendar_merge.py")
    parser.add_argument("--start", required=True, help="Week start date in YYYY-MM-DD")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--day-start", default="08:00")
    parser.add_argument("--day-end", default="18:00")
    args = parser.parse_args()

    week_start = date.fromisoformat(args.start)
    week_end = week_start + timedelta(days=args.days)
    day_start = time.fromisoformat(args.day_start)
    day_end = time.fromisoformat(args.day_end)

    events = load_events(args.input)
    by_day = defaultdict(list)
    for event in events:
        if week_start <= event["_start"].date() < week_end:
            by_day[event["_start"].date().isoformat()].append(event)

    print("# Weekly Plan Summary")
    print()
    print(f"- Window: {week_start.isoformat()} to {(week_end - timedelta(days=1)).isoformat()}")
    print(f"- Days with events: {len(by_day)}")
    print()

    for offset in range(args.days):
        current_day = week_start + timedelta(days=offset)
        key = current_day.isoformat()
        day_events = by_day.get(key, [])
        print(f"## {key}")
        if not day_events:
            print("- No scheduled events")
            print("- Best use: reserve a focus block or recovery block")
            print()
            continue

        total_hours = sum(
            (event["_end"] - event["_start"]).total_seconds() / 3600 for event in day_events
        )
        meeting_hours = sum(
            (event["_end"] - event["_start"]).total_seconds() / 3600
            for event in day_events
            if "meeting" in event.get("tags", []) or event.get("hard")
        )
        focus_gap = largest_gap(
            day_events,
            datetime.combine(current_day, day_start, tzinfo=day_events[0]["_start"].tzinfo),
            datetime.combine(current_day, day_end, tzinfo=day_events[0]["_start"].tzinfo),
        )

        print(f"- Events: {len(day_events)}")
        print(f"- Scheduled hours: {total_hours:.1f}")
        print(f"- Hard or meeting hours: {meeting_hours:.1f}")
        print(f"- Longest open block: {int(focus_gap.total_seconds() // 60)} minutes")
        print(f"- First event: `{day_events[0]['title']}` at {day_events[0]['_start'].time()}")
        print(f"- Last event: `{day_events[-1]['title']}` ending at {day_events[-1]['_end'].time()}")
        print()


if __name__ == "__main__":
    main()
