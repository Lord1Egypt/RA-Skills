#!/usr/bin/env python3
"""
crawlee_http.py — Shared HTTP helper with Crawlee fallback.

Tries requests first. If blocked (403, 429, or connection error),
falls back to crawlee_fetch.py subprocess for bot-detection evasion.

Usage (as a library):
    from crawlee_http import fetch_with_fallback
    resp = fetch_with_fallback("https://example.com")
    print(resp.status_code, resp.text[:500])
"""

import subprocess
import sys
import json
import os

# Status codes that trigger Crawlee fallback
BLOCKED_CODES = {403, 429, 503}

CRAWLEE_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crawlee_fetch.py")


def fetch_with_fallback(url, headers=None, timeout=10):
    """
    Fetch a URL using requests; fall back to Crawlee if blocked.

    Returns a requests-like object with .status_code and .text attributes.
    Raises on total failure (both methods fail).
    """
    import requests

    # Try requests first
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code not in BLOCKED_CODES:
            return resp
        print(f"  [crawlee_http] {resp.status_code} from {url}, trying Crawlee...", file=sys.stderr)
    except requests.exceptions.RequestException as e:
        print(f"  [crawlee_http] requests failed for {url}: {e}, trying Crawlee...", file=sys.stderr)

    # Fallback: call crawlee_fetch.py as subprocess
    return _crawlee_fetch(url)


class _CrawleeResponse:
    """Minimal requests.Response-compatible wrapper for Crawlee output."""

    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"Crawlee fetch returned status {self.status_code}")


def _crawlee_fetch(url):
    """Run crawlee_fetch.py as a subprocess and return a response-like object."""
    try:
        result = subprocess.run(
            [sys.executable, CRAWLEE_SCRIPT, "--url", url, "--extract-text"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            raise Exception(f"crawlee_fetch.py failed: {result.stderr.strip()}")

        data = json.loads(result.stdout)
        if not data:
            raise Exception("crawlee_fetch.py returned empty results")

        entry = data[0]
        status = entry.get("status", 200)
        text = entry.get("text", "") or entry.get("html_preview", "")
        return _CrawleeResponse(status, text)

    except subprocess.TimeoutExpired:
        raise Exception(f"Crawlee fetch timed out for {url}")
    except json.JSONDecodeError:
        raise Exception(f"Crawlee fetch returned invalid JSON for {url}")
