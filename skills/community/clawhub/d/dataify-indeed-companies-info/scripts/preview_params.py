#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print Dataify Indeed company info parameter confirmation tables."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

from indeed_options import INDUSTRY_OPTIONS, STATE_OPTIONS


SPIDERS = {
    "company-list-url": {
        "id": "indeed_companies-info_by-company-list-url",
        "fields": [
            ("company_list_url", "Indeed company list URL", True, "https://www.indeed.com/companies/browse-companies"),
        ],
    },
    "keyword": {
        "id": "indeed_companies-info_by-keyword",
        "fields": [
            ("keyword", "Company keyword", True, "openai"),
        ],
    },
    "industry-and-state": {
        "id": "indeed_companies-info_by-industry-and-state",
        "fields": [
            ("industry", "Indeed industry dropdown value", True, "All"),
            ("state", "Indeed region/state dropdown value", False, "United States"),
        ],
    },
    "company-url": {
        "id": "indeed_companies-info_by-company-url",
        "fields": [
            ("company_url", "Indeed company URL", True, "https://www.indeed.com/cmp/Allstate-Insurance"),
        ],
    },
}

ALIASES = {
    "indeed_companies-info_by-company-list-url": "company-list-url",
    "indeed_companies-info_by-keyword": "keyword",
    "indeed_companies-info_by-industry-and-state": "industry-and-state",
    "indeed_companies-info_by-company-url": "company-url",
}


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except AttributeError:
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preview Dataify Indeed company info parameters.")
    parser.add_argument("--tool", choices=sorted(SPIDERS), help="Collection mode.")
    parser.add_argument("--spider-id", help="Full Dataify spider ID. Alternative to --tool.")
    parser.add_argument("--parameters-json", help="JSON object or array for spider_parameters.")
    parser.add_argument("--dropdown", choices=("industry", "state"), help="Print dropdown options as a Markdown table.")
    parser.add_argument("--company-list-url", dest="company_list_url")
    parser.add_argument("--keyword")
    parser.add_argument("--industry")
    parser.add_argument("--state")
    parser.add_argument("--company-url", dest="company_url")
    parser.add_argument("--file-name", default="{{TasksID}}")
    return parser.parse_args()


def markdown_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def normalize_tool(args: argparse.Namespace) -> str:
    if args.tool:
        return args.tool
    if args.spider_id:
        tool = ALIASES.get(args.spider_id)
        if tool:
            return tool
    raise SystemExit("Provide --tool or a supported --spider-id.")


def parse_jsonish(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        if '\\"' in raw:
            return json.loads(raw.replace('\\"', '"'))
        relaxed = re.sub(r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)', r'\1"\2"\3', raw)
        relaxed = re.sub(r':\s*([^{}\[\],"\s][^{}\[\],]*)(?=\s*[,}])', lambda m: ': "' + m.group(1).strip() + '"', relaxed)
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


def current_values_from_args(args: argparse.Namespace, fields: list[tuple[str, str, bool, str]]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for name, _description, _required, _default in fields:
        value = getattr(args, name, None)
        if value is not None:
            values[name] = value
    return values


def print_dropdown(name: str) -> None:
    options = INDUSTRY_OPTIONS if name == "industry" else STATE_OPTIONS
    print(f"### {name} options")
    print("| Label | Value |")
    print("|---|---|")
    for option in options:
        escaped = markdown_escape(option)
        print(f"| {escaped} | {escaped} |")


def print_preview(args: argparse.Namespace) -> None:
    tool = normalize_tool(args)
    spider = SPIDERS[tool]
    fields = spider["fields"]
    parameter_sets = load_parameter_sets(args.parameters_json)
    arg_values = current_values_from_args(args, fields)

    print("| Parameter | Current value | Default value | Required | Description |")
    print("|---|---|---|---|---|")
    print(f"| spider_name | indeed.com | indeed.com | Yes | Fixed spider platform name. |")
    print(f"| spider_id | {spider['id']} | {spider['id']} | Yes | Dataify spider identifier. |")

    if parameter_sets is not None:
        current_parameters = json.dumps(parameter_sets, ensure_ascii=False, separators=(",", ":"))
    else:
        merged = {}
        for name, _description, _required, default in fields:
            merged[name] = arg_values.get(name, default)
        current_parameters = json.dumps([merged], ensure_ascii=False, separators=(",", ":"))

    default_parameters = {
        name: default for name, _description, _required, default in fields
    }
    print(
        "| spider_parameters | "
        f"{markdown_escape(current_parameters)} | "
        f"{markdown_escape(json.dumps([default_parameters], ensure_ascii=False, separators=(',', ':')))} | "
        "Yes | JSON array; include multiple objects to collect multiple parameter sets. |"
    )
    print("| spider_errors | true | true | Yes | Include spider error details. |")
    print(f"| file_name | {markdown_escape(args.file_name)} | {{{{TasksID}}}} | No | Output file name. |")

    for name, description, required, default in fields:
        current = arg_values.get(name)
        if current is None and parameter_sets is None:
            current = default
        elif current is None and parameter_sets is not None:
            current = "Provided in spider_parameters"
        print(
            f"| {name} | {markdown_escape(current)} | {markdown_escape(default)} | "
            f"{'Yes' if required else 'No'} | {markdown_escape(description)} |"
        )


def main() -> int:
    configure_stdio()
    args = parse_args()
    if args.dropdown:
        print_dropdown(args.dropdown)
        return 0
    print_preview(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
