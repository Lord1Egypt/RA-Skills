#!/usr/bin/env python3
"""Better Tavily Search CLI for OpenClaw.

Design goals:
- Standard-library only
- Conservative defaults
- Stable machine-facing output
- Thin execution layer that preserves Tavily-native controls

Subcommands:
- search
- extract
- map
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, NoReturn
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request

API_BASE = os.environ.get("TAVILY_API_BASE", "https://api.tavily.com").rstrip("/")
DEFAULT_TIMEOUT = 30.0
DEFAULT_RETRIES = 2

SEARCH_DEPTHS = {"advanced", "basic", "fast", "ultra-fast"}
EXTRACT_DEPTHS = {"basic", "advanced"}
SEARCH_TOPICS = {"general", "news", "finance"}
TIME_RANGE_ALIASES = {
    "day": "day",
    "week": "week",
    "month": "month",
    "year": "year",
    "d": "day",
    "w": "week",
    "m": "month",
    "y": "year",
}
CHUNK_SPLIT_RE = re.compile(r"\s*(?:\[\.\.\.\]|\[\u2026\])\s*")


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def warn(message: str) -> None:
    eprint(f"Warning: {message}")


def fatal(message: str, exit_code: int = 2) -> NoReturn:
    eprint(f"Error: {message}")
    raise SystemExit(exit_code)


def compact_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def normalize_date(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise argparse.ArgumentTypeError("dates must use YYYY-MM-DD")
    return value


def normalize_time_range(value: str | None) -> str | None:
    if value is None:
        return None
    lowered = value.strip().lower()
    if lowered not in TIME_RANGE_ALIASES:
        raise argparse.ArgumentTypeError(f"invalid time range: {value!r}")
    return TIME_RANGE_ALIASES[lowered]


def parse_csvish(items: list[str] | None) -> list[str]:
    if not items:
        return []
    out: list[str] = []
    for item in items:
        for part in item.split(","):
            cleaned = part.strip()
            if cleaned:
                out.append(cleaned)
    return out


def unique_preserve(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def clamp(value: int, lower: int, upper: int) -> int:
    return max(lower, min(upper, value))


def maybe_truncate(text: str | None, limit: int = 500) -> str | None:
    if text is None:
        return None
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def split_chunks(raw_content: str | None) -> list[str]:
    if not raw_content:
        return []
    parts = [part.strip() for part in CHUNK_SPLIT_RE.split(raw_content)]
    return [part for part in parts if part]


def infer_domain(url: str | None) -> str | None:
    if not url:
        return None
    try:
        netloc = urllib_parse.urlparse(url).netloc.lower()
    except Exception:
        return None
    return netloc or None


def validate_http_url(url: str, *, label: str = "URL") -> str:
    value = url.strip()
    parsed = urllib_parse.urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        fatal(f"{label} must be a valid http/https URL: {url!r}")
    return value


def note_query_length(query: str) -> None:
    if len(query) > 400:
        warn("query is longer than 400 characters; Tavily search usually works better with shorter, retrieval-style queries")


def read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists() or not path.is_file():
        return values
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return values
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, raw_val = line.split("=", 1)
        key = key.strip()
        raw_val = raw_val.strip()
        if not key:
            continue
        if len(raw_val) >= 2 and raw_val[0] == raw_val[-1] and raw_val[0] in {'"', "'"}:
            raw_val = raw_val[1:-1]
        values[key] = raw_val
    return values


def load_api_key() -> str:
    env_value = (os.environ.get("TAVILY_API_KEY") or "").strip()
    if env_value:
        return env_value
    env_file = Path.home() / ".openclaw" / ".env"
    file_vars = read_env_file(env_file)
    env_value = (file_vars.get("TAVILY_API_KEY") or "").strip()
    if env_value:
        return env_value
    fatal("Missing TAVILY_API_KEY. Set the environment variable or add it to ~/.openclaw/.env", exit_code=1)


def summarize_error_body(body: str) -> str:
    text = body.strip()
    if not text:
        return ""
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return maybe_truncate(text, 300) or ""

    def collect(value: Any) -> list[str]:
        if isinstance(value, str):
            cleaned = compact_whitespace(value)
            return [cleaned] if cleaned else []
        if isinstance(value, list):
            out: list[str] = []
            for item in value:
                out.extend(collect(item))
            return out
        if isinstance(value, dict):
            out: list[str] = []
            for key in ("detail", "message", "error", "title", "description"):
                if key in value:
                    out.extend(collect(value[key]))
            return out
        return []

    messages = unique_preserve(collect(parsed))
    if messages:
        return maybe_truncate(" | ".join(messages), 300) or ""
    return maybe_truncate(text, 300) or ""


class TavilyHTTPError(RuntimeError):
    def __init__(self, status: int, message: str, body: str = "") -> None:
        super().__init__(message)
        self.status = status
        self.body = body


class TavilyClient:
    def __init__(self, api_key: str, timeout: float = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES) -> None:
        self.api_key = api_key
        self.timeout = timeout
        self.retries = retries

    def post(self, endpoint: str, payload: dict[str, Any], *, timeout: float | None = None) -> dict[str, Any]:
        url = f"{API_BASE}/{endpoint.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "better-tavily-search/0.2",
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib_request.Request(url, data=data, headers=headers, method="POST")

        last_exc: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                with urllib_request.urlopen(req, timeout=timeout or self.timeout) as resp:
                    body = resp.read().decode("utf-8", errors="replace")
                    try:
                        parsed = json.loads(body)
                    except json.JSONDecodeError as exc:
                        raise RuntimeError(f"{endpoint} returned non-JSON response") from exc
                    if not isinstance(parsed, dict):
                        raise RuntimeError(f"{endpoint} returned unexpected response shape")
                    return parsed
            except urllib_error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                detail = summarize_error_body(body)
                message = f"Tavily {endpoint} failed with HTTP {exc.code}"
                if detail:
                    message += f": {detail}"
                last_exc = TavilyHTTPError(exc.code, message, body)
                if exc.code in {429, 500, 502, 503, 504} and attempt < self.retries:
                    retry_after = exc.headers.get("Retry-After") if exc.headers else None
                    delay = float(retry_after) if retry_after and retry_after.isdigit() else (1.5 ** attempt)
                    time.sleep(min(delay, 10.0))
                    continue
                raise last_exc
            except urllib_error.URLError as exc:
                last_exc = RuntimeError(f"Network error calling Tavily {endpoint}: {exc}")
                if attempt < self.retries:
                    time.sleep(1.5 ** attempt)
                    continue
                raise last_exc
        assert last_exc is not None
        raise last_exc


def add_common_output_flags(parser: argparse.ArgumentParser, *, allow_brave: bool) -> None:
    formats = ["agent", "raw", "md"] + (["brave"] if allow_brave else [])
    parser.add_argument("--format", choices=formats, default="agent", help="Output format")


def add_usage_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--include-usage",
        dest="include_usage",
        action="store_true",
        default=True,
        help="Include usage metadata in machine-facing requests (default: true)",
    )
    parser.add_argument(
        "--no-include-usage",
        dest="include_usage",
        action="store_false",
        help="Disable usage metadata in the Tavily response",
    )


def add_answer_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--include-answer",
        nargs="?",
        const="basic",
        default=False,
        choices=["basic", "advanced"],
        metavar="{basic,advanced}",
        help="Include an LLM-generated answer. Bare flag implies 'basic'.",
    )


def add_raw_content_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--include-raw-content",
        nargs="?",
        const="markdown",
        default=False,
        choices=["markdown", "text"],
        metavar="{markdown,text}",
        help="Include parsed page content in search results. Bare flag implies 'markdown'.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tavily.py",
        description="Tavily-powered search/extract/map CLI for OpenClaw skills",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"HTTP timeout in seconds for this CLI process (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=DEFAULT_RETRIES,
        help=f"Retry count for retryable network/API failures (default: {DEFAULT_RETRIES})",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search the web with Tavily")
    search.add_argument("--query", required=True, help="Search query")
    search.add_argument(
        "--profile",
        choices=["general", "news", "finance", "official", "precision", "regional"],
        default="general",
        help="High-level intent profile",
    )
    search.add_argument("--topic", choices=sorted(SEARCH_TOPICS), help="Override Tavily topic")
    search.add_argument("--search-depth", choices=sorted(SEARCH_DEPTHS), help="Override Tavily search depth")
    search.add_argument("--max-results", type=int, default=5, help="Requested number of results (default: 5)")
    search.add_argument("--time-range", choices=sorted(TIME_RANGE_ALIASES), help="Relative recency filter")
    search.add_argument("--start-date", type=normalize_date, help="YYYY-MM-DD")
    search.add_argument("--end-date", type=normalize_date, help="YYYY-MM-DD")
    search.add_argument("--include-domains", action="append", help="Comma-separated or repeated list of domains")
    search.add_argument("--exclude-domains", action="append", help="Comma-separated or repeated list of domains")
    search.add_argument("--country", help="Country boost for topic=general")
    search.add_argument("--exact-match", action="store_true", help="Require exact quoted phrase matching")
    search.add_argument("--auto-parameters", action="store_true", help="Let Tavily infer additional parameters")
    search.add_argument("--chunks-per-source", type=int, help="1..3 for advanced search")
    search.add_argument("--include-favicon", action="store_true", help="Include favicon URLs in results")
    search.add_argument("--safe-search", action="store_true", help="Enable enterprise safe search if available")
    add_answer_flag(search)
    add_raw_content_flag(search)
    add_usage_flags(search)
    add_common_output_flags(search, allow_brave=True)

    extract = subparsers.add_parser("extract", help="Extract content from specific URLs")
    extract.add_argument(
        "--urls",
        required=True,
        action="append",
        help="Comma-separated or repeated list of URLs to extract",
    )
    extract.add_argument("--query", help="Optional user intent for reranking extracted chunks")
    extract.add_argument(
        "--chunks-per-source",
        type=int,
        default=None,
        help="1..5 when query is provided (default: 3 when query is provided)",
    )
    extract.add_argument(
        "--extract-depth",
        choices=sorted(EXTRACT_DEPTHS),
        default="basic",
        help="Extraction depth (default: basic)",
    )
    extract.add_argument(
        "--content-format",
        choices=["markdown", "text"],
        default="markdown",
        help="Format of extracted page content (default: markdown)",
    )
    extract.add_argument("--include-images", action="store_true", help="Include extracted image URLs")
    extract.add_argument("--include-favicon", action="store_true", help="Include favicon URLs")
    extract.add_argument("--request-timeout", type=float, help="Endpoint timeout in seconds")
    add_usage_flags(extract)
    add_common_output_flags(extract, allow_brave=False)

    mapping = subparsers.add_parser("map", help="Map a documentation site or knowledge base")
    mapping.add_argument("--url", required=True, help="Root URL to map")
    mapping.add_argument("--instructions", help="Optional natural-language mapping instructions")
    mapping.add_argument("--max-depth", type=int, default=1, help="1..5 (default: 1)")
    mapping.add_argument("--max-breadth", type=int, default=20, help="1..500 (default: 20)")
    mapping.add_argument("--limit", type=int, default=50, help="Total URLs to process (default: 50)")
    mapping.add_argument("--select-paths", action="append", help="Comma-separated or repeated regex path filters")
    mapping.add_argument("--select-domains", action="append", help="Comma-separated or repeated regex domain filters")
    mapping.add_argument("--exclude-paths", action="append", help="Comma-separated or repeated regex path exclusions")
    mapping.add_argument("--exclude-domains", action="append", help="Comma-separated or repeated regex domain exclusions")
    mapping.add_argument(
        "--allow-external",
        dest="allow_external",
        action="store_true",
        default=False,
        help="Include external domain links in results",
    )
    mapping.add_argument(
        "--no-allow-external",
        dest="allow_external",
        action="store_false",
        help="Exclude external domain links from results (default)",
    )
    mapping.add_argument("--request-timeout", type=float, help="Endpoint timeout in seconds")
    add_usage_flags(mapping)
    add_common_output_flags(mapping, allow_brave=False)

    return parser


def profile_defaults(profile: str, query: str) -> dict[str, Any]:
    defaults: dict[str, Any] = {
        "topic": "general",
        "search_depth": "basic",
    }
    if profile == "news":
        defaults["topic"] = "news"
    elif profile == "finance":
        defaults["topic"] = "finance"
    elif profile == "precision":
        defaults["search_depth"] = "advanced"
        if '"' in query:
            defaults["exact_match"] = True
        defaults["chunks_per_source"] = 3
    elif profile in {"official", "regional"}:
        defaults["topic"] = "general"
    return defaults


def maybe_add(payload: dict[str, Any], key: str, value: Any) -> None:
    if value is None:
        return
    if value is False:
        return
    if isinstance(value, list) and not value:
        return
    payload[key] = value


def effective_http_timeout(command: str, args: argparse.Namespace) -> float:
    base_timeout = max(1.0, float(args.timeout))
    if command == "search":
        return base_timeout
    if command == "extract":
        endpoint_timeout = args.request_timeout
        if endpoint_timeout is None:
            endpoint_timeout = 30.0 if args.extract_depth == "advanced" else 10.0
        return max(base_timeout, float(endpoint_timeout) + 5.0)
    if command == "map":
        endpoint_timeout = float(args.request_timeout) if args.request_timeout is not None else 150.0
        return max(base_timeout, endpoint_timeout + 5.0)
    return base_timeout


def build_search_payload(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    query = compact_whitespace(args.query)
    if not query:
        fatal("search query cannot be empty")
    note_query_length(query)

    if args.time_range and (args.start_date or args.end_date):
        fatal("use either --time-range or --start-date/--end-date, not both")
    if args.start_date and args.end_date and args.start_date > args.end_date:
        fatal("--start-date must be on or before --end-date")

    defaults = profile_defaults(args.profile, query)
    topic = args.topic or defaults.get("topic", "general")
    search_depth = args.search_depth or defaults.get("search_depth", "basic")
    time_range = normalize_time_range(args.time_range)

    if args.safe_search and search_depth in {"fast", "ultra-fast"}:
        fatal("--safe-search is not supported with --search-depth fast or ultra-fast; use basic or advanced")

    include_domains = unique_preserve(parse_csvish(args.include_domains))
    exclude_domains = unique_preserve(parse_csvish(args.exclude_domains))
    overlap = {d.lower() for d in include_domains} & {d.lower() for d in exclude_domains}
    if overlap:
        warn(f"the same domains appeared in both include and exclude lists and will remain in include only: {', '.join(sorted(overlap))}")
        exclude_domains = [d for d in exclude_domains if d.lower() not in overlap]

    payload: dict[str, Any] = {
        "query": query,
        "topic": topic,
        "search_depth": search_depth,
        "max_results": clamp(args.max_results, 1, 20),
        "include_usage": bool(args.include_usage),
        "include_favicon": bool(args.include_favicon),
        "include_answer": False,
        "include_raw_content": False,
    }

    if args.include_answer is not False:
        payload["include_answer"] = args.include_answer
    if args.include_raw_content is not False:
        payload["include_raw_content"] = args.include_raw_content

    maybe_add(payload, "time_range", time_range)
    maybe_add(payload, "start_date", args.start_date)
    maybe_add(payload, "end_date", args.end_date)
    maybe_add(payload, "include_domains", include_domains)
    maybe_add(payload, "exclude_domains", exclude_domains)

    if args.country:
        if topic == "general":
            payload["country"] = args.country.strip().lower()
        else:
            warn("--country only applies to topic=general and will be ignored for this request")

    exact_match = args.exact_match or defaults.get("exact_match", False)
    if exact_match:
        payload["exact_match"] = True
    if args.auto_parameters:
        payload["auto_parameters"] = True
    if args.safe_search:
        payload["safe_search"] = True

    chunks = args.chunks_per_source if args.chunks_per_source is not None else defaults.get("chunks_per_source")
    if chunks is not None:
        chunks = clamp(int(chunks), 1, 3)
        if search_depth == "advanced":
            payload["chunks_per_source"] = chunks
        elif args.chunks_per_source is not None:
            warn("--chunks-per-source is only sent for search_depth=advanced and will be ignored for this request")

    meta = {
        "query_original": args.query,
        "query_executed": payload["query"],
        "profile": args.profile,
        "params": payload.copy(),
    }
    return payload, meta


def build_extract_payload(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    urls = unique_preserve([validate_http_url(url, label="extract URL") for url in parse_csvish(args.urls)])
    if not urls:
        fatal("extract requires at least one URL")

    payload: dict[str, Any] = {
        "urls": urls,
        "extract_depth": args.extract_depth,
        "format": args.content_format,
        "include_images": bool(args.include_images),
        "include_favicon": bool(args.include_favicon),
        "include_usage": bool(args.include_usage),
    }

    if args.query:
        query = compact_whitespace(args.query)
        if not query:
            fatal("extract query cannot be empty when provided")
        note_query_length(query)
        payload["query"] = query
        payload["chunks_per_source"] = clamp(args.chunks_per_source or 3, 1, 5)
    elif args.chunks_per_source is not None:
        warn("--chunks-per-source is only sent when --query is provided and will be ignored for this request")

    if args.request_timeout is not None:
        if not (1.0 <= args.request_timeout <= 60.0):
            fatal("extract --request-timeout must be between 1 and 60 seconds")
        payload["timeout"] = args.request_timeout

    meta = {
        "query": payload.get("query"),
        "urls": urls,
        "params": payload.copy(),
    }
    return payload, meta


def build_map_payload(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    if not (1 <= args.max_depth <= 5):
        fatal("map --max-depth must be between 1 and 5")
    if not (1 <= args.max_breadth <= 500):
        fatal("map --max-breadth must be between 1 and 500")
    if args.limit < 1:
        fatal("map --limit must be at least 1")

    root_url = validate_http_url(args.url, label="map URL")
    payload: dict[str, Any] = {
        "url": root_url,
        "max_depth": args.max_depth,
        "max_breadth": args.max_breadth,
        "limit": args.limit,
        "allow_external": bool(args.allow_external),
        "include_usage": bool(args.include_usage),
    }

    if args.instructions:
        instructions = compact_whitespace(args.instructions)
        if not instructions:
            fatal("map instructions cannot be empty when provided")
        payload["instructions"] = instructions

    maybe_add(payload, "select_paths", unique_preserve(parse_csvish(args.select_paths)))
    maybe_add(payload, "select_domains", unique_preserve(parse_csvish(args.select_domains)))
    maybe_add(payload, "exclude_paths", unique_preserve(parse_csvish(args.exclude_paths)))
    maybe_add(payload, "exclude_domains", unique_preserve(parse_csvish(args.exclude_domains)))

    if args.request_timeout is not None:
        if not (10.0 <= args.request_timeout <= 150.0):
            fatal("map --request-timeout must be between 10 and 150 seconds")
        payload["timeout"] = args.request_timeout

    meta = {
        "url": root_url,
        "params": payload.copy(),
    }
    return payload, meta


def to_agent_search(response: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    normalized_results: list[dict[str, Any]] = []
    for item in response.get("results", []) or []:
        if not isinstance(item, dict):
            continue
        url = item.get("url")
        title = item.get("title")
        if not url or not title:
            continue
        normalized_results.append(
            {
                "title": title,
                "url": url,
                "domain": infer_domain(url),
                "snippet": maybe_truncate(item.get("content"), 700),
                "score": item.get("score"),
                "favicon": item.get("favicon"),
                "published_date": item.get("published_date"),
            }
        )
    out: dict[str, Any] = {
        "endpoint": "search",
        "query_original": meta["query_original"],
        "query_executed": response.get("query") or meta["query_executed"],
        "profile": meta["profile"],
        "params": meta["params"],
        "answer": response.get("answer"),
        "results": normalized_results,
        "images": response.get("images") if response.get("images") else [],
        "usage": response.get("usage"),
        "response_time": response.get("response_time"),
        "request_id": response.get("request_id"),
    }
    if response.get("auto_parameters"):
        out["auto_parameters"] = response.get("auto_parameters")
    return out


def to_brave_search(response: dict[str, Any]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for item in response.get("results", []) or []:
        if not isinstance(item, dict):
            continue
        if not item.get("title") or not item.get("url"):
            continue
        results.append(
            {
                "title": item.get("title"),
                "url": item.get("url"),
                "snippet": maybe_truncate(item.get("content"), 700),
            }
        )
    out: dict[str, Any] = {
        "query": response.get("query"),
        "results": results,
    }
    if response.get("answer") is not None:
        out["answer"] = response.get("answer")
    return out


def to_md_search(response: dict[str, Any], meta: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Search Results")
    lines.append("")
    lines.append(f"Query: {response.get('query') or meta['query_executed']}")
    lines.append(f"Profile: {meta['profile']}")
    if response.get("response_time") is not None:
        lines.append(f"Response time: {response.get('response_time')}")
    lines.append("")
    results = response.get("results") or []
    if results:
        lines.append("## Sources")
        lines.append("")
        for idx, item in enumerate(results, start=1):
            if not isinstance(item, dict):
                continue
            title = item.get("title") or "Untitled"
            url = item.get("url") or ""
            score = item.get("score")
            score_text = f" (score: {score:.3f})" if isinstance(score, (int, float)) else ""
            lines.append(f"{idx}. **{title}**{score_text}")
            if url:
                lines.append(f"   {url}")
            snippet = maybe_truncate(item.get("content"), 700)
            if snippet:
                lines.append(f"   - {snippet}")
            lines.append("")
    else:
        lines.append("No results returned.")
        lines.append("")
    if response.get("answer"):
        lines.append("## Answer")
        lines.append("")
        lines.append(str(response["answer"]))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def to_agent_extract(response: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for item in response.get("results", []) or []:
        if not isinstance(item, dict):
            continue
        raw_content = item.get("raw_content") or item.get("content")
        results.append(
            {
                "url": item.get("url"),
                "title": item.get("title"),
                "content": raw_content,
                "chunks": split_chunks(raw_content),
                "favicon": item.get("favicon"),
                "images": item.get("images") or [],
            }
        )
    return {
        "endpoint": "extract",
        "query": meta.get("query"),
        "urls": meta.get("urls") or [],
        "params": meta.get("params"),
        "results": results,
        "failed_results": response.get("failed_results") or [],
        "usage": response.get("usage"),
        "response_time": response.get("response_time"),
        "request_id": response.get("request_id"),
    }


def to_md_extract(response: dict[str, Any], meta: dict[str, Any]) -> str:
    lines = ["# Extract Results", ""]
    if meta.get("query"):
        lines.append(f"Query: {meta['query']}")
        lines.append("")
    for idx, item in enumerate(response.get("results") or [], start=1):
        if not isinstance(item, dict):
            continue
        lines.append(f"## {idx}. {item.get('title') or item.get('url') or 'Untitled'}")
        lines.append("")
        if item.get("url"):
            lines.append(str(item["url"]))
            lines.append("")
        raw_content = item.get("raw_content") or item.get("content")
        if raw_content:
            lines.append(str(raw_content))
            lines.append("")
    failed = response.get("failed_results") or []
    if failed:
        lines.append("## Failed")
        lines.append("")
        for item in failed:
            if isinstance(item, dict):
                lines.append(f"- {item.get('url') or item}")
            else:
                lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def to_agent_map(response: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "endpoint": "map",
        "url": meta.get("url"),
        "params": meta.get("params"),
        "base_url": response.get("base_url"),
        "results": response.get("results") or [],
        "usage": response.get("usage"),
        "response_time": response.get("response_time"),
        "request_id": response.get("request_id"),
    }


def to_md_map(response: dict[str, Any], meta: dict[str, Any]) -> str:
    lines = ["# Map Results", "", f"URL: {meta.get('url')}", ""]
    if response.get("base_url"):
        lines.append(f"Base URL: {response.get('base_url')}")
        lines.append("")
    urls = response.get("results") or []
    if urls:
        lines.append("## URLs")
        lines.append("")
        for idx, url in enumerate(urls, start=1):
            lines.append(f"{idx}. {url}")
        lines.append("")
    else:
        lines.append("No URLs returned.")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def handle_search(client: TavilyClient, args: argparse.Namespace) -> None:
    payload, meta = build_search_payload(args)
    response = client.post("search", payload, timeout=effective_http_timeout("search", args))
    if args.format == "raw":
        print_json(response)
    elif args.format == "agent":
        print_json(to_agent_search(response, meta))
    elif args.format == "brave":
        print_json(to_brave_search(response))
    elif args.format == "md":
        print(to_md_search(response, meta), end="")
    else:
        fatal(f"unsupported output format for search: {args.format}")


def handle_extract(client: TavilyClient, args: argparse.Namespace) -> None:
    payload, meta = build_extract_payload(args)
    response = client.post("extract", payload, timeout=effective_http_timeout("extract", args))
    if args.format == "raw":
        print_json(response)
    elif args.format == "agent":
        print_json(to_agent_extract(response, meta))
    elif args.format == "md":
        print(to_md_extract(response, meta), end="")
    else:
        fatal(f"unsupported output format for extract: {args.format}")


def handle_map(client: TavilyClient, args: argparse.Namespace) -> None:
    payload, meta = build_map_payload(args)
    response = client.post("map", payload, timeout=effective_http_timeout("map", args))
    if args.format == "raw":
        print_json(response)
    elif args.format == "agent":
        print_json(to_agent_map(response, meta))
    elif args.format == "md":
        print(to_md_map(response, meta), end="")
    else:
        fatal(f"unsupported output format for map: {args.format}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    api_key = load_api_key()
    client = TavilyClient(api_key=api_key, timeout=max(1.0, args.timeout), retries=max(0, args.retries))

    try:
        if args.command == "search":
            handle_search(client, args)
        elif args.command == "extract":
            handle_extract(client, args)
        elif args.command == "map":
            handle_map(client, args)
        else:
            fatal(f"unsupported command: {args.command}")
    except TavilyHTTPError as exc:
        fatal(str(exc), exit_code=1)
    except RuntimeError as exc:
        fatal(str(exc), exit_code=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
