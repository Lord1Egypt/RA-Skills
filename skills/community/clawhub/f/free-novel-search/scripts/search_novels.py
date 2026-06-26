#!/usr/bin/env python3
"""
Free Novel Search Tool

Search multiple free novel databases and platforms.
Supports: Project Gutenberg, Open Library, and general web search.
"""

import argparse
import json
import sys
from urllib.parse import quote_plus

# Platform configurations
PLATFORMS = {
    "gutenberg": {
        "name": "Project Gutenberg",
        "base_url": "https://gutendex.com/books",
        "search_param": "search",
        "free_domain": True
    },
    "openlibrary": {
        "name": "Open Library",
        "base_url": "https://openlibrary.org/search.json",
        "search_param": "q",
        "free_domain": True
    },
    "manybooks": {
        "name": "ManyBooks",
        "base_url": "https://manybooks.net/search",
        "search_param": "search",
        "free_domain": True
    }
}

CATEGORIES = {
    "fiction": "fiction",
    "scifi": "science%20fiction",
    "fantasy": "fantasy",
    "mystery": "mystery",
    "romance": "romance",
    "nonfic": "nonfiction"
}


def format_gutenberg_result(book):
    """Format Gutenberg book result."""
    return {
        "title": book.get("title", "Unknown"),
        "author": book.get("authors", [{}])[0].get("name", "Unknown"),
        "id": book.get("id"),
        "formats": list(book.get("formats", {}).keys()),
        "languages": book.get("languages", []),
        "url": f"https://gutendex.com/books/{book.get('id')}"
    }


def format_openlibrary_result(doc):
    """Format Open Library search result."""
    return {
        "title": doc.get("title", "Unknown"),
        "author": doc.get("author_name", ["Unknown"])[0],
        "publish_year": doc.get("first_publish_year"),
        "language": doc.get("language", []),
        "url": f"https://openlibrary.org{doc.get('key', '')}",
        "source": "Open Library"
    }


def search_gutenberg(query, limit=20):
    """Search Project Gutenberg via Gutendex API."""
    try:
        import urllib.request
        import ssl

        # Disable SSL verification for gutendex
        context = ssl._create_unverified_context()
        url = f"{PLATFORMS['gutenberg']['base_url']}?search={quote_plus(query)}"
        url += f"&languages=en"

        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/json')

        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            data = json.loads(response.read().decode())
            results = data.get("results", [])[:limit]
            return [format_gutenberg_result(book) for book in results]
    except Exception as e:
        print(f"Gutenberg search error: {e}", file=sys.stderr)
        return []


def search_openlibrary(query, limit=20, category=None):
    """Search Open Library."""
    try:
        import urllib.request
        import urllib.parse
        import ssl

        params = {"q": query, "limit": limit, "mode": "everything"}
        if category and category in CATEGORIES:
            params["subject"] = CATEGORIES[category]

        url = f"{PLATFORMS['openlibrary']['base_url']}?{urllib.parse.urlencode(params)}"

        context = ssl._create_unverified_context()
        req = urllib.request.Request(url)

        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            data = json.loads(response.read().decode())
            docs = data.get("docs", [])[:limit]
            return [format_openlibrary_result(doc) for doc in docs]
    except Exception as e:
        print(f"Open Library search error: {e}", file=sys.stderr)
        return []


def search_general(query, limit=10):
    """Provide search link for general web search (requires browser or external tool)."""
    # Since we can't actually scrape, provide search URLs
    search_urls = [
        ("Gutenberg", f"https://gutendex.com/books?search={quote_plus(query)}"),
        ("Open Library", f"https://openlibrary.org/search?q={quote_plus(query)}"),
        ("ManyBooks", f"https://manybooks.net/search?search={quote_plus(query)}"),
        ("Wattpad", f"https://www.wattpad.com/search/{quote_plus(query)}"),
        ("Google", f"https://www.google.com/search?q={quote_plus(query)}+free+novel")
    ]

    return {
        "query": query,
        "search_links": [
            {"site": name, "url": url}
            for name, url in search_urls
        ],
        "message": "Use web browser or search tool to access these links"
    }


def main():
    parser = argparse.ArgumentParser(
        description="Search free novel databases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --query "Harry Potter"
  %(prog)s --query "science fiction" --source gutenberg
  %(prog)s --query "mystery" --category mystery --limit 10
  %(prog)s --query "Jane Austen" --output results.json
        """
    )

    parser.add_argument(
        "--query", "-q",
        required=True,
        help="Search query"
    )

    parser.add_argument(
        "--source", "-s",
        choices=["gutenberg", "openlibrary", "all"],
        default="all",
        help="Data source (default: all)"
    )

    parser.add_argument(
        "--category", "-c",
        choices=["fiction", "scifi", "fantasy", "mystery", "romance", "nonfic"],
        help="Filter by category"
    )

    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=20,
        help="Maximum results (default: 20)"
    )

    parser.add_argument(
        "--output", "-o",
        help="Output results to JSON file"
    )

    args = parser.parse_args()

    all_results = {
        "query": args.query,
        "sources": {}
    }

    if args.source in ["gutenberg", "all"]:
        print("Searching Project Gutenberg...")
        gutenberg_results = search_gutenberg(args.query, args.limit)
        all_results["sources"]["gutenberg"] = gutenberg_results
        print(f"  Found {len(gutenberg_results)} results")

    if args.source in ["openlibrary", "all"]:
        print("Searching Open Library...")
        ol_results = search_openlibrary(args.query, args.limit, args.category)
        all_results["sources"]["openlibrary"] = ol_results
        print(f"  Found {len(ol_results)} results")

    if args.source == "all" and not all_results["sources"]:
        # Fallback to search links
        print("No API access, providing search links...")
        all_results["search_links"] = search_general(args.query)["search_links"]

    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved to {args.output}")
    else:
        print("\n" + "="*50)
        print(json.dumps(all_results, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())