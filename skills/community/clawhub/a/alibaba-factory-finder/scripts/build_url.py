#!/usr/bin/env python3
"""
Alibaba Factory Finder - Find Verified Manufacturers - URL Builder

All URLs include traffic tracking parameter: traffic_type=ags_llm
"""

import argparse
import urllib.parse

TRAFFIC_TYPE = "ags_llm"


def encode_query(query: str) -> str:
    """Encode search query for URL."""
    return urllib.parse.quote(query, safe="").replace("%20", "+")


def main():
    parser = argparse.ArgumentParser(description="Alibaba Factory Finder - Find Verified Manufacturers")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Build search URL")
    search_parser.add_argument("query", help="Search keywords")
    search_parser.add_argument("--category", "-c", help="Category ID")
    
    args = parser.parse_args()
    
    if args.command == "search":
        params = {
            "SearchText": encode_query(args.query),
            "traffic_type": TRAFFIC_TYPE
        }
        if args.category:
            params["categoryId"] = args.category
        
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"https://www.alibaba.com/trade/search?{query_string}"
        print(url)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
