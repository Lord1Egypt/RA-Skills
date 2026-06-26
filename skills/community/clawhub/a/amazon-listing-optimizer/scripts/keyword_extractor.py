#!/usr/bin/env python3
"""
Amazon Keyword Extractor — Find keywords from competitor listings and search suggestions
Free alternative to Helium 10's Cerebro ($97/mo).
Uses Amazon's own autocomplete API for keyword discovery.
"""

import json
import sys
import urllib.request
import urllib.parse
import time
from collections import Counter


def get_amazon_suggestions(keyword, marketplace="com"):
    """Get Amazon search autocomplete suggestions."""
    encoded = urllib.parse.quote(keyword)
    url = (
        f"https://completion.amazon.{marketplace}/api/2017/suggestions"
        f"?session-id=000-0000000-0000000"
        f"&customer-id=000000000"
        f"&request-id=000000000"
        f"&page-type=Gateway"
        f"&lop=en_US"
        f"&site-variant=desktop"
        f"&client-info=amazon-search-ui"
        f"&mid=ATVPDKIKX0DER"
        f"&alias=aps"
        f"&prefix={encoded}"
        f"&event=onKeyPress"
        f"&limit=11"
        f"&fb=1"
        f"&suggestion-type=KEYWORD"
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Accept": "application/json",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            suggestions = []
            for s in data.get("suggestions", []):
                suggestions.append(s.get("value", ""))
            return suggestions
    except Exception as e:
        return []


def expand_keywords(seed_keyword, depth=2, marketplace="com"):
    """Expand a seed keyword into many long-tail variations."""
    all_keywords = set()
    queue = [seed_keyword]
    processed = set()

    for level in range(depth):
        next_queue = []
        for kw in queue:
            if kw in processed:
                continue
            processed.add(kw)

            suggestions = get_amazon_suggestions(kw, marketplace)
            for s in suggestions:
                if s and s not in all_keywords:
                    all_keywords.add(s)
                    next_queue.append(s)

            # Also try alphabet expansion
            if level == 0:
                for letter in "abcdefghijklmnopqrstuvwxyz":
                    alpha_suggestions = get_amazon_suggestions(f"{kw} {letter}", marketplace)
                    for s in alpha_suggestions:
                        if s and s not in all_keywords:
                            all_keywords.add(s)
                    time.sleep(0.1)  # Rate limiting

            time.sleep(0.1)  # Rate limiting

        queue = next_queue[:20]  # Limit expansion

    return sorted(all_keywords)


def extract_keyword_frequency(keywords):
    """Analyze word frequency across all keywords."""
    words = Counter()
    for kw in keywords:
        for word in kw.lower().split():
            if len(word) > 2:  # Skip short words
                words[word] += 1
    return words.most_common(30)


def run_keyword_research(seed, marketplace="com", depth=2):
    """Full keyword research for a seed term."""
    print(f"\n🔍 Amazon Keyword Research: '{seed}'")
    print(f"   Marketplace: amazon.{marketplace}")
    print(f"   Depth: {depth}")
    print("=" * 60)

    print(f"\n⏳ Expanding keywords (this takes ~30 seconds)...")
    keywords = expand_keywords(seed, depth, marketplace)

    print(f"\n📊 Found {len(keywords)} keyword variations:\n")

    # Group by relevance (contains all seed words)
    seed_words = set(seed.lower().split())
    exact_match = []
    broad_match = []

    for kw in keywords:
        kw_words = set(kw.lower().split())
        if seed_words.issubset(kw_words):
            exact_match.append(kw)
        else:
            broad_match.append(kw)

    if exact_match:
        print(f"🎯 Exact Match ({len(exact_match)}):")
        for kw in exact_match[:20]:
            print(f"   • {kw}")
        if len(exact_match) > 20:
            print(f"   ... and {len(exact_match) - 20} more")

    if broad_match:
        print(f"\n🌐 Broad Match ({len(broad_match)}):")
        for kw in broad_match[:15]:
            print(f"   • {kw}")
        if len(broad_match) > 15:
            print(f"   ... and {len(broad_match) - 15} more")

    # Word frequency
    freq = extract_keyword_frequency(keywords)
    if freq:
        print(f"\n📈 Top Keywords by Frequency:")
        for word, count in freq[:15]:
            bar = "█" * min(count, 20)
            print(f"   {word:20s} {bar} ({count})")

    return {
        "seed": seed,
        "total_keywords": len(keywords),
        "exact_match": exact_match,
        "broad_match": broad_match,
        "frequency": dict(freq),
        "all_keywords": keywords,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 keyword_extractor.py 'seed keyword' [marketplace] [depth]")
        print("Example: python3 keyword_extractor.py 'seasoning blend'")
        print("Example: python3 keyword_extractor.py 'garlic powder organic' com 2")
        sys.exit(1)

    seed = sys.argv[1]
    marketplace = sys.argv[2] if len(sys.argv) > 2 else "com"
    depth = int(sys.argv[3]) if len(sys.argv) > 3 else 2

    result = run_keyword_research(seed, marketplace, depth)

    # Save results
    import os
    report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports")
    os.makedirs(report_dir, exist_ok=True)
    safe_name = seed.replace(" ", "-").lower()[:30]
    report_file = os.path.join(report_dir, f"keywords-{safe_name}.json")
    with open(report_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n💾 Keywords saved: {report_file}")
