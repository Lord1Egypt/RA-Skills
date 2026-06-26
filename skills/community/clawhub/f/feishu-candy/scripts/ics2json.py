#!/usr/bin/env python3
import os
import json
import argparse
from icalendar import Calendar

import datetime

def parse_trigger(trigger):
    if not trigger:
        return None

    value = trigger.dt

    if isinstance(value, datetime.timedelta):
        total_seconds = int(value.total_seconds())

        sign = "-" if total_seconds < 0 else ""
        seconds = abs(total_seconds)

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if hours > 0:
            return f"{sign}PT{hours}H{minutes}M"
        else:
            return f"{sign}PT{minutes}M"

    elif isinstance(value, datetime.datetime):
        return value.isoformat()

    return str(value)

def parse_ics_file(file_path):
    """解析单个 ICS 文件"""
    with open(file_path, "rb") as f:
        cal = Calendar.from_ical(f.read())

    events = []

    for component in cal.walk():
        if component.name == "VEVENT":
            event = {
                "uid": str(component.get("UID")),
                "summary": str(component.get("SUMMARY")),
                "status": str(component.get("STATUS")),
                "organizer": str(component.get("ORGANIZER")),
                "start": component.get("DTSTART").dt.isoformat() if component.get("DTSTART") else None,
                "end": component.get("DTEND").dt.isoformat() if component.get("DTEND") else None,
            }

            # 解析提醒
            alarms = []
            for sub in component.walk():
                if sub.name == "VALARM":
                    alarms.append({
                        "action": str(sub.get("ACTION")),
                        "trigger": parse_trigger(sub.get("TRIGGER")),
                        "description": str(sub.get("DESCRIPTION")),
                    })

            event["alarms"] = alarms
            events.append(event)

    return events


def process_directory(input_dir, output_file=None, split=False):
    """处理目录中的所有 ICS 文件"""
    all_events = []

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".ics"):
                path = os.path.join(root, file)
                try:
                    events = parse_ics_file(path)

                    if split:
                        out_path = os.path.splitext(path)[0] + ".json"
                        with open(out_path, "w", encoding="utf-8") as f:
                            json.dump(events, f, indent=4, ensure_ascii=False)
                        print(f"[OK] {file} → {out_path}")
                    else:
                        all_events.extend(events)
                        print(f"[OK] Parsed {file}")

                except Exception as e:
                    print(f"[ERROR] Failed to parse {file}: {e}")

    if not split and output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_events, f, indent=4, ensure_ascii=False)
        print(f"\n✅ All events saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert .ics calendar files to JSON"
    )
    parser.add_argument(
        "input_dir",
        help="Directory containing .ics files"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output JSON file (used when not splitting)",
        default="output.json"
    )
    parser.add_argument(
        "--split",
        action="store_true",
        help="Output one JSON per ICS file"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print("❌ Invalid directory")
        return

    process_directory(args.input_dir, args.output, args.split)


if __name__ == "__main__":
    main()
