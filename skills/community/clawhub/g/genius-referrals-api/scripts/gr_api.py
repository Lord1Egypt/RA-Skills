#!/usr/bin/env python3
"""Small stdlib Genius Referrals API helper for OpenClaw skills."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request


def parse_pairs(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Expected key=value, got: {value}")
        key, item_value = value.split("=", 1)
        result[key] = item_value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Call the Genius Referrals API.")
    parser.add_argument("method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"])
    parser.add_argument("path", help="API path, e.g. /accounts/{account_slug}/advocates")
    parser.add_argument("--base-url", default=os.environ.get("GR_API_BASE_URL", "https://api.geniusreferrals.com"))
    parser.add_argument("--token", default=os.environ.get("GR_API_TOKEN"))
    parser.add_argument("--account", default=os.environ.get("GR_ACCOUNT_SLUG"))
    parser.add_argument("--path-param", action="append", default=[], help="Path replacement as key=value")
    parser.add_argument("--query", action="append", default=[], help="Query param as key=value")
    parser.add_argument("--json", default=None, help="JSON request body")
    args = parser.parse_args()

    if not args.token:
        raise SystemExit("Missing GR_API_TOKEN or --token")

    path_params = parse_pairs(args.path_param)
    if args.account:
        path_params.setdefault("account_slug", args.account)

    path = args.path
    for key, value in path_params.items():
        path = path.replace("{" + key + "}", urllib.parse.quote(value, safe=""))

    if "{" in path or "}" in path:
        raise SystemExit(f"Unresolved path parameter in: {path}")

    query = urllib.parse.urlencode(parse_pairs(args.query))
    url = args.base_url.rstrip("/") + "/" + path.lstrip("/")
    if query:
        url += "?" + query

    body = None
    headers = {
        "Accept": "application/json",
        "X-Auth-Token": args.token,
    }
    if args.json is not None:
        try:
            json.loads(args.json)
        except json.JSONDecodeError as error:
            raise SystemExit(f"Invalid JSON request body: {error.msg} at position {error.pos}") from None
        body = args.json.encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=body, headers=headers, method=args.method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8", errors="replace")
            print(json.dumps({
                "status": response.status,
                "url": url,
                "body": json.loads(payload) if payload else None,
            }, indent=2, sort_keys=True))
            return 0
    except urllib.error.HTTPError as error:
        payload = error.read().decode("utf-8", errors="replace")
        print(json.dumps({
            "status": error.code,
            "url": url,
            "body": payload,
        }, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
