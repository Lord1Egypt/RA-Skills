#!/usr/bin/env python3
"""Generate a safe Markdown report path for Bluetooth earbuds reports.

This helper is optional. The skill can also follow references/export-policy.md manually.
"""

import argparse
import re
from datetime import date
from pathlib import Path


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "report"


def unique_path(path):
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    version = 2
    while True:
        candidate = parent / f"{stem}-v{version}{suffix}"
        if not candidate.exists():
            return candidate
        version += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="reports/earbuds", help="Export folder")
    parser.add_argument("--region", default="unknown-region")
    parser.add_argument("--budget", default=None, help="Example: under-1000-cny or 1000-1800-cny")
    parser.add_argument("--brand", default=None, help="Example: sony or open-market")
    parser.add_argument("--use-case", default="general", help="Example: commuting-calls")
    parser.add_argument("--date", default=date.today().isoformat())
    args = parser.parse_args()

    parts = [args.date, "earbuds", slugify(args.region)]
    if args.brand:
        parts.append(slugify(args.brand))
    if args.budget:
        parts.append(slugify(args.budget))
    if args.use_case:
        parts.append(slugify(args.use_case))

    filename = "-".join(parts) + ".md"
    folder = Path(args.root)
    folder.mkdir(parents=True, exist_ok=True)
    print(unique_path(folder / filename))


if __name__ == "__main__":
    main()
