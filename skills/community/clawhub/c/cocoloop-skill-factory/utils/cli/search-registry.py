#!/usr/bin/env python3
"""Run a cocoloop or clawhub search and normalize the results as JSON."""

from __future__ import annotations

import argparse
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import sys

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent))

from _common import (
    json_print,
    normalize_search_payload,
    normalize_text_results,
    run_command,
    safe_json_loads,
    utc_now,
)


DEFAULT_COMMANDS = {
    "cocoloop": ["cocoloop", "search"],
    "clawhub": ["clawhub", "--no-input", "search"],
}

COCOLOOP_SEARCH_API = "https://api.cocoloop.cn/api/v1/store/skills?page=1&page_size={limit}&keyword={query}&sort=downloads"
GITHUB_SEARCH_API = "https://api.github.com/search/repositories?q={query}&per_page={limit}&sort=stars&order=desc"


def slugify(value: str) -> str:
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", value.strip().lower())).strip("-")


def fetch_cocoloop_api(query: str, limit: int) -> dict[str, Any]:
    url = COCOLOOP_SEARCH_API.format(
        query=urllib.parse.quote(query, safe=""),
        limit=limit,
    )
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "cocoloop-skill-factory/1.0",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw_text = response.read().decode("utf-8")
        parsed_json = safe_json_loads(raw_text)
        return {
            "command": ["GET", url],
            "available": True,
            "ok": parsed_json is not None,
            "returncode": 0 if parsed_json is not None else None,
            "raw_text": raw_text,
            "parsed_json": parsed_json,
            "error": None if parsed_json is not None else "cocoloop api returned non-json payload",
        }
    except Exception as exc:
        return {
            "command": ["GET", url],
            "available": True,
            "ok": False,
            "returncode": None,
            "raw_text": "",
            "parsed_json": None,
            "error": str(exc),
        }


def fetch_github_api(query: str, limit: int) -> dict[str, Any]:
    url = GITHUB_SEARCH_API.format(
        query=urllib.parse.quote(query, safe=""),
        limit=limit,
    )
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "cocoloop-skill-factory/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw_text = response.read().decode("utf-8")
        parsed_json = safe_json_loads(raw_text)
        ok = parsed_json is not None and not (
            isinstance(parsed_json, dict)
            and parsed_json.get("message")
            and "items" not in parsed_json
        )
        return {
            "command": ["GET", url],
            "available": True,
            "ok": ok,
            "returncode": 0 if ok else None,
            "raw_text": raw_text,
            "parsed_json": parsed_json,
            "error": None if ok else (
                parsed_json.get("message") if isinstance(parsed_json, dict) and parsed_json.get("message") else "github api returned non-json payload"
            ),
        }
    except Exception as exc:
        return {
            "command": ["GET", url],
            "available": True,
            "ok": False,
            "returncode": None,
            "raw_text": "",
            "parsed_json": None,
            "error": str(exc),
        }


def execute_search(source: str, query: str, limit: int) -> dict[str, Any]:
    if source == "github":
        return fetch_github_api(query, limit)
    args = [*DEFAULT_COMMANDS[source], query]
    if source == "clawhub":
        args.extend(["--limit", str(limit)])
    result = run_command(args, timeout=60)
    raw_text = (result.get("stdout") or "") + (result.get("stderr") or "")
    parsed_json = safe_json_loads(result.get("stdout") or "")
    if parsed_json is None:
        parsed_json = safe_json_loads(result.get("stderr") or "")

    return {
        "command": args,
        "available": result["available"],
        "ok": result["ok"],
        "returncode": result["returncode"],
        "raw_text": raw_text,
        "parsed_json": parsed_json,
        "error": None if result["ok"] else (result["stderr"] or "search command returned a non-zero exit code"),
    }


def normalize_clawhub_text(raw_text: str) -> list[dict[str, Any]]:
    items = []
    pattern = re.compile(r"^(?P<slug>\S+)\s{2,}(?P<title>.+?)\s{2,}\((?P<score>[0-9.]+)\)$")
    for line in raw_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("- Searching"):
            continue
        match = pattern.match(stripped)
        if match:
            items.append(
                {
                    "source": "clawhub",
                    "title": match.group("title").strip(),
                    "summary": "",
                    "url": "",
                    "score": float(match.group("score")),
                    "tags": [match.group("slug")],
                    "raw": stripped,
                    "slug": match.group("slug"),
                }
            )
            continue
        items.append(
            {
                "source": "clawhub",
                "title": stripped,
                "summary": "",
                "url": "",
                "score": None,
                "tags": [],
                "raw": stripped,
            }
        )
    return items


def extract_slug_candidates(item: dict[str, Any]) -> list[str]:
    candidates: list[str] = []

    def add_candidate(value: Any) -> None:
        if not isinstance(value, str):
            return
        normalized = slugify(value)
        if normalized and normalized not in candidates:
            candidates.append(normalized)

    for key in ("slug", "id", "name", "skill_name", "title", "label"):
        add_candidate(item.get(key))

    raw = item.get("raw")
    if isinstance(raw, dict):
        for key in ("slug", "id", "name", "skill_name", "title", "label"):
            add_candidate(raw.get(key))

    for tag in item.get("tags") or []:
        add_candidate(tag)

    return candidates


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    source = args.source
    if not args.query:
        return {
            "tool": "search-registry",
            "status": "degraded",
            "generated_at": utc_now(),
            "source": source,
            "query": "",
            "command": None,
            "execution": {
                "mode": "validation",
                "available": False,
                "ok": False,
                "returncode": None,
            },
            "raw_format": "empty",
            "raw_text": "",
            "normalized_results": [],
            "degradation": {
                "reason": "missing_query",
                "message": "query is required",
            },
        }

    execution = execute_search(source, args.query, args.limit)
    if source == "cocoloop" and (not execution["available"] or not execution["ok"]):
        execution = fetch_cocoloop_api(args.query, args.limit)
    parsed_json = execution["parsed_json"]
    if not execution["available"] or not execution["ok"]:
        normalized = []
        raw_format = "text" if execution["raw_text"].strip() else "empty"
    elif parsed_json is not None:
        normalized = normalize_search_payload(parsed_json, source)
        raw_format = "json"
    elif source == "clawhub":
        normalized = normalize_clawhub_text(execution["raw_text"])
        raw_format = "text" if execution["raw_text"].strip() else "empty"
    else:
        normalized = normalize_text_results(execution["raw_text"], source)
        raw_format = "text" if execution["raw_text"].strip() else "empty"

    exact_slug = slugify(args.exact_slug or "")
    exact_matches = []
    if exact_slug:
        exact_matches = [
            item for item in normalized
            if exact_slug in extract_slug_candidates(item)
        ]

    status = "ok" if execution["ok"] else "degraded"
    degradation = None
    if not execution["available"]:
        degradation = {
            "reason": "command_missing",
            "message": f"{source} command is not available on this machine",
            "command": execution["command"],
        }
    elif not execution["ok"]:
        degradation = {
            "reason": "command_failed",
            "message": execution["error"],
            "command": execution["command"],
        }

    return {
        "tool": "search-registry",
        "status": status,
        "generated_at": utc_now(),
        "source": source,
        "query": args.query,
        "command": execution["command"],
        "execution": {
            "mode": "command",
            "available": execution["available"],
            "ok": execution["ok"],
            "returncode": execution["returncode"],
        },
        "exact_match_found": bool(exact_matches),
        "exact_matches": exact_matches,
        "exact_slug": exact_slug,
        "raw_format": raw_format,
        "raw_text": execution["raw_text"],
        "normalized_results": normalized,
        "degradation": degradation,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run cocoloop/clawhub/github search and normalize the results as JSON.")
    parser.add_argument("--source", choices=("cocoloop", "clawhub", "github"), required=True)
    parser.add_argument("--query", default="", help="Search query text.")
    parser.add_argument("--exact-slug", default="", help="Optional slug to match exactly inside normalized results.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of search results to request.")
    args = parser.parse_args()

    payload = build_payload(args)
    return json_print(payload)


if __name__ == "__main__":
    raise SystemExit(main())
