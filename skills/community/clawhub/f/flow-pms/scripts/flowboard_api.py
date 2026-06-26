#!/usr/bin/env python3
import argparse
import json
import os
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE_URL = os.environ.get(
    "FLOWBOARD_BASE_URL",
    "https://mycivgjuujlnyoycuwrz.supabase.co/functions/v1/api-gateway",
)


def parse_json(value, flag_name):
    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON for {flag_name}: {exc}")


def resolve_api_key(explicit_key):
    api_key = explicit_key or os.environ.get("FLOWBOARD_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing API key. Pass --api-key or export FLOWBOARD_API_KEY."
        )
    return api_key


def build_url(path, query):
    url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    if query:
        url = f"{url}?{urlencode(query, doseq=True)}"
    return url


def main():
    parser = argparse.ArgumentParser(description="Call the FlowBoard API")
    parser.add_argument("method", help="HTTP method, e.g. GET, POST, PATCH, DELETE")
    parser.add_argument("path", help="API path, e.g. /projects or /tasks/{id}")
    parser.add_argument("--api-key", help="Bearer token for Authorization header")
    parser.add_argument("--query", help="JSON object with query params")
    parser.add_argument("--body", help="JSON object request body")
    args = parser.parse_args()

    method = args.method.upper()
    query = parse_json(args.query, "--query")
    body = parse_json(args.body, "--body")
    api_key = resolve_api_key(args.api_key)

    if query is not None and not isinstance(query, dict):
        raise SystemExit("--query must be a JSON object")
    if body is not None and not isinstance(body, dict):
        raise SystemExit("--body must be a JSON object")

    url = build_url(args.path, query)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(url, data=data, headers=headers, method=method)

    try:
        with urlopen(request) as response:
            raw = response.read().decode("utf-8")
            status = response.getcode()
            content_type = response.headers.get("Content-Type", "")
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        payload = raw
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            pass
        print(
            json.dumps(
                {
                    "ok": False,
                    "status": exc.code,
                    "path": args.path,
                    "error": payload,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)
    except URLError as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "path": args.path,
                    "error": str(exc.reason),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)

    if "application/json" in content_type.lower() and raw:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = raw
    else:
        payload = raw

    print(
        json.dumps(
            {
                "ok": True,
                "status": status,
                "path": args.path,
                "data": payload,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
