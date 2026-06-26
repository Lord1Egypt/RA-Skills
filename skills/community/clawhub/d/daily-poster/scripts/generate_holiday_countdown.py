#!/usr/bin/env python3
"""Generate reusable holiday countdown JSON for the poster renderer."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from holiday_countdown import build_payload, parse_base_date


def parse_args() -> argparse.Namespace:
    root_dir = Path(__file__).resolve().parents[1]
    default_output = root_dir / "references" / "holiday-countdown-2026.json"
    parser = argparse.ArgumentParser(description="Generate a reusable holiday countdown JSON file for 2026.")
    parser.add_argument("--base-date", default="today", help='Preview date in YYYY-MM-DD format. Use "today" to preview the current day.')
    parser.add_argument("--limit", type=int, default=4, help="Maximum number of countdown items to keep.")
    parser.add_argument("--title", default="假期倒计时", help="Countdown panel title.")
    parser.add_argument("--output", default=str(default_output), help="Output JSON path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_date = parse_base_date(args.base_date)
    output_path = Path(args.output).resolve()
    payload = build_payload(base_date, title=args.title, limit=args.limit)
    payload["metadata"]["generated_at"] = datetime.now().isoformat(timespec="seconds")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated holiday countdown JSON: {output_path}")


if __name__ == "__main__":
    main()
