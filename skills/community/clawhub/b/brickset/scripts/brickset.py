#!/usr/bin/env python3
"""Brickset API v3 helper CLI.

Reads BRICKSET_API_KEY from:
1. --api-key
2. environment variable BRICKSET_API_KEY
3. workspace .env in current working directory or one of its parents

Default output is JSON. Use --format text for human-readable summaries.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = "https://brickset.com/api/v3.asmx"


def load_dotenv(start: Path | None = None) -> dict[str, str]:
    start = (start or Path.cwd()).resolve()
    candidates = [start, *start.parents]
    for directory in candidates:
        env_path = directory / ".env"
        if env_path.exists():
            values: dict[str, str] = {}
            for raw_line in env_path.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip().strip('"').strip("'")
            return values
    return {}


def resolve_api_key(explicit: str | None) -> str:
    if explicit:
        return explicit
    if os.getenv("BRICKSET_API_KEY"):
        return os.environ["BRICKSET_API_KEY"]
    env_values = load_dotenv()
    if env_values.get("BRICKSET_API_KEY"):
        return env_values["BRICKSET_API_KEY"]
    raise SystemExit(
        "BRICKSET_API_KEY is not set. Pass --api-key or add BRICKSET_API_KEY=... to the environment or workspace .env"
    )


def call_api(method: str, api_key: str, extra_params: dict[str, Any] | None = None, post: bool = False) -> dict[str, Any]:
    params: dict[str, Any] = {"apiKey": api_key}
    if extra_params:
        for key, value in extra_params.items():
            if value is None:
                continue
            params[key] = value

    url = f"{API_BASE}/{method}"
    headers = {"Accept": "application/json"}

    try:
        if post:
            body = urlencode(params).encode("utf-8")
            request = Request(url, data=body, headers=headers, method="POST")
        else:
            request = Request(f"{url}?{urlencode(params)}", headers=headers, method="GET")
        with urlopen(request, timeout=60) as response:
            text = response.read().decode("utf-8")
    except HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        return {"status": "http_error", "code": exc.code, "body": text}
    except URLError as exc:
        return {"status": "network_error", "message": str(exc)}

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"status": "decode_error", "body": text}


def parse_params(raw: str | None) -> str | None:
    if raw is None:
        return None
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise SystemExit("--params must decode to a JSON object")
    return json.dumps(parsed, separators=(",", ":"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Brickset API v3 CLI")
    parser.add_argument("--api-key", help="Brickset API key. Defaults to BRICKSET_API_KEY env/.env")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check-key", help="Validate the API key")
    sub.add_parser("usage-stats", help="Fetch 30-day API usage stats")
    sub.add_parser("themes", help="List themes")

    years = sub.add_parser("years", help="List years, optionally filtered by theme")
    years.add_argument("--theme", default="", help="Theme name. Leave blank for all years")

    subthemes = sub.add_parser("subthemes", help="List subthemes for a theme")
    subthemes.add_argument("theme", help="Theme name")

    get_sets = sub.add_parser("get-sets", help="Call getSets with raw JSON params")
    get_sets.add_argument("--params", required=True, help='JSON object string, e.g. {"theme":"Space","pageSize":5}')
    get_sets.add_argument("--user-hash", help="Optional user hash for owned/wanted queries")

    search = sub.add_parser("search", help="Simple set search wrapper")
    search.add_argument("query", help="Search term")
    search.add_argument("--theme")
    search.add_argument("--year")
    search.add_argument("--page-size", type=int, default=10)
    search.add_argument("--page-number", type=int, default=1)
    search.add_argument("--order-by", default="Number")
    search.add_argument("--extended-data", action="store_true")

    instructions = sub.add_parser("instructions2", help="Get instructions by set number")
    instructions.add_argument("set_number", help="Set number like 6876-1")

    images = sub.add_parser("additional-images", help="Get additional images by Brickset setID")
    images.add_argument("set_id", type=int, help="Brickset setID")

    raw = sub.add_parser("raw", help="Call any Brickset method with arbitrary params")
    raw.add_argument("method", help="Method name like getReviews or getCollection")
    raw.add_argument("--param", action="append", default=[], help="key=value pair; repeatable")
    raw.add_argument("--post", action="store_true", help="Use POST instead of GET")

    return parser


def safe_get(obj: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = obj
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def format_set_line(item: dict[str, Any]) -> str:
    number = f"{item.get('number', '?')}-{item.get('numberVariant', '?')}"
    name = item.get("name", "(no name)")
    year = item.get("year", "?")
    theme = item.get("theme", "?")
    pieces = item.get("pieces")
    minifigs = item.get("minifigs")
    extras: list[str] = []
    if pieces is not None:
        extras.append(f"{pieces} pcs")
    if minifigs is not None:
        extras.append(f"{minifigs} minifigs")
    tail = f" - {', '.join(extras)}" if extras else ""
    return f"- {number}: {name} ({year}, {theme}){tail}"


def format_result_text(command: str, args: argparse.Namespace, result: dict[str, Any]) -> str:
    status = result.get("status")
    if status in {"error", "http_error", "network_error", "decode_error"}:
        parts = [f"Brickset API call failed: {status}"]
        if "message" in result:
            parts.append(str(result["message"]))
        if "code" in result:
            parts.append(f"HTTP {result['code']}")
        if "body" in result:
            body = str(result["body"]).strip()
            if body:
                parts.append(body[:1200])
        return "\n".join(parts)

    if command == "check-key":
        return "Brickset API key is valid."

    if command == "usage-stats":
        matches = result.get("matches", 0)
        lines = [f"Brickset API usage stats: {matches} day entries in the last 30 days."]
        usage = result.get("apiKeyUsage", [])[:10]
        for entry in usage:
            lines.append(f"- {entry.get('dateStamp', '?')}: {entry.get('count', 0)} getSets calls")
        if result.get("apiKeyUsage") and len(result["apiKeyUsage"]) > 10:
            lines.append(f"- ... {len(result['apiKeyUsage']) - 10} more entries")
        return "\n".join(lines)

    if command == "themes":
        themes = result.get("themes", [])
        lines = [f"Brickset themes: {result.get('matches', len(themes))} total."]
        for item in themes[:25]:
            lines.append(
                f"- {item.get('theme', '?')}: {item.get('setCount', 0)} sets, {item.get('subthemeCount', 0)} subthemes, {item.get('yearFrom', '?')}–{item.get('yearTo', '?')}"
            )
        if len(themes) > 25:
            lines.append(f"- ... {len(themes) - 25} more themes")
        return "\n".join(lines)

    if command == "years":
        years = result.get("years", [])
        scope = args.theme if getattr(args, "theme", "") else "all themes"
        lines = [f"Brickset years for {scope}: {result.get('matches', len(years))} entries."]
        for item in years[:25]:
            lines.append(f"- {item.get('year', '?')}: {item.get('setCount', 0)} sets")
        if len(years) > 25:
            lines.append(f"- ... {len(years) - 25} more years")
        return "\n".join(lines)

    if command == "subthemes":
        subthemes = result.get("subthemes", [])
        lines = [f"Brickset subthemes for {args.theme}: {result.get('matches', len(subthemes))} entries."]
        for item in subthemes[:25]:
            lines.append(
                f"- {item.get('subtheme', '?')}: {item.get('setCount', 0)} sets, {item.get('yearFrom', '?')}–{item.get('yearTo', '?')}"
            )
        if len(subthemes) > 25:
            lines.append(f"- ... {len(subthemes) - 25} more subthemes")
        return "\n".join(lines)

    if command in {"search", "get-sets"}:
        sets = result.get("sets", [])
        lines = [f"Brickset set results: {result.get('matches', len(sets))} matches."]
        for item in sets[:20]:
            lines.append(format_set_line(item))
        if len(sets) > 20:
            lines.append(f"- ... {len(sets) - 20} more sets in this page")
        return "\n".join(lines)

    if command == "instructions2":
        instructions = result.get("instructions", [])
        lines = [f"Instructions for {args.set_number}: {result.get('matches', len(instructions))} files."]
        for item in instructions[:20]:
            lines.append(f"- {item.get('description', '(no description)')}: {item.get('URL', '')}")
        return "\n".join(lines)

    if command == "additional-images":
        images = result.get("additionalImages", [])
        lines = [f"Additional images for setID {args.set_id}: {result.get('matches', len(images))} files."]
        for item in images[:20]:
            url = item.get("imageURL") or item.get("URL") or str(item)
            lines.append(f"- {url}")
        return "\n".join(lines)

    if command == "raw":
        lines = [f"Brickset raw call succeeded: {args.method}"]
        for key in ("matches", "message"):
            if key in result:
                lines.append(f"- {key}: {result[key]}")
        top_keys = ", ".join(sorted(result.keys()))
        lines.append(f"- top-level fields: {top_keys}")
        return "\n".join(lines)

    return json.dumps(result, indent=2, ensure_ascii=False)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    api_key = resolve_api_key(args.api_key)

    if args.command == "check-key":
        result = call_api("checkKey", api_key)
    elif args.command == "usage-stats":
        result = call_api("getKeyUsageStats", api_key)
    elif args.command == "themes":
        result = call_api("getThemes", api_key)
    elif args.command == "years":
        result = call_api("getYears", api_key, {"theme": args.theme})
    elif args.command == "subthemes":
        result = call_api("getSubthemes", api_key, {"theme": args.theme})
    elif args.command == "get-sets":
        result = call_api("getSets", api_key, {"userHash": args.user_hash or "", "params": parse_params(args.params)}, post=True)
    elif args.command == "search":
        payload = {
            "query": args.query,
            "pageSize": args.page_size,
            "pageNumber": args.page_number,
            "orderBy": args.order_by,
        }
        if args.theme:
            payload["theme"] = args.theme
        if args.year:
            payload["year"] = str(args.year)
        if args.extended_data:
            payload["extendedData"] = 1
        result = call_api("getSets", api_key, {"userHash": "", "params": json.dumps(payload, separators=(",", ":"))}, post=True)
    elif args.command == "instructions2":
        result = call_api("getInstructions2", api_key, {"setNumber": args.set_number})
    elif args.command == "additional-images":
        result = call_api("getAdditionalImages", api_key, {"setID": args.set_id})
    elif args.command == "raw":
        extra: dict[str, str] = {}
        for item in args.param:
            if "=" not in item:
                raise SystemExit(f"Invalid --param '{item}'. Use key=value")
            key, value = item.split("=", 1)
            extra[key] = value
        result = call_api(args.method, api_key, extra, post=args.post)
    else:
        parser.error("Unknown command")
        return 2

    if args.format == "text":
        print(format_result_text(args.command, args, result))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    if result.get("status") in {"error", "http_error", "network_error", "decode_error"}:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
