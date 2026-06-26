#!/usr/bin/env python3
"""
Search recent tweets
Convenience wrapper around x_api_client.py
"""

import sys
import json
from x_api_client import XAPIClient


def search_tweets(query, max_results=10):
    """
    Search recent tweets (last 7 days)
    
    Note: Requires Elevated or Academic access level on X Developer Portal
    
    Args:
        query: Search query string
        max_results: Number of tweets to fetch (10-100)
    
    Returns:
        List of matching tweets
    """
    client = XAPIClient()
    result = client.search_recent_tweets(query, max_results=max_results)
    
    return {
        'query': query,
        'tweets': result.get('data', []),
        'meta': result.get('meta', {})
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: search_tweets.py <query> [count]")
        print("Example: search_tweets.py 'machine learning' 20")
        sys.exit(1)
    
    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 10
    
    try:
        result = search_tweets(query, count)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
