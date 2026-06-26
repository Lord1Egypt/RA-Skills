#!/usr/bin/env python3
"""
Batch search - search for multiple keywords at once.

Usage:
    python examples/batch_search.py "数据资产" "张三" "报告"
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from everything_search import EverythingSearch


def main():
    if len(sys.argv) < 2:
        print("Usage: python batch_search.py <keyword1> [keyword2] [keyword3] ...")
        print("Example: python batch_search.py 数据资产 张三 报告")
        sys.exit(1)

    keywords = sys.argv[1:]

    print(f"🔍 Batch Search - {len(keywords)} keywords")
    print("=" * 60)

    # Initialize search client
    search = EverythingSearch(port=2853)

    # Check connection
    if not search.check_connection():
        print("❌ Error: Cannot connect to Everything HTTP Server")
        sys.exit(1)

    # Search for each keyword
    for i, keyword in enumerate(keywords, 1):
        print(f"\n[{i}/{len(keywords)}] Searching: {keyword}")
        print("-" * 60)

        try:
            results = search.search(keyword, max_results=5)

            print(f"   Found {results.total} results in {results.query_time:.2f}s")

            if results.total > 0:
                print(f"   Top 3 results:")
                for item in results.items[:3]:
                    icon = "📁" if item.item_type == "folder" else "📄"
                    print(f"     {icon} {item.name}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "=" * 60)
    print("✅ Batch search complete!")


if __name__ == "__main__":
    main()
