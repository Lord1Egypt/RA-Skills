#!/usr/bin/env python3
"""
Anspire Search Python wrapper
Usage: python search.py "your search query" [--top-k 10]
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
from typing import Dict, List, Any


def search(query: str, top_k: int = 10, api_key: str = None) -> Dict[str, Any]:
    """
    Execute Anspire search query

    Args:
        query: Search query string
        top_k: Number of results to return (default: 10)
        api_key: API key (defaults to ANSPIRE_API_KEY env var)

    Returns:
        JSON response from API
    """
    if api_key is None:
        api_key = os.environ.get('ANSPIRE_API_KEY')

    if not api_key:
        raise ValueError("ANSPIRE_API_KEY environment variable is not set")

    # Build URL with query parameters
    base_url = "https://plugin.anspire.cn/api/ntsearch/search"
    params = urllib.parse.urlencode({
        'query': query,
        'top_k': str(top_k)
    })
    url = f"{base_url}?{params}"

    # Create request with headers
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }

    req = urllib.request.Request(url, headers=headers)

    # Execute request
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise Exception(f"API request failed: {e.code} {e.reason}\n{error_body}")


def format_results(results: List[Dict[str, Any]]) -> str:
    """Format search results for display"""
    output = []
    for i, result in enumerate(results, 1):
        output.append(f"\n{'='*80}")
        output.append(f"Result {i}")
        output.append(f"{'='*80}")
        output.append(f"Title: {result.get('title', 'N/A')}")
        output.append(f"URL: {result.get('url', 'N/A')}")
        output.append(f"Score: {result.get('score', 'N/A')}")
        output.append(f"Date: {result.get('date', 'N/A')}")
        output.append(f"\nContent:\n{result.get('content', 'N/A')[:500]}...")
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Anspire Search - Real-time web search'
    )
    parser.add_argument('query', help='Search query')
    parser.add_argument('--top-k', type=int, default=10,
                       help='Number of results to return (default: 10)')
    parser.add_argument('--json', action='store_true',
                       help='Output raw JSON response')
    parser.add_argument('--api-key', help='API key (overrides ANSPIRE_API_KEY env var)')

    args = parser.parse_args()

    try:
        response = search(args.query, args.top_k, args.api_key)

        if args.json:
            print(json.dumps(response, indent=2, ensure_ascii=False))
        else:
            results = response.get('results', [])
            if not results:
                print("No results found")
            else:
                print(format_results(results))
                print(f"\n\nTotal results: {len(results)}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
