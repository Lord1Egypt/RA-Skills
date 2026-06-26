#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create Dataify Google Shopping keyword collection tasks."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


API_URL = "https://scraperapi.dataify.com/builder?platform=1"
SPIDER_NAME = "google.com"
SPIDER_ID = "google_shopping_by-keywords"
DEFAULT_KEYWORD = "iphone"
TOKEN_MISSING_MESSAGE = (
    "Missing Dataify API token. Provide a token, or log in/register at "
    "https://dashboard.dataify.com/login?utm_source=skill. If you already have one, open "
    "https://dashboard.dataify.com?utm_source=skill and copy the API TOKEN from the top-right area."
)


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except AttributeError:
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create Dataify Google Shopping keyword collection tasks.")
    parser.add_argument("--parameters-json", help="JSON object or array for spider_parameters.")
    parser.add_argument("--keyword")
    parser.add_argument("--file-name", default="{{TasksID}}")
    parser.add_argument("--spider-id", default=SPIDER_ID)
    parser.add_argument("--spider-errors", default="true")
    parser.add_argument("--token", help="Dataify API token. Bearer prefix is optional.")
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--dry-run", action="store_true", help="Print normalized form data without calling the API.")
    return parser.parse_args()


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


def clean_value(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def build_parameter_sets(args: argparse.Namespace) -> list[dict[str, str]]:
    provided_sets = load_parameter_sets(args.parameters_json)
    if provided_sets is None:
        provided_sets = [{"keyword": clean_value(args.keyword) or DEFAULT_KEYWORD}]

    normalized_sets: list[dict[str, str]] = []
    for item in provided_sets:
        keyword = clean_value(item.get("keyword")) or DEFAULT_KEYWORD
        normalized_sets.append({"keyword": keyword})
    return normalized_sets


def normalize_token(token: str | None) -> str:
    token = clean_value(token) or clean_value(os.environ.get("DATAIFY_API_TOKEN"))
    if not token:
        raise SystemExit(TOKEN_MISSING_MESSAGE)
    if token.lower().startswith("bearer "):
        return token
    return f"Bearer {token}"


def build_form(args: argparse.Namespace) -> dict[str, str]:
    if args.spider_id != SPIDER_ID:
        raise SystemExit(f"Unsupported --spider-id: {args.spider_id}")
    parameter_sets = build_parameter_sets(args)
    return {
        "spider_name": SPIDER_NAME,
        "spider_id": SPIDER_ID,
        "spider_parameters": json.dumps(parameter_sets, ensure_ascii=False, separators=(",", ":")),
        "spider_errors": str(args.spider_errors).lower(),
        "file_name": args.file_name,
    }


def call_api(form: dict[str, str], token: str, timeout: float) -> str:
    encoded = urllib.parse.urlencode(form).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=encoded,
        method="POST",
        headers={
            "Authorization": token,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Request failed: {exc}") from exc


def main() -> int:
    configure_stdio()
    args = parse_args()
    form = build_form(args)
    if args.dry_run:
        print(json.dumps(form, ensure_ascii=False, indent=2))
        return 0
    token = normalize_token(args.token)
    print(call_api(form, token, args.timeout))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
