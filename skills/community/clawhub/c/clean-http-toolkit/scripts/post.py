#!/usr/bin/env python3
"""
post.py - HTTP POST / PUT / PATCH / DELETE with a JSON or form body.

Pure Python 3 stdlib (urllib). Designed for AI agents calling REST APIs.

Usage:
    post.py URL [options]

Body sources (pick one):
    --json '{"key": "value"}'   send a JSON body
    --json-file PATH            read a JSON file and send as body
    --form K=V                  add a form field (may repeat); body is sent
                                as application/x-www-form-urlencoded
    --raw-file PATH             send the file as the raw body
                                (use --content-type to set the MIME type)
    --content-type TYPE         override the Content-Type header

Other options:
    --method METHOD             POST (default) / PUT / PATCH / DELETE
    --output PATH               write response body to file (default: stdout)
    --header 'Name: V'          custom header (may repeat)
    --bearer TOKEN              shorthand for Authorization: Bearer ...
    --basic USER:PASS           HTTP Basic auth shorthand
    --timeout SECONDS           default: 30
    --retries N                 default: 3 (only retries on 5xx / 429 / timeout)
    --no-redirects              do not follow 3xx
    --insecure                  skip TLS cert verification
    --print-headers             print response headers (JSON) to stderr
    --fail                      exit 1 on non-2xx
    --json-summary              machine-readable summary on stderr
    --quiet                     suppress the text summary
    -h, --help                  show this help

Exit codes:
    0   response received (and 2xx if --fail not set)
    1   --fail and response was non-2xx
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
    p.add_argument("--method", default="POST",
                   choices=("POST", "PUT", "PATCH", "DELETE"))
    p.add_argument("--json", dest="json_body")
    p.add_argument("--json-file", dest="json_file")
    p.add_argument("--form", action="append", default=[])
    p.add_argument("--raw-file", dest="raw_file")
    p.add_argument("--content-type", dest="content_type")
    p.add_argument("--output")
    p.add_argument("--header", action="append", default=[])
    p.add_argument("--bearer")
    p.add_argument("--basic")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    p.add_argument("--retries", type=int, default=3)
    p.add_argument("--no-redirects", dest="no_redirects", action="store_true")
    p.add_argument("--insecure", action="store_true")
    p.add_argument("--print-headers", dest="print_headers", action="store_true")
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

    # Build body
    body_sources = sum(1 for b in (args.json_body, args.json_file, args.raw_file,
                                    args.form) if b)
    if body_sources > 1:
        print("Error: --json, --json-file, --raw-file, and --form are mutually "
              "exclusive (except form supports multiple --form k=v).",
              file=sys.stderr)
        return 2

    try:
        headers = parse_headers(args.header)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    body: bytes = b""
    content_type = args.content_type

    if args.json_body is not None:
        try:
            obj = json.loads(args.json_body)
        except json.JSONDecodeError as e:
            print(f"Error: --json must be valid JSON: {e}", file=sys.stderr)
            return 2
        body = json.dumps(obj).encode("utf-8")
        content_type = content_type or "application/json"
    elif args.json_file:
        try:
            jp = safe_path(args.json_file)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
        if not jp.is_file():
            print(f"Error: --json-file not found: {jp}", file=sys.stderr)
            return 2
        body = jp.read_bytes()
        # Validate it parses
        try:
            json.loads(body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Error: --json-file is not valid JSON: {e}", file=sys.stderr)
            return 2
        content_type = content_type or "application/json"
    elif args.form:
        pairs = []
        for f in args.form:
            if "=" not in f:
                print(f"Error: --form expects K=V, got: {f!r}", file=sys.stderr)
                return 2
            k, _, v = f.partition("=")
            pairs.append((k, v))
        body = urllib.parse.urlencode(pairs).encode("utf-8")
        content_type = content_type or "application/x-www-form-urlencoded"
    elif args.raw_file:
        try:
            rp = safe_path(args.raw_file)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
        if not rp.is_file():
            print(f"Error: --raw-file not found: {rp}", file=sys.stderr)
            return 2
        body = rp.read_bytes()
        # No default content_type; user should set --content-type
    # else: empty body (legal for DELETE etc.)

    if content_type:
        headers.setdefault("Content-Type", content_type)
    if body:
        headers.setdefault("Content-Length", str(len(body)))

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
        status, resp_headers, resp_body, trail = fetch(
            url, method=args.method, headers=headers, body=body,
            timeout=args.timeout, retries=args.retries,
            follow_redirects=not args.no_redirects,
            allow_insecure=args.insecure,
        )
    except (urllib.error.URLError, OSError) as e:
        print(f"Error: network error: {e}", file=sys.stderr)
        return 2

    if args.print_headers:
        print(headers_to_json(resp_headers), file=sys.stderr)

    resp_ct = (resp_headers.get("Content-Type")
               or resp_headers.get("content-type") or "")
    is_text = ("text" in resp_ct or "json" in resp_ct or "xml" in resp_ct)
    write_or_print(out_path, resp_body, text=is_text)

    if not args.quiet:
        if args.json_summary:
            summary = {
                "url": url, "method": args.method, "status": status,
                "request_bytes": len(body), "response_bytes": len(resp_body),
                "response_content_type": resp_ct,
                "redirects": len(trail) - 1,
                "output": str(out_path) if out_path else None,
            }
            print(json.dumps(summary, indent=2), file=sys.stderr)
        else:
            print(f"{args.method} {url} -> {status} "
                  f"(sent {len(body):,}, recv {len(resp_body):,})"
                  + (f" -> {out_path}" if out_path else ""), file=sys.stderr)

    if args.fail and not (200 <= status < 300):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
