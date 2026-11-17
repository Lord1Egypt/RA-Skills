#!/usr/bin/env python3
"""Content Calendar Planner

Builds a {horizon}-day weekly plan for content calendar planner.

Parameters for this build:
{
  "horizon_days": 90,
  "cadence": "weekly"
}

Usage:
    python3 content_calendar_planner.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Content Calendar Planner"


def read_flat(path):
    """Read a small YAML-ish file: `key: value`, `- item` lists, '#' comments."""
    data, key = {}, None
    try:
        raw = open(path, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        raise SystemExit(f"cannot read {path}: {exc}")
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            if key is None:
                continue
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(stripped[2:].strip().strip('"').strip("'"))
            continue
        if ":" in stripped:
            name, _, value = stripped.partition(":")
            name, value = name.strip(), value.strip().strip('"').strip("'")
            if value == "":
                data[name] = []
                key = name
            else:
                data[name] = value
                key = None
    return data


def read_csv(path):
    import csv
    with open(path, newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def write_out(out_dir, name, lines):
    import os
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print(f"wrote {path}")
    return path


HORIZON = 90
CADENCE = 'weekly'


def run(input_path, out_dir):
    import datetime
    data = read_flat(input_path)
    start = str(data.get("start_date", "") or "").strip()
    try:
        begin = datetime.date.fromisoformat(start)
    except ValueError:
        begin = datetime.date.today()
    step = 1 if CADENCE == "daily" else (14 if CADENCE == "biweekly" else 7)
    report = [f"# {TITLE} plan", "", f"start: {begin.isoformat()}", f"horizon: {HORIZON} days", f"cadence: {CADENCE}", ""]
    day = 0
    while day <= HORIZON:
        date = begin + datetime.timedelta(days=day)
        report.append(f"- {date.isoformat()} - {data.get('focus', 'session 1') if day == 0 else 'next block'}")
        day += step
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never put a seasonal moment in the plan without checking the date for that year.", "Never plan a sponsored slot without the disclosure line written into the slot.", "Never fill a slot with a statistic or a claim that has no source."]:
        report.append(f"- {rule}")
    write_out(out_dir, "plan.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
