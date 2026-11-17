#!/usr/bin/env python3
"""Invoke the fixed AI Web API /extract endpoint."""

from __future__ import annotations
import argparse
import sys
from ai_web_client import DEFAULT_REQUEST_TIMEOUT, emit_dry_run, normalize_public_url, parse_headers, post_json, resolve_base_url, resolve_token, validate_country, validate_formats, validate_int_range, validate_string_list

UNIQUE_ID = "extract"

def build_parser():
    parser = argparse.ArgumentParser(description="Invoke the AI Web API extract endpoint.")
    parser.add_argument("--url", required=True, help="Public page URL.")
    parser.add_argument("--format", action="append", choices=("markdown", "raw_html", "clean_html", "links"), help="Output format; repeat for multiple formats.")
    parser.add_argument("--only-main-content", action=argparse.BooleanOptionalAction, default=None, help="Keep only main content.")
    parser.add_argument("--include-tag", action="append", help="Tag selector to include.")
    parser.add_argument("--exclude-tag", action="append", help="Tag selector to exclude.")
    parser.add_argument("--header", action="append", help="Target request header as 'Name: Value' or 'Name=Value'; repeat as needed.")
    parser.add_argument("--max-age-ms", type=int, help="Maximum cache age.")
    parser.add_argument("--timeout-ms", type=int, help="Extraction timeout in milliseconds.")
    parser.add_argument("--wait-for-ms", type=int, help="Wait time before extraction.")
    parser.add_argument("--country", help="Two-letter uppercase country code.")
    parser.add_argument("--advanced-mode", action=argparse.BooleanOptionalAction, default=None, help="Enable advanced extraction mode.")
    parser.add_argument("--base-url", help="Gateway origin. Defaults to https://aiwebapi.dataify.com.")
    parser.add_argument("--request-timeout", type=int, default=DEFAULT_REQUEST_TIMEOUT)
    parser.add_argument("--dry-run", action="store_true", help="Print the request without sending it.")
    return parser

def build_payload(args):
    validate_int_range("max_age_ms", args.max_age_ms, 0, 172800000)
    validate_int_range("timeout_ms", args.timeout_ms, 1000, 120000)
    validate_int_range("wait_for_ms", args.wait_for_ms, 0, 30000)
    if args.timeout_ms and args.wait_for_ms is not None and args.wait_for_ms > args.timeout_ms / 2:
        raise ValueError("wait_for_ms must not exceed half of timeout_ms.")
    country = validate_country(args.country)
    formats = validate_formats(args.format)
    include_tags = validate_string_list("include_tags", args.include_tag)
    exclude_tags = validate_string_list("exclude_tags", args.exclude_tag)
    headers = parse_headers(args.header)
    payload = {"unique_id": UNIQUE_ID, "url": normalize_public_url(args.url)}
    if formats: payload["formats"] = formats
    if args.only_main_content is not None: payload["only_main_content"] = args.only_main_content
    if include_tags: payload["include_tags"] = include_tags
    if exclude_tags: payload["exclude_tags"] = exclude_tags
    if headers: payload["headers"] = headers
    if args.max_age_ms is not None: payload["max_age_ms"] = args.max_age_ms
    if args.timeout_ms is not None: payload["timeout_ms"] = args.timeout_ms
    if args.wait_for_ms is not None: payload["wait_for_ms"] = args.wait_for_ms
    if country: payload["country"] = country
    if args.advanced_mode is not None: payload["advanced_mode"] = args.advanced_mode
    return payload

def _configure_utf8_output():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try: stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, ValueError): pass

def main():
    parser = build_parser(); args = parser.parse_args()
    try:
        payload = build_payload(args)
        base_url = resolve_base_url(args.base_url, required=not args.dry_run)
        token = resolve_token()
        if args.dry_run:
            emit_dry_run("/extract", payload, base_url, token); return 0
        if not token:
            print("DATAIFY_API_TOKEN is not set. Configure it before calling the AI Web API.", file=sys.stderr); return 1
        return post_json("/extract", payload, base_url, token, args.request_timeout)
    except ValueError as exc:
        parser.error(str(exc))
    return 2

if __name__ == "__main__":
    _configure_utf8_output(); raise SystemExit(main())
