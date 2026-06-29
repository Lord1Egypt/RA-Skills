#!/usr/bin/env python3
"""
get.py - HTTP GET with sensible defaults for AI agents: retries on 5xx/429,
gzip decoding, redirect-following, custom headers, JSON pretty-print.

Pure Python 3 stdlib (urllib). No `requests`, no `httpx`, no pip install.

Usage:
    get.py URL [options]

Options:
    --output PATH        write the response body to PATH (default: stdout)
    --header 'Name: V'   custom header (may repeat)
    --bearer TOKEN       shorthand for --header 'Authorization: Bearer TOKEN'
    --basic USER:PASS    HTTP Basic auth shorthand
    --query K=V          add a URL query parameter (may repeat)
    --timeout SECONDS    request timeout (default: 30)
    --retries N          retry count for 5xx/429/timeout (default: 3)
    --no-redirects       do not follow 3xx redirects
    --insecure           skip TLS certificate verification
    --json               if response is JSON, pretty-print it (indent=2)
    --print-headers      print response headers (as JSON) to stderr
    --status-only        print the status code to stdout and exit (no body)
    --fail               exit with code 1 on any non-2xx status
    --json-summary       emit a machine-readable summary on stderr
    --quiet              suppress the request summary on stderr
    -h, --help           show this help

Exit codes:
    0   2xx response (or any response if --fail not set)
    1   --fail and the response was not 2xx (4xx / 5xx after retries)
    2   bad arguments / unsafe path / bad URL / network error
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
import urllib.error
import urllib.parse

from _common import (DEFAULT_TIMEOUT, fetch, headers_to_json, parse_headers,
                     safe_path, safe_url, write_or_print)


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("url", nargs="?")
    p.add_argument("--output")
    p.add_argument("--header", action="append", default=[])
    p.add_argument("--bearer")
    p.add_argument("--basic")
    p.add_argument("--query", action="append", default=[])
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    p.add_argument("--retries", type=int, default=3)
    p.add_argument("--no-redirects", dest="no_redirects", action="store_true")
    p.add_argument("--insecure", action="store_true")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--print-headers", dest="print_headers", action="store_true")
    p.add_argument("--status-only", dest="status_only", action="store_true")
    p.add_argument("--fail", action="store_true")
    p.add_argument("--json-summary", dest="json_summary", action="store_true")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.url:
        print(__doc__)
        return 0 if args.help else 2

    try:
        url = safe_url(args.url)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    # --query
    if args.query:
        qs = []
        for q in args.query:
            if "=" not in q:
                print(f"Error: --query expects K=V, got: {q!r}", file=sys.stderr)
                return 2
            k, _, v = q.partition("=")
            qs.append((k, v))
        sep = "&" if "?" in url else "?"
        url = url + sep + urllib.parse.urlencode(qs)

    try:
        headers = parse_headers(args.header)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if args.bearer:
        headers["Authorization"] = f"Bearer {args.bearer}"
    if args.basic:
        if ":" not in args.basic:
            print(f"Error: --basic expects USER:PASS", file=sys.stderr)
            return 2
        encoded = base64.b64encode(args.basic.encode("utf-8")).decode("ascii")
        headers["Authorization"] = f"Basic {encoded}"

    out_path = None
    if args.output:
        try:
            out_path = safe_path(args.output)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2

    try:
        status, resp_headers, body, trail = fetch(
            url, method="GET", headers=headers,
            timeout=args.timeout, retries=args.retries,
            follow_redirects=not args.no_redirects,
            allow_insecure=args.insecure,
        )
    except (urllib.error.URLError, OSError) as e:
        print(f"Error: network error: {e}", file=sys.stderr)
        return 2

    if args.status_only:
        print(status)
        return 0 if (200 <= status < 300 or not args.fail) else 1

    if args.print_headers:
        print(headers_to_json(resp_headers), file=sys.stderr)

    # Body output
    content_type = (resp_headers.get("Content-Type")
                    or resp_headers.get("content-type") or "")
    if args.as_json:
        # Try to parse and pretty-print
        try:
            obj = json.loads(body.decode("utf-8"))
            pretty = json.dumps(obj, indent=2, ensure_ascii=False).encode("utf-8")
            write_or_print(out_path, pretty, text=True)
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Fall back to raw
            write_or_print(out_path, body, text="text" in content_type)
    else:
        is_text = ("text" in content_type or "json" in content_type or
                   "xml" in content_type or "javascript" in content_type)
        write_or_print(out_path, body, text=is_text)

    if not args.quiet:
        if args.json_summary:
            summary = {
                "url": url, "method": "GET", "status": status,
                "bytes": len(body), "content_type": content_type,
                "redirects": len(trail) - 1,
                "output": str(out_path) if out_path else None,
            }
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            print(f"get {url} -> {status} ({len(body):,} bytes, "
                  f"{content_type or 'no content-type'})"
                  + (f" -> {out_path}" if out_path else ""), file=sys.stderr)

    if args.fail and not (200 <= status < 300):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
