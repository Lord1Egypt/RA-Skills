#!/usr/bin/env python3
"""Invoke fixed AI Web API /search modes."""

from __future__ import annotations

import argparse
import sys

from ai_web_client import (
    DEFAULT_REQUEST_TIMEOUT, emit_dry_run, post_json, resolve_base_url, resolve_token,
    validate_country, validate_formats, validate_int_range, validate_string_list,
)


MODES = {
    "web": {"unique_id": "search_web", "source": "web"},
    "shopping": {"unique_id": "search_shopping", "source": "shopping"},
    "news": {"unique_id": "search_news", "source": "news"},
    "scholar": {"unique_id": "search_scholar", "source": "scholar"},
}


def add_transport_arguments(parser):
    parser.add_argument("--base-url", help="Gateway origin. Defaults to https://aiwebapi.dataify.com.")
    parser.add_argument("--request-timeout", type=int, default=DEFAULT_REQUEST_TIMEOUT)
    parser.add_argument("--dry-run", action="store_true", help="Print the request without sending it.")


def add_extract_arguments(parser):
    parser.add_argument("--extract-content", action="store_true", help="Extract result bodies.")
    parser.add_argument("--extract-format", action="append", choices=("markdown", "raw_html", "clean_html", "links"), help="Format for extracted result bodies; repeat for multiple formats.")
    parser.add_argument("--only-main-content", action=argparse.BooleanOptionalAction, default=None, help="Keep only main content when extracting.")
    parser.add_argument("--include-tag", action="append", help="Tag selector to include.")
    parser.add_argument("--exclude-tag", action="append", help="Tag selector to exclude.")
    parser.add_argument("--max-age-ms", type=int, help="Maximum cache age.")
    parser.add_argument("--timeout-ms", type=int, help="Extraction timeout in milliseconds.")
    parser.add_argument("--wait-for-ms", type=int, help="Wait time before extraction.")
    parser.add_argument("--advanced-mode", action=argparse.BooleanOptionalAction, default=None, help="Enable advanced extraction mode.")


def add_search_mode(subparsers, transport, name, unique_id, *, time_range=False, country=True):
    parser = subparsers.add_parser(name, parents=[transport], help=f"Search using unique_id={unique_id}.")
    parser.add_argument("--query", required=True, help="Search query, up to 256 characters.")
    parser.add_argument("--max-results", type=int, help="Maximum results, 1 to 100.")
    if country:
        parser.add_argument("--country", help="Two-letter uppercase country code.")
    parser.add_argument("--language", help="Search language.")
    if time_range:
        parser.add_argument("--time-range", choices=("hour", "day", "week", "month", "year"), help="Result freshness.")
    add_extract_arguments(parser)
    return parser


def build_parser():
    parser = argparse.ArgumentParser(description="Invoke fixed AI Web API search modes.")
    subparsers = parser.add_subparsers(dest="mode", required=True)
    transport = argparse.ArgumentParser(add_help=False)
    add_transport_arguments(transport)
    add_search_mode(subparsers, transport, "web", "search_web", time_range=True)
    add_search_mode(subparsers, transport, "shopping", "search_shopping")
    add_search_mode(subparsers, transport, "news", "search_news", time_range=True)
    add_search_mode(subparsers, transport, "scholar", "search_scholar", country=False)
    return parser


def build_payload(args):
    query = args.query.strip()
    if not query:
        raise ValueError("query must not be empty.")
    if len(query) > 256:
        raise ValueError("query must be no longer than 256 characters.")
    validate_int_range("max_results", args.max_results, 1, 100)
    country = validate_country(getattr(args, "country", None))
    mode = MODES[args.mode]
    payload = {"unique_id": mode["unique_id"], "source": mode["source"], "query": query}
    if args.max_results is not None:
        payload["max_results"] = args.max_results
    if country:
        payload["country"] = country
    if args.language:
        payload["language"] = args.language.strip()
    if getattr(args, "time_range", None):
        payload["time_range"] = args.time_range
    validate_int_range("max_age_ms", args.max_age_ms, 0, 172800000)
    validate_int_range("timeout_ms", args.timeout_ms, 1000, 120000)
    validate_int_range("wait_for_ms", args.wait_for_ms, 0, 30000)
    if args.timeout_ms and args.wait_for_ms is not None and args.wait_for_ms > args.timeout_ms / 2:
        raise ValueError("wait_for_ms must not exceed half of timeout_ms.")
    formats = validate_formats(args.extract_format)
    include_tags = validate_string_list("include_tags", args.include_tag)
    exclude_tags = validate_string_list("exclude_tags", args.exclude_tag)
    options = {}
    if formats: options["formats"] = formats
    if args.only_main_content is not None: options["only_main_content"] = args.only_main_content
    if include_tags: options["include_tags"] = include_tags
    if exclude_tags: options["exclude_tags"] = exclude_tags
    if args.max_age_ms is not None: options["max_age_ms"] = args.max_age_ms
    if args.timeout_ms is not None: options["timeout_ms"] = args.timeout_ms
    if args.wait_for_ms is not None: options["wait_for_ms"] = args.wait_for_ms
    if args.advanced_mode is not None: options["advanced_mode"] = args.advanced_mode
    if options and not args.extract_content:
        raise ValueError("extract options require --extract-content.")
    if args.extract_content: payload["extract_content"] = True
    if options: payload["extract_options"] = options
    return payload


def _configure_utf8_output():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try: stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, ValueError): pass


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        payload = build_payload(args)
        base_url = resolve_base_url(args.base_url, required=not args.dry_run)
        token = resolve_token()
        if args.dry_run:
            emit_dry_run("/search", payload, base_url, token)
            return 0
        if not token:
            print("DATAIFY_API_TOKEN is not set. Configure it before calling the AI Web API.", file=sys.stderr)
            return 1
        return post_json("/search", payload, base_url, token, args.request_timeout)
    except ValueError as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    _configure_utf8_output()
    raise SystemExit(main())
