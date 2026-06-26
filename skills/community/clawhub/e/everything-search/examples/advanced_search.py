#!/usr/bin/env python3
"""
Advanced search with filters.

Usage:
    python examples/advanced_search.py --type jpg --size ">1mb" "照片"
"""

import sys
import os
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from everything_search import EverythingSearch


def main():
    parser = argparse.ArgumentParser(description='Advanced file search with filters')
    parser.add_argument('keyword', help='Search keyword')
    parser.add_argument('--type', '-t', help='File type/extension (e.g., jpg, pdf)')
    parser.add_argument('--size', '-s', help='Minimum file size (e.g., 1mb, 100kb)')
    parser.add_argument('--max-size', help='Maximum file size')
    parser.add_argument('--path', '-p', help='Search only in this path')
    parser.add_argument('--exclude', '-e', help='Exclude this path')
    parser.add_argument('--date', '-d', help='Modified after date (YYYY-MM-DD)')
    parser.add_argument('--max-results', '-m', type=int, default=20, help='Maximum results')
    
    args = parser.parse_args()
    
    print(f"🔍 Advanced Search")
    print("=" * 60)
    print(f"Keyword: {args.keyword}")
    if args.type:
        print(f"File Type: {args.type}")
    if args.size:
        print(f"Min Size: {args.size}")
    if args.max_size:
        print(f"Max Size: {args.max_size}")
    if args.path:
        print(f"Path: {args.path}")
    if args.exclude:
        print(f"Exclude Path: {args.exclude}")
    if args.date:
        print(f"Modified After: {args.date}")
    print("=" * 60)
    
    # Initialize search client
    search = EverythingSearch(port=2853)
    
    # Check connection
    if not search.check_connection():
        print("❌ Error: Cannot connect to Everything HTTP Server")
        sys.exit(1)
    
    # Execute search with filters
    try:
        results = search.search(
            keyword=args.keyword,
            file_type=args.type,
            min_size=args.size,
            max_size=args.max_size,
            path=args.path,
            exclude_path=args.exclude,
            modified_after=args.date,
            max_results=args.max_results
        )
        
        print(f"\n✅ Found {results.total} results in {results.query_time:.2f}s")
        print()
        
        if results.total == 0:
            print("No files found. Try adjusting filters.")
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
