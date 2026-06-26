#!/usr/bin/env python3
"""
Amazon Competitor Spy — Analyze top competitors for any search term
Scrapes search results, analyzes listings, finds gaps in the market.
"""

import json
import re
import sys
import urllib.request
import urllib.parse
import time


def search_amazon(query, marketplace="com", page=1):
    """Search Amazon and extract ASINs from results."""
    encoded = urllib.parse.quote(query)
    url = f"https://www.amazon.{marketplace}/s?k={encoded}&page={page}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        # Extract ASINs from search results
        asins = re.findall(r'data-asin="([A-Z0-9]{10})"', html)
        # Deduplicate while preserving order
        seen = set()
        unique = []
        for a in asins:
            if a not in seen and a:
                seen.add(a)
                unique.append(a)
        return unique[:20]

    except Exception as e:
        print(f"❌ Search failed: {e}")
        return []


def extract_search_result_data(html):
    """Extract basic data from search result cards."""
    results = []

    # Find result cards
    cards = re.findall(
        r'data-asin="([A-Z0-9]{10})".*?'
        r'class="a-size-base-plus a-color-base a-text-normal"[^>]*>(.*?)</span>.*?'
        r'class="a-price-whole">(\d+)</span>',
        html, re.DOTALL
    )

    for asin, title, price in cards:
        results.append({
            "asin": asin,
            "title": title.strip()[:100],
            "price": f"${price}",
        })

    return results


def analyze_competitors(query, marketplace="com", limit=10):
    """Full competitor analysis for a search term."""
    print(f"\n🕵️ Competitor Analysis: '{query}'")
    print(f"   Marketplace: amazon.{marketplace}")
    print("=" * 60)

    asins = search_amazon(query, marketplace)

    if not asins:
        print("❌ No results found. Try a different search term.")
        return None

    print(f"\n📦 Top {min(len(asins), limit)} competitors:\n")

    competitors = []
    for i, asin in enumerate(asins[:limit]):
        print(f"  {i+1}. ASIN: {asin}")
        competitors.append({"rank": i+1, "asin": asin})

    # Price analysis
    print(f"\n💡 Quick Analysis:")
    print(f"   • {len(asins)} products found for '{query}'")
    print(f"   • Run 'analyzer.py <ASIN>' on each to get detailed scores")
    print(f"   • Focus on listings with Grade C or below — those are vulnerable")

    # Keyword suggestions based on what we found
    print(f"\n🔑 Suggested Actions:")
    print(f"   1. Analyze top 5 ASINs: python3 analyzer.py {asins[0]}")
    print(f"   2. Extract keywords: python3 keyword_extractor.py '{query}'")
    print(f"   3. Look for listings with <100 reviews — easier to outrank")
    print(f"   4. Check for listings with poor images — visual differentiation wins")

    return {
        "query": query,
        "marketplace": marketplace,
        "total_results": len(asins),
        "competitors": competitors,
        "top_asins": asins[:limit],
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 competitor_spy.py 'search term' [marketplace] [limit]")
        print("Example: python3 competitor_spy.py 'seasoning blend gift set'")
        sys.exit(1)

    query = sys.argv[1]
    marketplace = sys.argv[2] if len(sys.argv) > 2 else "com"
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    result = analyze_competitors(query, marketplace, limit)

    if result:
        import os
        report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports")
        os.makedirs(report_dir, exist_ok=True)
        safe_name = query.replace(" ", "-").lower()[:30]
        report_file = os.path.join(report_dir, f"competitors-{safe_name}.json")
        with open(report_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Report saved: {report_file}")
