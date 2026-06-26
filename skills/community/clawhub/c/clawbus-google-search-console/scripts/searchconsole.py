#!/usr/bin/env python3
"""Query Google Search Console sitemap status through MyBrandMetrics."""

import argparse
import json
import os
import re
import sys
import time

import requests


BASE_URL = "https://api.mybrandmetrics.com/explorer/query"
DEFAULT_TIMEOUT = 30


class SearchConsoleClient:
    """Small client for MyBrandMetrics Google Search Console sitemap queries."""

    def __init__(self, api_key: str, connection_id: str, account_id: str | None = None):
        if not api_key:
            raise ValueError("API key is required")
        if not connection_id:
            raise ValueError("Connection ID is required")

        self.api_key = api_key
        self.connection_id = connection_id
        self.account_id = account_id or connection_id

    def headers(self) -> dict[str, str]:
        return {
            "X-API_KEY": self.api_key,
            "Content-Type": "application/json",
        }

    def query(
        self,
        source_key: str,
        metrics: list[str] | None = None,
        dimensions: list[str] | None = None,
        filters: list[dict] | None = None,
        limit: int = 200,
        retry_count: int = 3,
    ) -> dict:
        body = {
            "source_key": source_key,
            "connection_id": self.connection_id,
            "account_id": self.account_id,
            "limit": limit,
        }
        if metrics:
            body["metrics"] = metrics
        if dimensions:
            body["dimensions"] = dimensions
        if filters:
            body["filters"] = filters

        for attempt in range(retry_count):
            try:
                response = requests.post(
                    BASE_URL,
                    headers=self.headers(),
                    json=body,
                    timeout=DEFAULT_TIMEOUT,
                )
                if response.status_code == 429 or response.status_code >= 503:
                    wait_seconds = 2**attempt
                    print(
                        f"Received {response.status_code}; retrying in {wait_seconds}s "
                        f"({attempt + 1}/{retry_count})",
                        file=sys.stderr,
                    )
                    time.sleep(wait_seconds)
                    continue

                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as exc:
                if attempt == retry_count - 1:
                    raise
                wait_seconds = 2**attempt
                print(
                    f"Request failed: {exc}; retrying in {wait_seconds}s "
                    f"({attempt + 1}/{retry_count})",
                    file=sys.stderr,
                )
                time.sleep(wait_seconds)

        raise RuntimeError("Request failed after retries")

    def list_sitemaps(
        self,
        metrics: list[str] | None = None,
        dimensions: list[str] | None = None,
        filters: list[dict] | None = None,
        limit: int = 200,
    ) -> dict:
        metrics = metrics or [
            "warnings",
            "errors",
            "contents_submitted",
            "contents_indexed",
            "sitemaps_count",
        ]
        dimensions = dimensions or [
            "site_url",
            "sitemap_path",
            "content_type",
            "last_downloaded",
            "is_pending",
        ]
        return self.query(
            "google_search_console_sitemaps",
            metrics=metrics,
            dimensions=dimensions,
            filters=filters,
            limit=limit,
        )


def split_csv(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_filters(raw_filters: list[str] | None) -> list[dict] | None:
    if not raw_filters:
        return None

    filters = []
    for raw_filter in raw_filters:
        match = re.match(r"([^:]+):([^:]+):(.+)", raw_filter)
        if not match:
            raise ValueError(
                f"Invalid filter format: {raw_filter}. Use field:operator:value."
            )
        filters.append(
            {
                "field": match.group(1),
                "operator": match.group(2),
                "value": match.group(3),
            }
        )
    return filters


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Query Google Search Console sitemap status through MyBrandMetrics."
    )
    parser.add_argument("--api-key", help="MyBrandMetrics API key")
    parser.add_argument(
        "--connection-id",
        required=True,
        help="Google Search Console connection ID, such as sc-domain:example.com",
    )
    parser.add_argument(
        "--account-id",
        help="Account ID. Defaults to the connection ID when omitted.",
    )
    parser.add_argument(
        "--metrics",
        help="Comma-separated metrics. Defaults to sitemap health metrics.",
    )
    parser.add_argument(
        "--dimensions",
        help="Comma-separated dimensions. Defaults to sitemap identity dimensions.",
    )
    parser.add_argument("--limit", type=int, default=200, help="Maximum rows to return")
    parser.add_argument(
        "--filter",
        action="append",
        dest="filters",
        help="Repeatable filter in field:operator:value format",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Print compact JSON instead of indented JSON",
    )
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("MYBRANDMETRICS_API_KEY")
    if not api_key:
        print(
            "Error: provide --api-key or set MYBRANDMETRICS_API_KEY.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        filters = parse_filters(args.filters)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    client = SearchConsoleClient(
        api_key=api_key,
        connection_id=args.connection_id,
        account_id=args.account_id,
    )
    result = client.list_sitemaps(
        metrics=split_csv(args.metrics),
        dimensions=split_csv(args.dimensions),
        filters=filters,
        limit=args.limit,
    )

    indent = None if args.compact else 2
    print(json.dumps(result, indent=indent, sort_keys=True))


if __name__ == "__main__":
    main()
