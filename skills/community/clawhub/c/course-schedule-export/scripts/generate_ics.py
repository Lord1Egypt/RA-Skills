#!/usr/bin/env python3
from __future__ import annotations

# Keep this script standard-library-only. The skill may use optional parsers
# during extraction, but the final .ics generation path should not require
# third-party installs.

import argparse
import hashlib
import json
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path


DAY_TO_INDEX = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an .ics file from a normalized schedule manifest.")
    parser.add_argument("manifest", help="Path to schedule manifest JSON")
    parser.add_argument("-o", "--output", help="Output .ics path")
    return parser.parse_args()


def fold_ics_line(line: str) -> str:
    if len(line) <= 75:
        return line
    parts: list[str] = []
    while len(line) > 75:
        parts.append(line[:75])
        line = " " + line[75:]
    parts.append(line)
    return "\r\n".join(parts)


def esc(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", r"\;")
        .replace(",", r"\,")
        .replace("\n", r"\n")
    )


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["calendar_name", "timezone", "slots", "courses"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Missing top-level keys: {', '.join(missing)}")
    if not isinstance(data["courses"], list) or not data["courses"]:
        raise ValueError("'courses' must be a non-empty list")
    return data


def validate_course(course: dict, slots: dict) -> None:
    required = ["name", "location", "slot"]
    missing = [key for key in required if key not in course]
    if missing:
        raise ValueError(f"Course missing keys: {', '.join(missing)} | {course}")
    if course["slot"] not in slots:
        raise ValueError(f"Unknown slot '{course['slot']}' in course {course['name']}")
    mode = course.get("mode")
    if mode is None:
        if "date" in course or "dates" in course:
            mode = "dated"
        elif "day" in course and "weeks" in course:
            mode = "recurring"
        else:
            raise ValueError(f"Cannot infer mode for course {course['name']}: {course}")
    if mode not in {"recurring", "dated"}:
        raise ValueError(f"Invalid mode '{mode}' in course {course['name']}")
    if mode == "recurring":
        if "day" not in course or "weeks" not in course:
            raise ValueError(f"Recurring course missing day/weeks: {course}")
        if course["day"] not in DAY_TO_INDEX:
            raise ValueError(f"Invalid day '{course['day']}' in course {course['name']}")
        weeks = course["weeks"]
        if not isinstance(weeks, list) or not weeks or any((not isinstance(w, int) or w <= 0) for w in weeks):
            raise ValueError(f"Invalid weeks for course {course['name']}: {weeks}")
    else:
        if "date" not in course and "dates" not in course:
            raise ValueError(f"Dated course missing date/dates: {course}")
        if "date" in course:
            date.fromisoformat(course["date"])
        if "dates" in course:
            if not isinstance(course["dates"], list) or not course["dates"]:
                raise ValueError(f"Invalid dates for course {course['name']}: {course['dates']}")
            for explicit_date in course["dates"]:
                date.fromisoformat(explicit_date)


def uid_for(course: dict, start_dt: datetime) -> str:
    mode = course.get("mode")
    if mode is None:
        mode = "dated" if ("date" in course or "dates" in course) else "recurring"
    raw = json.dumps(
        {
            "name": course["name"],
            "location": course["location"],
            "mode": mode,
            "day": course.get("day"),
            "date": course.get("date"),
            "dates": course.get("dates"),
            "slot": course["slot"],
            "start": start_dt.isoformat(),
        },
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return f"{hashlib.sha1(raw).hexdigest()}@local.codex"


def build_event(course: dict, start_dt: datetime, end_dt: datetime, timezone: str) -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    description_lines = []
    teacher = course.get("teacher", "")
    if teacher:
        description_lines.append(f"Teacher: {teacher}")
    mode = course.get("mode")
    if mode is None:
        mode = "dated" if ("date" in course or "dates" in course) else "recurring"
    if mode == "dated":
        if "dates" in course:
            description_lines.append(f"Dates: {','.join(course['dates'])}")
        else:
            description_lines.append(f"Date: {course['date']}")
    else:
        description_lines.append(f"Weeks: {','.join(str(w) for w in course['weeks'])}")
    note = course.get("note", "")
    if note:
        description_lines.append(note)

    fields = [
        "BEGIN:VEVENT",
        f"UID:{uid_for(course, start_dt)}",
        f"DTSTAMP:{stamp}",
        f"DTSTART;TZID={timezone}:{start_dt.strftime('%Y%m%dT%H%M%S')}",
        f"DTEND;TZID={timezone}:{end_dt.strftime('%Y%m%dT%H%M%S')}",
        f"SUMMARY:{esc(course['name'])}",
        f"LOCATION:{esc(course['location'])}",
        f"DESCRIPTION:{esc(chr(10).join(description_lines))}",
        "END:VEVENT",
    ]
    return "\r\n".join(fold_ics_line(field) for field in fields)


def main() -> None:
    args = parse_args()
    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = load_manifest(manifest_path)

    calendar_name = manifest["calendar_name"]
    timezone = manifest["timezone"]
    slots = manifest["slots"]
    needs_week1 = any(
        (course.get("mode") == "recurring")
        or ("mode" not in course and "day" in course and "weeks" in course)
        for course in manifest["courses"]
    )
    week1_monday = None
    if needs_week1:
        if "week1_monday" not in manifest:
            raise ValueError("Manifest needs week1_monday because it contains recurring courses")
        week1_monday = date.fromisoformat(manifest["week1_monday"])
        if week1_monday.weekday() != 0:
            raise ValueError(f"week1_monday must be a Monday, got {week1_monday.isoformat()}")

    events: list[str] = []
    for course in manifest["courses"]:
        validate_course(course, slots)
        slot = slots[course["slot"]]
        start_clock = time.fromisoformat(slot["start"])
        end_clock = time.fromisoformat(slot["end"])
        mode = course.get("mode")
        if mode is None:
            mode = "dated" if ("date" in course or "dates" in course) else "recurring"
        if mode == "dated":
            if "dates" in course:
                event_dates = [date.fromisoformat(explicit_date) for explicit_date in course["dates"]]
            else:
                event_dates = [date.fromisoformat(course["date"])]
        else:
            day_offset = DAY_TO_INDEX[course["day"]]
            event_dates = [
                week1_monday + timedelta(days=(week - 1) * 7 + day_offset)
                for week in sorted(set(course["weeks"]))
            ]
        for event_date in event_dates:
            start_dt = datetime.combine(event_date, start_clock)
            end_dt = datetime.combine(event_date, end_clock)
            events.append(build_event(course, start_dt, end_dt, timezone))

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{esc(calendar_name)}",
        f"X-WR-TIMEZONE:{timezone}",
        *events,
        "END:VCALENDAR",
        "",
    ]

    output = Path(args.output).expanduser().resolve() if args.output else manifest_path.with_suffix(".ics")
    output.write_text("\r\n".join(lines), encoding="utf-8")
    print(output)
    print(f"events={len(events)}")


if __name__ == "__main__":
    main()
