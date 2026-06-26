#!/usr/bin/env python3
"""
Example usage patterns for the Jiimore API client.

This script demonstrates common use cases and best practices for
querying Amazon niche markets via the Jiimore tool.
"""

import json
import sys
from typing import List, Dict, Any
from jiimore_client import JiimoreClient


def example_basic_search():
    """Example 1: Basic niche market search."""
    print("\n=== Example 1: Basic Search ===")

    client = JiimoreClient()

    # Simple search with defaults
    results = client.query(
        keyword="bluetooth speaker",
        country="US",
        page_size=10
    )

    print(f"Found {results['total']} niches for 'bluetooth speaker'")
    print(f"\nTop 3 results by 7-day sales:\n")

    for i, niche in enumerate(results['data'][:3], 1):
        print(f"{i}. {niche['nicheTitle']}")
        print(f"   Demand: {niche['demand']}")
        print(f"   Price: ${niche['avgPrice']:.2f}")
        print(f"   Weekly Sales: {niche['unitsSoldWeekly']:,}")
        print()


def example_low_competition():
    """Example 2: Find low-competition opportunities."""
    print("\n=== Example 2: Low Competition Search ===")

    client = JiimoreClient()

    # Use built-in low-competition helper
    results = client.find_low_competition(
        keyword="yoga accessories",
        country="US",
        max_brands=40,
        max_brand_share=0.25,
        min_demand=65
    )

    print(f"Low-competition niches found: {results['total']}")
    print("\nBest opportunities:\n")

    for i, niche in enumerate(results['data'][:5], 1):
        brand_share = niche['top5BrandsClickShare'] * 100
        print(f"{i}. {niche['nicheTitle']}")
        print(f"   Demand: {niche['demand']}")
        print(f"   Brands: {niche['brandCount']}")
        print(f"   TOP5 Brand Share: {brand_share:.1f}%")
        print()


def example_profitable_niches():
    """Example 3: Find profitable niches with good margins."""
    print("\n=== Example 3: Profitable Niche Search ===")

    client = JiimoreClient()

    # Search for profitable opportunities
    results = client.find_profitable(
        keyword="kitchen gadgets",
        country="DE",
        min_price=20,
        max_price=60,
        min_profit_ratio=0.35,
        max_return_rate=0.08
    )

    print(f"Profitable niches found: {results['total']}")
    print("\nTop opportunities:\n")

    for i, niche in enumerate(results['data'][:5], 1):
        profit_ratio = niche.get('profitMarginGt50PctSkuRatio', 0) * 100
        return_rate = niche.get('returnRateAnnual', 0) * 100
        acos = niche.get('acos', 0) * 100

        print(f"{i}. {niche['nicheTitle']}")
        print(f"   Price: €{niche['avgPrice']:.2f}")
        print(f"   Profit Ratio >50%: {profit_ratio:.1f}%")
        print(f"   Return Rate: {return_rate:.1f}%")
        print(f"   ACOS: {acos:.1f}%")
        print()


def example_custom_filters():
    """Example 4: Advanced filtering with custom parameters."""
    print("\n=== Example 4: Custom Filter Search ===")

    client = JiimoreClient()

    # Complex filter combination
    filters = {
        "productCountMin": 50,
        "productCountMax": 300,
        "unitsSoldT7Min": 2000,
        "searchVolumeGrowthT7Min": 0.05,  # 5% growth
        "top5ProductsClickShareMax": 0.35,
        "returnRateT360Max": 0.12
    }

    results = client.query(
        keyword="wireless charging",
        country="US",
        sort_field="searchVolumeGrowthT7",
        sort_type="desc",
        filters=filters,
        page_size=10
    )

    print(f"Niches matching criteria: {results['total']}")
    print("\nGrowing markets with healthy competition:\n")

    for i, niche in enumerate(results['data'][:5], 1):
        growth = niche.get('searchVolumeGrowthWeekly', 0) * 100
        product_share = niche.get('top5ProductsClickShare', 0) * 100

        print(f"{i}. {niche['nicheTitle']}")
        print(f"   Products: {niche['productCount']}")
        print(f"   Weekly Sales: {niche['unitsSoldWeekly']:,}")
        print(f"   Search Growth: {growth:.1f}%")
        print(f"   TOP5 Product Share: {product_share:.1f}%")
        print()


def example_multi_market_comparison():
    """Example 5: Compare same keyword across multiple markets."""
    print("\n=== Example 5: Multi-Market Comparison ===")

    client = JiimoreClient()
    keyword = "coffee grinder"
    markets = ["US", "JP", "DE"]

    print(f"Comparing '{keyword}' across markets:\n")

    for market in markets:
        results = client.query(
            keyword=keyword,
            country=market,
            page_size=1,
            sort_field="demand",
            sort_type="desc"
        )

        if results['data']:
            top = results['data'][0]
            print(f"{market}:")
            print(f"  Total Niches: {results['total']}")
            print(f"  Top Demand: {top['demand']}")
            print(f"  Avg Price: ${top['avgPrice']:.2f}")
            print(f"  Weekly Sales: {top['unitsSoldWeekly']:,}")
            print(f"  Brand Count: {top['brandCount']}")
            print()


def example_trend_analysis():
    """Example 6: Analyze trends using weekly vs quarterly data."""
    print("\n=== Example 6: Trend Analysis ===")

    client = JiimoreClient()

    results = client.query(
        keyword="fitness tracker",
        country="US",
        page_size=5,
        sort_field="demand",
        sort_type="desc"
    )

    print("Comparing weekly vs quarterly trends:\n")

    for i, niche in enumerate(results['data'][:3], 1):
        # Calculate growth indicators
        weekly_sales = niche['unitsSoldWeekly']
        quarterly_sales = niche['unitsSoldQuarterly']
        weekly_search_growth = niche.get('searchVolumeGrowthWeekly', 0) * 100
        quarterly_search_growth = niche.get('searchVolumeGrowthQuarterly', 0) * 100

        # Estimate weekly average from quarterly
        quarterly_weekly_avg = quarterly_sales / 13 if quarterly_sales else 0
        momentum = "↑" if weekly_sales > quarterly_weekly_avg else "↓"

        print(f"{i}. {niche['nicheTitle']}")
        print(f"   Current Week Sales: {weekly_sales:,}")
        print(f"   Quarterly Avg/Week: {quarterly_weekly_avg:,.0f} {momentum}")
        print(f"   Search Growth (7d): {weekly_search_growth:.1f}%")
        print(f"   Search Growth (90d): {quarterly_search_growth:.1f}%")
        print()


def example_export_to_json():
    """Example 7: Export results to JSON file for further analysis."""
    print("\n=== Example 7: Export to JSON ===")

    client = JiimoreClient()

    results = client.query(
        keyword="smart home",
        country="US",
        page_size=50
    )

    # Save to file
    output_file = "jiimore_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(results['data'])} niches to {output_file}")
    print(f"Total niches available: {results['total']}")


def example_format_markdown_table():
    """Example 8: Format results as Markdown table."""
    print("\n=== Example 8: Markdown Table Export ===")

    client = JiimoreClient()

    results = client.query(
        keyword="laptop stand",
        country="US",
        page_size=10,
        sort_field="demand",
        sort_type="desc"
    )

    # Generate Markdown table
    print("\n| Title | Demand | Price | Sales (7d) | Brands | TOP5 Share |")
    print("|-------|--------|-------|------------|--------|------------|")

    for niche in results['data'][:10]:
        title = niche['nicheTitle'][:30]
        demand = niche['demand']
        price = f"${niche['avgPrice']:.2f}"
        sales = f"{niche['unitsSoldWeekly']:,}"
        brands = niche['brandCount']
        share = f"{niche['top5BrandsClickShare'] * 100:.1f}%"

        print(f"| {title} | {demand} | {price} | {sales} | {brands} | {share} |")


def example_error_handling():
    """Example 9: Proper error handling and retry logic."""
    print("\n=== Example 9: Error Handling ===")

    try:
        client = JiimoreClient()

        # Use retry wrapper for resilience
        results = client.query_with_retry(
            keyword="phone case",
            country="US",
            max_retries=3,
            backoff_factor=2.0
        )

        print(f"Successfully retrieved {results['total']} results")

    except ValueError as e:
        print(f"Validation error: {e}")
        print("Check your API key and parameters")

    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Query failed after retries")


def example_find_emerging_markets():
    """Example 10: Identify emerging market opportunities."""
    print("\n=== Example 10: Emerging Market Finder ===")

    client = JiimoreClient()

    # Search for markets with high growth, low maturity
    filters = {
        "searchVolumeGrowthT7Min": 0.15,  # 15%+ growth
        "productCountMax": 150,  # Not saturated yet
        "launchRateT180Min": 0.25,  # New products succeeding
        "brandCountMax": 40  # Not brand-dominated
    }

    results = client.query(
        keyword="eco friendly",
        country="US",
        sort_field="searchVolumeGrowthT7",
        sort_type="desc",
        filters=filters,
        page_size=10
    )

    print(f"Emerging opportunities found: {results['total']}")
    print("\nFastest growing niches:\n")

    for i, niche in enumerate(results['data'][:5], 1):
        growth = niche.get('searchVolumeGrowthWeekly', 0) * 100
        launch_rate = niche.get('launchRateSemiannual', 0) * 100
        new_products = niche.get('newProductsLaunchedSemiannual', 0)

        print(f"{i}. {niche['nicheTitle']}")
        print(f"   Search Growth: {growth:.1f}%")
        print(f"   Products: {niche['productCount']}")
        print(f"   Launch Success Rate: {launch_rate:.1f}%")
        print(f"   New Products (180d): {new_products}")
        print()


def main():
    """Run all examples."""
    examples = [
        ("Basic Search", example_basic_search),
        ("Low Competition", example_low_competition),
        ("Profitable Niches", example_profitable_niches),
        ("Custom Filters", example_custom_filters),
        ("Multi-Market", example_multi_market_comparison),
        ("Trend Analysis", example_trend_analysis),
        ("Export JSON", example_export_to_json),
        ("Markdown Table", example_format_markdown_table),
        ("Error Handling", example_error_handling),
        ("Emerging Markets", example_find_emerging_markets),
    ]

    print("=" * 60)
    print("Jiimore API Client - Usage Examples")
    print("=" * 60)

    if len(sys.argv) > 1:
        # Run specific example
        example_num = int(sys.argv[1])
        if 1 <= example_num <= len(examples):
            name, func = examples[example_num - 1]
            print(f"\nRunning: {name}")
            func()
        else:
            print(f"Invalid example number. Choose 1-{len(examples)}")
    else:
        # List available examples
        print("\nAvailable examples:")
        for i, (name, _) in enumerate(examples, 1):
            print(f"  {i}. {name}")
        print(f"\nRun: python examples.py <number>")
        print("Example: python examples.py 1")


if __name__ == "__main__":
    main()
