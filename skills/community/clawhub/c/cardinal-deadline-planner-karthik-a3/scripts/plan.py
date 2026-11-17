#!/usr/bin/env python3
"""Portable, dependency-free deadline planner. Original AI-assisted implementation, CSCI 599 A3."""
import json
import sys
from datetime import datetime, timedelta


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Timestamps require timezone offsets")
    return parsed


def plan(data):
    start, end = timestamp(data["window_start"]), min(timestamp(data["window_end"]), timestamp(data["deadline"]))
    minutes = data["minutes"]
    if type(minutes) is not int or not 1 <= minutes <= 480 or start >= end:
        raise ValueError("Use an increasing window before the deadline and integer duration 1–480")
    intervals = []
    for event in data.get("events", []):
        left, right = timestamp(event["start"]), timestamp(event["end"])
        if left >= right:
            raise ValueError("Event end must follow start")
        if left < end and right > start:
            intervals.append((max(start, left), min(end, right), event.get("title", "Untitled")))
    intervals.sort()
    slots, conflicts, cursor = [], [], start
    for i, (left, right, title) in enumerate(intervals):
        for a, b, other in intervals[:i]:
            if a < right and left < b:
                conflicts.append([other, title])
        if left - cursor >= timedelta(minutes=minutes):
            slots.append({"start": cursor.isoformat(), "end": (cursor + timedelta(minutes=minutes)).isoformat()})
        cursor = max(cursor, right)
    if end - cursor >= timedelta(minutes=minutes):
        slots.append({"start": cursor.isoformat(), "end": (cursor + timedelta(minutes=minutes)).isoformat()})
    return {"slots": slots[:3], "conflicts": conflicts}


if __name__ == "__main__":
    try:
        print(json.dumps(plan(json.load(sys.stdin)), indent=2))
    except (ValueError, KeyError, TypeError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        sys.exit(1)
