#!/usr/bin/env python3
import os
import requests
import sys

DEFAULT_BASE = "http://127.0.0.1:8080"
BASE_URL = os.environ.get("SEARXNG_BASE_URL", DEFAULT_BASE).rstrip("/")


def main():
    try:
        r = requests.get(BASE_URL, timeout=5)
        if r.status_code == 200:
            print(f"OK: SearXNG reachable at {BASE_URL}")
            sys.exit(0)
        else:
            print(f"Unexpected status code: {r.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"Healthcheck failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
