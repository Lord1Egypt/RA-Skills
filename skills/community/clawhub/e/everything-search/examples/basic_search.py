#!/usr/bin/env python3
"""
Basic search example.

Usage:
    python examples/basic_search.py "数据资产"
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from everything_search import EverythingSearch


def main():
    if len(sys.argv) < 2:
        print("Usage: python basic_search.py <keyword>")
        print("Example: python basic_search.py 数据资产")
        sys.exit(1)
    
    keyword = sys.argv[1]
    
    print(f"🔍 Searching for: {keyword}")
    print("=" * 60)
    
    # Initialize search client
    search = EverythingSearch(port=2853)
    
    # Check connection
    if not search.check_connection():
        print("❌ Error: Cannot connect to Everything HTTP Server")
        print("\nPlease check:")
        print("1. Everything is running")
        print("2. HTTP Server is enabled (Ctrl+P → HTTP Server → Enable)")
        print("3. Port is set to 2853")
        sys.exit(1)
    
    # Execute search
    try:
        results = search.search(keyword, max_results=20)
        
        print(f"✅ Found {results.total} results in {results.query_time:.2f}s")
        print()
        
        if results.total == 0:
            print("No files found. Try different keywords.")
        else:
            print(f"Top {len(results.items)} results:")
            print("-" * 60)
            
            for i, item in enumerate(results.items, 1):
                icon = "📁" if item.item_type == "folder" else "📄"
                print(f"{i:2}. {icon} {item.name}")
                print(f"    Path: {item.full_path}")
                print(f"    Size: {item.format_size()}")
                print()
    
    except Exception as e:
        print(f"❌ Search failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
