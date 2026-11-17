#!/usr/bin/env python3
"""Create a daily note from the bundled template."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = Path(__file__).resolve().parents[1] / "references" / "note-template.md"


def parse_date(value: str) -> dt.date:
    return dt.datetime.strptime(value, "%Y-%m-%d").date()


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a daily note")
    parser.add_argument("date", nargs="?", help="Date in YYYY-MM-DD format")
    parser.add_argument("--root", default=str(ROOT), help="Workspace root")
    args = parser.parse_args()

    note_date = parse_date(args.date) if args.date else dt.date.today()
    memory_dir = Path(args.root) / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    target = memory_dir / f"{note_date.isoformat()}.md"

    if target.exists():
        print(f"exists: {target}")
        return 0

    template = TEMPLATE.read_text(encoding="utf-8")
    target.write_text(template.replace("{{DATE}}", note_date.isoformat()), encoding="utf-8")
    print(f"created: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
