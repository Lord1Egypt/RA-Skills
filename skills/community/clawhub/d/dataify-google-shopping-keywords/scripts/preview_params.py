#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print Dataify Google Shopping keyword parameter confirmation tables."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


SPIDER_NAME = "google.com"
SPIDER_ID = "google_shopping_by-keywords"
DEFAULT_KEYWORD = "iphone"
DEFAULT_FILE_NAME = "{{TasksID}}"


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except AttributeError:
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preview Dataify Google Shopping keyword parameters.")
    parser.add_argument("--parameters-json", help="JSON object or array for spider_parameters.")
    parser.add_argument("--keyword")
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
        current_keyword = "Provided in spider_parameters"
    else:
        current_keyword = args.keyword or DEFAULT_KEYWORD
        current_parameters = json.dumps(
            [{"keyword": current_keyword}],
            ensure_ascii=False,
            separators=(",", ":"),
        )

    default_parameters = json.dumps(
        [{"keyword": DEFAULT_KEYWORD}],
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
        "Yes | JSON array; include multiple objects to collect multiple keyword sets. |"
    )
    print("| spider_errors | true | true | Yes | Include spider error details. |")
    print(f"| file_name | {markdown_escape(args.file_name)} | {DEFAULT_FILE_NAME} | No | Output file name. |")
    print(f"| keyword | {markdown_escape(current_keyword)} | {DEFAULT_KEYWORD} | Yes | Product keyword. |")


def main() -> int:
    configure_stdio()
    args = parse_args()
    print_preview(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
