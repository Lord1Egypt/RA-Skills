#!/usr/bin/env python3
"""Compute a study plan from explicit JSON input; no network or calendar writes."""

import argparse
import json
import re
import sys
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

VERSION = "1.0.0"
UTC = timezone.utc


def integer(data, key, default, low, high):
    value = data.get(key, default)
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{key} must be an integer from {low} to {high}")
    return value


def instant(value, day, zone):
    if not isinstance(value, str):
        raise ValueError("Times must be HH:MM or ISO 8601 strings")
    if re.fullmatch(r"\d{2}:\d{2}", value):
        parsed = datetime.combine(day, time.fromisoformat(value))
    else:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is not None:
        return parsed.astimezone(UTC)
    candidates = set()
    for fold in (0, 1):
        candidate = parsed.replace(tzinfo=zone, fold=fold).astimezone(UTC)
        if candidate.astimezone(zone).replace(tzinfo=None) == parsed:
            candidates.add(candidate)
    if len(candidates) != 1:
        raise ValueError("Ambiguous or nonexistent local time; supply an explicit UTC offset")
    return candidates.pop()


def plan(data):
    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object")
    day = date.fromisoformat(data["date"])
    zone = ZoneInfo(data["timezone"])
    window = data["window"]
    start, stop = (instant(window[k], day, zone) for k in ("start", "end"))
    if start.astimezone(zone).date() != day:
        raise ValueError("date must match the local date of the study window start")
    if not start < stop <= start + timedelta(hours=36):
        raise ValueError("The study window must be positive and at most 36 elapsed hours")
    block = integer(data, "block_minutes", 45, 15, 180)
    total = integer(data, "total_minutes", block, 15, 720)
    rest = integer(data, "break_minutes", 10, 0, 120)
    buffer = integer(data, "buffer_minutes", 5, 0, 120)
    busy = data.get("busy", [])
    if not isinstance(busy, list) or len(busy) > 200:
        raise ValueError("busy must be a list containing at most 200 intervals")
    intervals = []
    for index, item in enumerate(busy):
        if not isinstance(item, dict):
            raise ValueError("Each busy interval must be an object")
        first, last = (instant(item[k], day, zone) for k in ("start", "end"))
        if last <= first:
            raise ValueError("Each busy interval must end after it starts")
        title = item.get("title", f"Busy interval {index + 1}")
        if not isinstance(title, str) or not title.strip() or len(title) > 120:
            raise ValueError("Busy titles must be nonempty strings of at most 120 characters")
        intervals.append((first, last, title))
    intervals.sort()

    def span(first, last):
        return {
            "start": first.astimezone(zone).isoformat(),
            "end": last.astimezone(zone).isoformat(),
        }

    conflicts = []
    for index, (first, last, title) in enumerate(intervals):
        for later, later_end, later_title in intervals[index + 1 :]:
            if later >= last:
                break
            overlap_start = max(first, later, start)
            overlap_end = min(last, later_end, stop)
            if overlap_start < overlap_end:
                conflicts.append(
                    {"titles": [title, later_title], **span(overlap_start, overlap_end)}
                )
    blocked = []
    padding = timedelta(minutes=buffer)
    for first, last, _ in intervals:
        first, last = max(start, first - padding), min(stop, last + padding)
        if first >= last:
            continue
        if blocked and first <= blocked[-1][1]:
            blocked[-1] = (blocked[-1][0], max(last, blocked[-1][1]))
        else:
            blocked.append((first, last))
    gaps, cursor = [], start
    for first, last in blocked:
        if cursor < first:
            gaps.append((cursor, first))
        cursor = max(cursor, last)
    if cursor < stop:
        gaps.append((cursor, stop))

    blocks, remaining = [], total
    earliest_next = start
    for first, last in gaps:
        cursor = max(first, earliest_next)
        while remaining >= 15:
            minutes = min(block, remaining)
            finish = cursor + timedelta(minutes=minutes)
            if finish > last:
                break
            blocks.append({**span(cursor, finish), "minutes": minutes})
            remaining -= minutes
            cursor = finish + timedelta(minutes=rest)
            earliest_next = cursor
    return {
        "skill": "cardinal-study-planner",
        "version": VERSION,
        "date": str(day),
        "timezone": str(zone),
        "requested_minutes": total,
        "scheduled_minutes": total - remaining,
        "unscheduled_minutes": remaining,
        "complete": remaining == 0,
        "block_minutes": block,
        "break_minutes": rest,
        "buffer_minutes": buffer,
        "blocks": blocks,
        "conflicts": conflicts,
        "available_gaps": [span(first, last) for first, last in gaps],
        "calendar_modified": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", required=True, help="Schedule JSON path, or - for standard input"
    )
    args = parser.parse_args()
    try:
        if args.input == "-":
            content = sys.stdin.read(65537)
        else:
            with open(args.input, encoding="utf-8") as handle:
                content = handle.read(65537)
        if len(content.encode("utf-8")) > 65536:
            raise ValueError("Input exceeds 64 KiB")
        result = plan(json.loads(content))
    except (ValueError, TypeError, KeyError, OSError, ZoneInfoNotFoundError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        raise SystemExit(2) from exc
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
