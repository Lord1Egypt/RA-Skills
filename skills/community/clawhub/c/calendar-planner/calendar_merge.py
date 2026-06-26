#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path


TITLE_KEYS = ("title", "summary", "subject", "name")
CALENDAR_KEYS = ("calendar", "calendarName", "calendar_id", "container")
SOURCE_KEYS = ("source", "provider", "service", "adapter")


def load_events(path: Path):
    payload = json.loads(path.read_text())
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("events", "items", "value", "data"):
            if isinstance(payload.get(key), list):
                return payload[key]
    raise ValueError(f"{path} does not contain a supported event list")


def pick(raw, keys, default=""):
    for key in keys:
        value = raw.get(key)
        if value not in (None, ""):
            return value
    return default


def coerce_time(value):
    if isinstance(value, dict):
        if value.get("dateTime"):
            return value["dateTime"]
        if value.get("date"):
            return value["date"]
    return value or ""


def normalize(raw, fallback_source):
    tags = raw.get("tags", [])
    if isinstance(tags, str):
        tags = [part.strip() for part in tags.split(",") if part.strip()]

    return {
        "title": pick(raw, TITLE_KEYS, "Untitled event"),
        "calendar": pick(raw, CALENDAR_KEYS, "unknown"),
        "source": pick(raw, SOURCE_KEYS, fallback_source),
        "start": coerce_time(raw.get("start")),
        "end": coerce_time(raw.get("end")),
        "hard": bool(raw.get("hard", raw.get("isAllDay", False))),
        "status": raw.get("status", raw.get("showAs", "")),
        "location": raw.get("location", ""),
        "notes": raw.get("notes", raw.get("bodyPreview", "")),
        "tags": tags,
    }


def dedupe_key(event):
    return (
        event["title"],
        event["calendar"],
        event["source"],
        event["start"],
        event["end"],
    )


def main():
    parser = argparse.ArgumentParser(
        description="Merge normalized calendar JSON exports into one sorted timeline."
    )
    parser.add_argument("inputs", nargs="+", help="JSON files with event arrays")
    args = parser.parse_args()

    merged = []
    seen = set()

    for raw_path in args.inputs:
        path = Path(raw_path)
        fallback_source = path.stem
        try:
            events = load_events(path)
        except Exception as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

        for raw in events:
            if not isinstance(raw, dict):
                continue
            event = normalize(raw, fallback_source)
            if not event["start"] or not event["end"]:
                continue
            key = dedupe_key(event)
            if key in seen:
                continue
            seen.add(key)
            merged.append(event)

    merged.sort(key=lambda item: (item["start"], item["end"], item["title"]))
    json.dump(merged, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
