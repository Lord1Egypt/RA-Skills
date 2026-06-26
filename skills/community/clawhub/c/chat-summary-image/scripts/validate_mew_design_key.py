#!/usr/bin/env python3
"""Validate a mew.design API key without starting a real image generation task."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = "https://api.mew.design/"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a mew.design API key using an auth-only probe request.",
    )
    parser.add_argument("--api-key", required=True, help="mew.design API key to validate.")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Gateway base URL.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds.",
    )
    return parser.parse_args()


def build_endpoint(base_url: str) -> str:
    normalized = base_url.rstrip("/") + "/"
    return urllib.parse.urljoin(normalized, "open/api/design/generate")


def probe_key(endpoint: str, api_key: str, timeout: int) -> dict:
    # Send an intentionally invalid body. A valid key should pass auth and fail on payload validation.
    request = urllib.request.Request(
        endpoint,
        data=b"{}",
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "User-Agent": "curl/8.7.1",
            "Accept": "*/*",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            return json.loads(raw)
        except json.JSONDecodeError as err:
            raise RuntimeError(f"HTTP {exc.code}: {raw}") from err
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as err:
        raise RuntimeError(f"Non-JSON response: {raw}") from err


def main() -> int:
    args = parse_args()
    endpoint = build_endpoint(args.base_url)

    try:
        response = probe_key(endpoint, args.api_key.strip(), args.timeout)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1

    status_code = response.get("statusCode")
    message = response.get("message", "")

    if status_code == "C40001":
        print(json.dumps({"valid": True, "statusCode": status_code, "message": message}, ensure_ascii=False))
        return 0

    if status_code in {"C40100", "C40101", "C40102", "C40103"}:
        print(json.dumps({"valid": False, "statusCode": status_code, "message": message}, ensure_ascii=False))
        return 2

    print(json.dumps({"valid": False, "statusCode": status_code, "message": message}, ensure_ascii=False))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
