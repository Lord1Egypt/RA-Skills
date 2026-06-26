#!/usr/bin/env python3
"""Slice FreshRSS unread items by calendar date."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def parse_timezone(value: str) -> timezone:
    if value in {"Asia/Shanghai", "UTC+08:00", "+08:00"}:
        return timezone(timedelta(hours=8))
    if value in {"UTC", "+00:00"}:
        return timezone.utc
    raise SystemExit(f"Unsupported timezone value: {value}")


def resolve_target_date(date_str: str | None, offset_days: int, tz: timezone) -> str:
    if date_str:
        return date_str
    now = datetime.now(tz)
    return (now + timedelta(days=offset_days)).strftime("%Y-%m-%d")


def canonical_link(item: dict[str, Any]) -> str:
    canonical = item.get("canonical") or []
    if canonical and isinstance(canonical, list) and isinstance(canonical[0], dict):
        return canonical[0].get("href", "")
    return ""


def item_source(item: dict[str, Any]) -> str:
    origin = item.get("origin") or {}
    return origin.get("title") or origin.get("streamId") or "Unknown"


def build_markdown(items: list[dict[str, Any]], target_date: str, source_json: str) -> str:
    lines = [
        f"# FreshRSS Slice | {target_date}",
        "",
        f"- source_json: `{source_json}`",
        f"- target_date: `{target_date}`",
        f"- count: `{len(items)}`",
        "",
    ]
    for index, item in enumerate(items, start=1):
        title = item.get("title") or "(Untitled)"
        source = item_source(item)
        link = canonical_link(item)
        published = item.get("published") or ""
        lines.extend(
            [
                f"## {index}. {title}",
                "",
                f"- source: {source}",
                f"- published: {published}",
                f"- link: {link}",
                f"- item_id: {item.get('id', '')}",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Slice FreshRSS unread items by date.")
    parser.add_argument("--source-json", required=True, help="Path to raw FreshRSS JSON.")
    parser.add_argument("--output-json", required=True, help="Path to sliced JSON output.")
    parser.add_argument("--output-md", required=True, help="Path to sliced Markdown output.")
    parser.add_argument("--date", default=None, help="Target date in YYYY-MM-DD.")
    parser.add_argument(
        "--offset-days",
        type=int,
        default=-1,
        help="Offset days from now when --date is omitted. Default: -1 (yesterday).",
    )
    parser.add_argument("--timezone", default="Asia/Shanghai", help="Timezone for date slicing.")
    args = parser.parse_args()

    source_json = Path(args.source_json)
    if not source_json.exists():
        raise SystemExit(f"Source JSON not found: {source_json}")

    tz = parse_timezone(args.timezone)
    target_date = resolve_target_date(args.date, args.offset_days, tz)

    raw = json.loads(source_json.read_text(encoding="utf-8"))
    items = raw.get("items", [])
    if not isinstance(items, list):
        raise SystemExit("Source JSON is missing items list")

    sliced: list[dict[str, Any]] = []
    for item in items:
        ts = item.get("published")
        if not ts:
            continue
        dt = datetime.fromtimestamp(int(ts), tz=timezone.utc).astimezone(tz)
        if dt.strftime("%Y-%m-%d") == target_date:
            sliced.append(item)

    result = {
        "target_date": target_date,
        "timezone": args.timezone,
        "count": len(sliced),
        "items": sliced,
    }

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(build_markdown(sliced, target_date, str(source_json)), encoding="utf-8")

    print(f"target_date={target_date}")
    print(f"count={len(sliced)}")
    print(f"json={output_json}")
    print(f"md={output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
