#!/usr/bin/env python3

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


ENDPOINT = "https://webunlocker.dataify.com/request"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Invoke the Dataify Web Unlocker API."
    )
    parser.add_argument("--url", required=True, help="Target URL to unlock.")
    parser.add_argument("--type", default="html", help="Response type.")
    parser.add_argument("--js-render", default="True", help="Whether to render JavaScript.")
    parser.add_argument("--block-resources", default="", help="Resource blocking setting.")
    parser.add_argument("--clean-content", default="", help="Clean content setting.")
    parser.add_argument("--country", default="us", help="Country code.")
    parser.add_argument("--headers", default="", help="Request headers as a string.")
    parser.add_argument("--cookies", default="", help="Cookies as a string.")
    parser.add_argument("--wait", default="", help="Wait time before capture.")
    parser.add_argument("--wait-for", default="", help="Selector or condition to wait for.")
    parser.add_argument("--follow-redirect", default="True", help="Whether to follow redirects.")
    parser.add_argument("--isjson", default="1", help="Response mode flag.")
    parser.add_argument("--dry-run", action="store_true", help="Print the request payload without calling the API.")
    return parser


def build_payload(args: argparse.Namespace) -> dict:
    return {
        "url": args.url,
        "type": args.type,
        "js_render": args.js_render,
        "block_resources": args.block_resources,
        "clean_content": args.clean_content,
        "country": args.country,
        "headers": args.headers,
        "cookies": args.cookies,
        "wait": args.wait,
        "wait_for": args.wait_for,
        "follow_redirect": args.follow_redirect,
        "isjson": args.isjson,
    }


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    token = os.environ.get("DATAIFY_API_TOKEN", "").strip()
    payload = build_payload(args)

    if args.dry_run:
        preview = {
            "endpoint": ENDPOINT,
            "authorization": "Bearer <redacted>" if token else "Bearer <missing DATAIFY_API_TOKEN>",
            "body": payload,
        }
        print(json.dumps(preview, indent=2))
        return 0

    if not token:
        print(
            "DATAIFY_API_TOKEN is not set. Sign in at https://dashboard.dataify.com?utm_source=skill to obtain it, then export it as an environment variable.",
            file=sys.stderr,
        )
        return 1

    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            content = response.read()
            if not content:
                print(response.status)
                return 0

            charset = response.headers.get_content_charset() or "utf-8"
            print(content.decode(charset, errors="replace"))
            return 0
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        if error_body:
            print(error_body, file=sys.stderr)
        else:
            print(f"HTTP {exc.code}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Request failed: {exc.reason}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
