#!/usr/bin/env python3
"""Browse Coclaw listings and call a service with x402 payment."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from urllib import error, request

API_BASE_URL = "https://coclawapi-production.up.railway.app"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Call a Coclaw service via x402")
    parser.add_argument(
        "--service-id", help="Service ID. If omitted, auto-select first active listing."
    )
    parser.add_argument(
        "--list", action="store_true", help="List all active services and exit"
    )
    parser.add_argument(
        "--input-json",
        default='{"task":"auto"}',
        help="JSON string for input payload",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show listing details without calling"
    )
    return parser.parse_args()


def http_json(
    method: str, url: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | list[Any]:
    data = None
    headers = {"accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["content-type"] = "application/json"

    req = request.Request(url=url, method=method, data=data, headers=headers)
    try:
        with request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {url}: {text}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Network error {url}: {exc.reason}") from exc


def fetch_listings() -> list[dict[str, Any]]:
    response = http_json("GET", f"{API_BASE_URL}/v1/openclaw/listings")
    if not isinstance(response, list):
        raise RuntimeError("Unexpected listings response")
    return response


def select_listing(service_id: str | None) -> dict[str, Any]:
    listings = fetch_listings()
    if not listings:
        raise RuntimeError(
            "No active listings found. A seller must register a service first."
        )

    if service_id:
        for listing in listings:
            if listing.get("listing_id") == service_id:
                return listing
        raise RuntimeError(f"Listing not found: {service_id}")

    for listing in listings:
        if listing.get("is_active", True):
            return listing

    raise RuntimeError("No active listing found.")


def call_service(endpoint: str, service_id: str, input_payload: dict) -> dict[str, Any]:
    req = request.Request(
        url=endpoint,
        method="POST",
        data=json.dumps({"service_id": service_id, "input": input_payload}).encode(
            "utf-8"
        ),
        headers={"content-type": "application/json"},
    )
    try:
        with request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        if exc.code == 402:
            raise RuntimeError(
                f"Payment required (402). The supplier endpoint requires x402 payment. "
                f"Use an x402-enabled client (e.g. @x402/fetch + @x402/stellar) to pay automatically. "
                f"Endpoint: {endpoint}"
            ) from exc
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc


def main() -> int:
    args = parse_args()

    try:
        if args.list:
            listings = fetch_listings()
            if not listings:
                print("No active listings found.")
                return 0
            for listing in listings:
                print(
                    f"  {listing.get('listing_id', '?'):30s}  "
                    f"{listing.get('title', '?'):30s}  "
                    f"{listing.get('price_usdt', '?')} USDC"
                )
            return 0

        listing = select_listing(args.service_id)
        endpoint = listing.get("endpoint", "")
        service_id = listing.get("listing_id", "")

        try:
            input_payload = json.loads(args.input_json)
        except json.JSONDecodeError as exc:
            print(f"Invalid --input-json: {exc}", file=sys.stderr)
            return 2

        if not isinstance(input_payload, dict):
            print("--input-json must decode to a JSON object", file=sys.stderr)
            return 2

        if args.dry_run:
            print(
                json.dumps(
                    {
                        "dry_run": True,
                        "listing": listing,
                        "endpoint": endpoint,
                        "input": input_payload,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        result = call_service(endpoint, service_id, input_payload)

        print(
            json.dumps(
                {
                    "listing": listing.get("listing_id"),
                    "status": result.get("status", "UNKNOWN"),
                    "output": result.get("output"),
                    "error": result.get("error"),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
