#!/usr/bin/env python3
"""Invoke the fixed AI Web API /map endpoint."""

from __future__ import annotations
import argparse
import sys
from ai_web_client import DEFAULT_REQUEST_TIMEOUT, emit_dry_run, normalize_public_url, post_json, resolve_base_url, resolve_token, validate_country, validate_int_range

UNIQUE_ID = "map"

def build_parser():
    parser = argparse.ArgumentParser(description="Invoke the AI Web API map endpoint.")
    parser.add_argument("--url", required=True, help="Public starting URL.")
    parser.add_argument("--country", help="Two-letter uppercase country code.")
    parser.add_argument("--domain-filter", choices=("domain", "all"), help="Domain scope.")
    parser.add_argument("--limit", type=int, help="Maximum returned URLs, 1 to 100000.")
    parser.add_argument("--sitemap", choices=("skip", "include", "only"), help="Sitemap mode.")
    parser.add_argument("--base-url", help="Gateway origin. Defaults to https://aiwebapi.dataify.com.")
    parser.add_argument("--request-timeout", type=int, default=DEFAULT_REQUEST_TIMEOUT)
    parser.add_argument("--dry-run", action="store_true", help="Print the request without sending it.")
    return parser

def build_payload(args):
    validate_int_range("limit", args.limit, 1, 100000)
    country = validate_country(args.country)
    payload = {"unique_id": UNIQUE_ID, "url": normalize_public_url(args.url)}
    if country: payload["country"] = country
    if args.domain_filter: payload["domain_filter"] = args.domain_filter
    if args.limit is not None: payload["limit"] = args.limit
    if args.sitemap: payload["sitemap"] = args.sitemap
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
            emit_dry_run("/map", payload, base_url, token); return 0
        if not token:
            print("DATAIFY_API_TOKEN is not set. Configure it before calling the AI Web API.", file=sys.stderr); return 1
        return post_json("/map", payload, base_url, token, args.request_timeout)
    except ValueError as exc:
        parser.error(str(exc))
    return 2

if __name__ == "__main__":
    _configure_utf8_output(); raise SystemExit(main())
