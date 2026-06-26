#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print Dataify Google Maps review parameter confirmation tables."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


SPIDER_NAME = "google.com"
SPIDER_ID = "google_comment_by-url"
DEFAULT_URL = (
    "https://www.google.com/maps/place/Waterfront+Botanical+Gardens/"
    "@38.2630366,-85.7288454,15z/data=!4m8!3m7!1s0x8869731e16a7bdbd:"
    "0x2f5d238fefed7ca1!8m2!3d38.2632837!4d-85.7239738!9m1!1b1!"
    "16s%2Fg%2F11c709xzzx?hl=en&entry=ttu"
)
DEFAULT_DAYS_LIMIT = "20"
DEFAULT_FILE_NAME = "{{TasksID}}"


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except AttributeError:
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preview Dataify Google Maps review parameters.")
    parser.add_argument("--parameters-json", help="JSON object or array for spider_parameters.")
    parser.add_argument("--url")
    parser.add_argument("--days-limit", dest="days_limit")
    parser.add_argument("--file-name", default=DEFAULT_FILE_NAME)
    parser.add_argument("--spider-id", default=SPIDER_ID)
    return parser.parse_args()


def markdown_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def parse_jsonish(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        if '\\"' in raw:
            return json.loads(raw.replace('\\"', '"'))
        relaxed = re.sub(r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)', r'\1"\2"\3', raw)
        relaxed = re.sub(
            r':\s*([^{}\[\],"\s][^{}\[\],]*)(?=\s*[,}])',
            lambda match: ': "' + match.group(1).strip() + '"',
            relaxed,
        )
        if relaxed != raw:
            return json.loads(relaxed)
        raise


def load_parameter_sets(raw: str | None) -> list[dict[str, Any]] | None:
    if not raw:
        return None
    try:
        data = parse_jsonish(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid --parameters-json: {exc}") from exc
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return data
    raise SystemExit("--parameters-json must be a JSON object or an array of objects.")


def print_preview(args: argparse.Namespace) -> None:
    if args.spider_id != SPIDER_ID:
        raise SystemExit(f"Unsupported --spider-id: {args.spider_id}")

    parameter_sets = load_parameter_sets(args.parameters_json)
    if parameter_sets is not None:
        current_parameters = json.dumps(parameter_sets, ensure_ascii=False, separators=(",", ":"))
        current_url = "Provided in spider_parameters"
        current_days_limit = "Provided in spider_parameters"
    else:
        current_url = args.url or DEFAULT_URL
        current_days_limit = args.days_limit or DEFAULT_DAYS_LIMIT
        current_parameters = json.dumps(
            [{"url": current_url, "days_limit": str(current_days_limit)}],
            ensure_ascii=False,
            separators=(",", ":"),
        )

    default_parameters = json.dumps(
        [{"url": DEFAULT_URL, "days_limit": DEFAULT_DAYS_LIMIT}],
        ensure_ascii=False,
        separators=(",", ":"),
    )

    print("| Parameter | Current value | Default value | Required | Description |")
    print("|---|---|---|---|---|")
    print(f"| spider_name | {SPIDER_NAME} | {SPIDER_NAME} | Yes | Fixed spider platform name. |")
    print(f"| spider_id | {SPIDER_ID} | {SPIDER_ID} | Yes | Dataify spider identifier. |")
    print(
        "| spider_parameters | "
        f"{markdown_escape(current_parameters)} | "
        f"{markdown_escape(default_parameters)} | "
        "Yes | JSON array; include multiple objects to collect multiple parameter sets. |"
    )
    print("| spider_errors | true | true | Yes | Include spider error details. |")
    print(f"| file_name | {markdown_escape(args.file_name)} | {DEFAULT_FILE_NAME} | No | Output file name. |")
    print(f"| url | {markdown_escape(current_url)} | {markdown_escape(DEFAULT_URL)} | Yes | Google Maps URL. |")
    print(
        f"| days_limit | {markdown_escape(current_days_limit)} | {DEFAULT_DAYS_LIMIT} | "
        "Yes | Number of days back from today to collect Google Maps reviews. |"
    )


def main() -> int:
    configure_stdio()
    args = parse_args()
    print_preview(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
