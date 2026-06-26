#!/usr/bin/env python3
"""
search.py — Google search CLI via ScrapingDog API
Usage:
  python search.py "your query"
  python search.py "your query" --results 5
  python search.py "your query" --country uk --lang en
  python search.py "your query" --json
"""

import argparse
import sys
import json
import os
import requests

API_KEY = os.environ.get("SCRAPINGDOG_API_KEY")
API_URL = "https://api.scrapingdog.com/google"


def search(query, results=10, country="us", language="en"):
    if not API_KEY:
        print("Error: SCRAPINGDOG_API_KEY environment variable is not set.", file=sys.stderr)
        print("  export SCRAPINGDOG_API_KEY=your_key_here", file=sys.stderr)
        sys.exit(1)

    params = {
        "api_key": API_KEY,
        "query": query,
        "results": results,
        "country": country,
        "language": language,
        "advance_search": "false",
        "domain": "google.com",
    }
    try:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        print(f"Error: HTTP {response.status_code} — {response.text}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect. Check your internet connection.", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: Request timed out.", file=sys.stderr)
        sys.exit(1)


def print_results(data, query):
    organic = data.get("organic_results") or data.get("organic_data") or []

    if not organic:
        print("No results found.")
        return

    print(f"\n  Results for: \"{query}\"\n")
    print("  " + "─" * 60)

    for i, result in enumerate(organic, 1):
        title   = result.get("title", "No title")
        url     = result.get("link", result.get("url", ""))
        snippet = result.get("snippet", result.get("description", ""))

        print(f"\n  [{i}] {title}")
        if url:
            print(f"      {url}")
        if snippet:
            words = snippet.split()
            lines, line = [], []
            for word in words:
                line.append(word)
                if len(" ".join(line)) > 70:
                    lines.append("      " + " ".join(line[:-1]))
                    line = [word]
            if line:
                lines.append("      " + " ".join(line))
            print("\n".join(lines))

    print("\n  " + "─" * 60)
    print(f"  {len(organic)} result(s)\n")


def main():
    parser = argparse.ArgumentParser(
        description="Search Google via ScrapingDog API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python search.py "python async tutorial"
  python search.py "openai news" --results 5
  python search.py "best laptops" --country uk
  python search.py "AI tools" --json

Environment:
  SCRAPINGDOG_API_KEY    Your ScrapingDog API key (required)
        """
    )
    parser.add_argument("query", help="Search query")
    #parser.add_argument("-n", "--results", type=int, default=9,
    #                    metavar="N", help="Number of results (default: 10)")
    parser.add_argument("--country", default="us",
                        help="Country code, e.g. us, uk, de (default: us)")
    parser.add_argument("--lang", default="en", dest="language",
                        help="Language code, e.g. en, fr, de (default: en)")
    parser.add_argument("--json", action="store_true", dest="raw_json",
                        help="Print raw JSON response")

    args = parser.parse_args()

    data = search(args.query, args.results, args.country, args.language)

    if args.raw_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print_results(data, args.query)


if __name__ == "__main__":
    main()
