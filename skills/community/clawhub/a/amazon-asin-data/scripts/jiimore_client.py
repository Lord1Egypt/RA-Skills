#!/usr/bin/env python3
"""
Jiimore API Client for Amazon Niche Market Analysis

This module provides a Python client for the Jiimore tool within LinkFoxAgent,
enabling programmatic access to Amazon marketplace niche data.
"""

import os
import sys
import json
import time
import requests
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict


@dataclass
class JiimoreQuery:
    """Represents a Jiimore API query with all parameters."""

    keyword: str
    countryCode: str = "US"
    page: int = 1
    pageSize: int = 50
    sortType: str = "desc"
    sortField: str = "unitsSoldT7"

    # Optional filter parameters
    productCountMin: Optional[int] = None
    productCountMax: Optional[int] = None
    avgPriceMin: Optional[float] = None
    avgPriceMax: Optional[float] = None
    brandCountMin: Optional[int] = None
    brandCountMax: Optional[int] = None
    unitsSoldT7Min: Optional[int] = None
    unitsSoldT7Max: Optional[int] = None
    searchVolumeT7Min: Optional[int] = None
    searchVolumeT7Max: Optional[int] = None
    top5BrandsClickShareMin: Optional[float] = None
    top5BrandsClickShareMax: Optional[float] = None
    top5ProductsClickShareMin: Optional[float] = None
    top5ProductsClickShareMax: Optional[float] = None
    returnRateT360Min: Optional[float] = None
    returnRateT360Max: Optional[float] = None
    launchRateT180Min: Optional[float] = None
    launchRateT180Max: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert query to dictionary, excluding None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}


class JiimoreClient:
    """Client for interacting with the Jiimore API."""

    BASE_URL = "https://test-tool-gateway.linkfox.com"
    ENDPOINT = "/jiimore/getNicheInfoByKeyword"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Jiimore client.

        Args:
            api_key: LinkFoxAgent API key. If not provided, reads from
                     LINKFOXAGENT_API_KEY environment variable.

        Raises:
            ValueError: If API key is not provided or found in environment.
        """
        self.api_key = api_key or os.getenv("LINKFOXAGENT_API_KEY")

        if not self.api_key:
            raise ValueError(
                "API key required. Set LINKFOXAGENT_API_KEY environment variable "
                "or pass api_key parameter.\n\n"
                "Setup:\n"
                "  export LINKFOXAGENT_API_KEY='your_api_key_here'\n"
            )

        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }

    def query(
        self,
        keyword: str,
        country: str = "US",
        page: int = 1,
        page_size: int = 50,
        sort_field: str = "unitsSoldT7",
        sort_type: str = "desc",
        filters: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """
        Query Amazon niche markets by keyword.

        Args:
            keyword: Search keyword (required)
            country: Country code (US, JP, DE)
            page: Page number (1-indexed)
            page_size: Results per page (10-100)
            sort_field: Field to sort by
            sort_type: Sort direction (desc/asc)
            filters: Additional filter parameters
            timeout: Request timeout in seconds

        Returns:
            API response as dictionary with keys:
                - total: Total number of results
                - data: List of niche market objects
                - columns: Column configuration
                - costToken: API cost
                - type: Response type
                - title: Response title

        Raises:
            requests.exceptions.RequestException: On API errors
        """
        # Build query object
        query = JiimoreQuery(
            keyword=keyword,
            countryCode=country,
            page=page,
            pageSize=page_size,
            sortField=sort_field,
            sortType=sort_type,
        )

        # Apply filters if provided
        if filters:
            for key, value in filters.items():
                if hasattr(query, key):
                    setattr(query, key, value)

        # Make API request
        url = f"{self.BASE_URL}{self.ENDPOINT}"
        payload = query.to_dict()

        try:
            response = requests.post(
                url, json=payload, headers=self.headers, timeout=timeout
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError(
                    "Authentication failed. Check your API key."
                ) from e
            elif e.response.status_code == 400:
                error_msg = e.response.json().get(
                    "message", "Invalid request parameters"
                )
                raise ValueError(f"Bad request: {error_msg}") from e
            elif e.response.status_code == 429:
                raise ValueError(
                    "Rate limit exceeded. Please retry later."
                ) from e
            else:
                raise

    def query_with_retry(
        self,
        keyword: str,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Query with automatic retry on transient failures.

        Args:
            keyword: Search keyword
            max_retries: Maximum number of retry attempts
            backoff_factor: Exponential backoff multiplier
            **kwargs: Additional arguments passed to query()

        Returns:
            API response dictionary

        Raises:
            Exception: If all retry attempts fail
        """
        last_exception = None

        for attempt in range(max_retries):
            try:
                return self.query(keyword, **kwargs)

            except requests.exceptions.RequestException as e:
                last_exception = e

                if attempt < max_retries - 1:
                    wait_time = backoff_factor**attempt
                    print(
                        f"Request failed (attempt {attempt + 1}/{max_retries}). "
                        f"Retrying in {wait_time}s...",
                        file=sys.stderr,
                    )
                    time.sleep(wait_time)
                    continue
                else:
                    break

        raise Exception(
            f"Query failed after {max_retries} attempts"
        ) from last_exception

    def find_low_competition(
        self,
        keyword: str,
        country: str = "US",
        max_brands: int = 50,
        max_brand_share: float = 0.3,
        max_product_share: float = 0.4,
        min_demand: int = 60,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Find low-competition niches with specific criteria.

        Args:
            keyword: Search keyword
            country: Country code
            max_brands: Maximum number of brands
            max_brand_share: Maximum TOP5 brand share (0-1)
            max_product_share: Maximum TOP5 product share (0-1)
            min_demand: Minimum demand score
            **kwargs: Additional filter parameters

        Returns:
            API response with filtered results
        """
        filters = {
            "brandCountMax": max_brands,
            "top5BrandsClickShareMax": max_brand_share,
            "top5ProductsClickShareMax": max_product_share,
            **kwargs,
        }

        results = self.query(
            keyword=keyword,
            country=country,
            sort_field="demand",
            sort_type="desc",
            filters=filters,
        )

        # Client-side filter by demand if needed
        if min_demand > 0 and "data" in results:
            results["data"] = [
                item for item in results["data"] if item.get("demand", 0) >= min_demand
            ]
            results["total"] = len(results["data"])

        return results

    def find_profitable(
        self,
        keyword: str,
        country: str = "US",
        min_price: float = 15.0,
        max_price: float = 50.0,
        min_profit_ratio: float = 0.3,
        max_return_rate: float = 0.1,
        max_acos: float = 0.25,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Find profitable niches with specific profit criteria.

        Args:
            keyword: Search keyword
            country: Country code
            min_price: Minimum average price
            max_price: Maximum average price
            min_profit_ratio: Minimum 50% natural profit ratio (0-1)
            max_return_rate: Maximum return rate (0-1)
            max_acos: Maximum ACOS (0-1)
            **kwargs: Additional filter parameters

        Returns:
            API response with filtered results
        """
        filters = {
            "avgPriceMin": min_price,
            "avgPriceMax": max_price,
            "returnRateT360Max": max_return_rate,
            **kwargs,
        }

        results = self.query(
            keyword=keyword,
            country=country,
            sort_field="profitRate50",
            sort_type="desc",
            filters=filters,
        )

        # Client-side filters
        if "data" in results:
            filtered = []
            for item in results["data"]:
                profit_ok = item.get("profitMarginGt50PctSkuRatio", 0) >= min_profit_ratio
                acos_ok = item.get("acos", 1) <= max_acos
                if profit_ok and acos_ok:
                    filtered.append(item)

            results["data"] = filtered
            results["total"] = len(filtered)

        return results

    def format_niche_summary(self, niche: Dict[str, Any]) -> str:
        """
        Format a niche market data object into a human-readable summary.

        Args:
            niche: Niche market data dictionary

        Returns:
            Formatted summary string
        """
        lines = [
            f"Title: {niche.get('nicheTitle', 'N/A')}",
            f"Chinese: {niche.get('translationZh', 'N/A')}",
            f"Demand Score: {niche.get('demand', 0)}",
            f"Price Range: ${niche.get('minimumPrice', 0):.2f} - ${niche.get('maximumPrice', 0):.2f} (avg: ${niche.get('avgPrice', 0):.2f})",
            f"Products: {niche.get('productCount', 0)} | Brands: {niche.get('brandCount', 0)}",
            f"Weekly Sales: {niche.get('unitsSoldWeekly', 0):,}",
            f"Search Volume (7d): {niche.get('searchVolumeWeekly', 0):,}",
            f"Brand Concentration: {niche.get('top5BrandsClickShare', 0) * 100:.1f}%",
            f"Return Rate: {niche.get('returnRateAnnual', 0) * 100:.1f}%",
            f"ACOS: {niche.get('acos', 0) * 100:.1f}%",
        ]

        return "\n".join(lines)


def main():
    """Command-line interface for Jiimore API."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Query Amazon niche markets via Jiimore API"
    )
    parser.add_argument("keyword", help="Search keyword")
    parser.add_argument(
        "-c", "--country", default="US", choices=["US", "JP", "DE"], help="Country code"
    )
    parser.add_argument(
        "-n", "--num", type=int, default=10, help="Number of results to display"
    )
    parser.add_argument(
        "--low-competition",
        action="store_true",
        help="Find low-competition niches",
    )
    parser.add_argument(
        "--profitable", action="store_true", help="Find profitable niches"
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    try:
        client = JiimoreClient()

        # Execute query based on mode
        if args.low_competition:
            results = client.find_low_competition(
                args.keyword, country=args.country, page_size=args.num
            )
        elif args.profitable:
            results = client.find_profitable(
                args.keyword, country=args.country, page_size=args.num
            )
        else:
            results = client.query(
                args.keyword, country=args.country, page_size=args.num
            )

        # Output results
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"\n=== Jiimore Results: {args.keyword} ({args.country}) ===")
            print(f"Total: {results.get('total', 0)} niches\n")

            for i, niche in enumerate(results.get("data", [])[:args.num], 1):
                print(f"\n--- Result {i} ---")
                print(client.format_niche_summary(niche))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
