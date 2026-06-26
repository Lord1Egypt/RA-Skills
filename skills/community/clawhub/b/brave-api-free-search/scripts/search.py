#!/usr/bin/env python3
import os
import sys
import requests

DEFAULT_BASE = "http://127.0.0.1:8080"
BASE_URL = os.environ.get("SEARXNG_BASE_URL", DEFAULT_BASE).rstrip("/")
SEARCH_ENDPOINT = f"{BASE_URL}/search"
HEALTH_ENDPOINT = f"{BASE_URL}/"


def health_check():
    try:
        r = requests.get(HEALTH_ENDPOINT, timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def search(query):
    params = {
        "q": query,
        "format": "json"
    }
    try:
        r = requests.get(SEARCH_ENDPOINT, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to SearXNG at {BASE_URL}")
        print("Tip: Run install.py or set SEARXNG_BASE_URL")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: search.py \"your query\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    if not health_check():
        print(f"SearXNG is not reachable at {BASE_URL}")
        print("Run scripts/install.py to deploy it.")
        sys.exit(1)

    results = search(query)

    for idx, item in enumerate(results.get("results", [])[:10], 1):
        print(f"{idx}. {item.get('title')}")
        print(f"   {item.get('url')}")
        print(f"   {item.get('content')}")
        print()


if __name__ == "__main__":
    main()
