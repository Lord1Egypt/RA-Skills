#!/usr/bin/env python3
"""
Amazon Product Fetcher — stdlib only, no pip dependencies.
Fetches title, price, rating, reviews, availability, image from a public Amazon page.

Usage:
    python fetch.py --url "https://www.amazon.com/dp/B0CX44VMKZ"
    python fetch.py --asin B0CX44VMKZ
    python fetch.py --asin B0CX44VMKZ --json
"""

import argparse
import html
import json
import os
import re
import sys
import urllib.request

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

MARKETPLACE = os.environ.get("AMAZON_MARKETPLACE", "www.amazon.com")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# ---------------------------------------------------------------------------
# URL / ASIN helpers
# ---------------------------------------------------------------------------

def extract_asin_from_url(url: str) -> str | None:
    """Extract ASIN from any Amazon URL format."""
    for pattern in [
        r"/dp/([A-Z0-9]{10})",
        r"/gp/product/([A-Z0-9]{10})",
        r"/ASIN/([A-Z0-9]{10})",
        r"[?&]asin=([A-Z0-9]{10})",
    ]:
        m = re.search(pattern, url, re.IGNORECASE)
        if m:
            return m.group(1).upper()
    return None


def build_url(asin: str) -> str:
    return f"https://{MARKETPLACE}/dp/{asin}"


# ---------------------------------------------------------------------------
# HTTP fetch
# ---------------------------------------------------------------------------

def fetch_page(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")
    except Exception as e:
        print(f"Error fetching page: {e}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Field parsers (regex on raw HTML — no lxml/bs4)
# ---------------------------------------------------------------------------

def _first(patterns: list, text: str) -> str:
    """Return first capturing group from the first matching pattern."""
    for p in patterns:
        m = re.search(p, text, re.DOTALL | re.IGNORECASE)
        if m:
            val = html.unescape(m.group(1)).strip()
            # Remove inner HTML tags if any slipped through
            val = re.sub(r"<[^>]+>", "", val).strip()
            if val:
                return val
    return ""


def parse_title(page: str) -> str:
    return _first([
        r'id="productTitle"[^>]*>\s*(.*?)\s*</span>',
        r'"title"\s*:\s*"([^"]{10,})"',
    ], page)


def parse_price(page: str) -> tuple:
    """Returns (price_number_str, currency_symbol)."""
    raw = _first([
        r'class="a-price[^"]*"[^>]*>.*?<span\s+class="a-offscreen">([^<]+)</span>',
        r'id="priceblock_ourprice"[^>]*>\s*([^<\n]+)',
        r'id="priceblock_dealprice"[^>]*>\s*([^<\n]+)',
        r'class="priceToPay[^"]*"[^>]*>.*?<span[^>]*>\s*([0-9][0-9,\.]*)\s*</span>',
    ], page)
    if not raw:
        return ("", "")
    raw = raw.strip()
    m = re.match(r'^([^\d]*)([\d,\.]+)', raw)
    if m:
        return (m.group(2).strip(), m.group(1).strip())
    return (raw, "")


def parse_rating(page: str) -> str:
    return _first([
        r'class="a-icon-alt">\s*([\d\.]+)\s+out of',
        r'aria-label="([\d\.]+) out of 5',
        r'"ratingScore"\s*:\s*"?([\d\.]+)"?',
    ], page)


def parse_reviews(page: str) -> str:
    return _first([
        r'id="acrCustomerReviewText"[^>]*>\s*([\d,]+)\s+rating',
        r'"reviewCount"\s*:\s*"?([\d,]+)"?',
        r'([\d,]+)\s+(?:global\s+)?ratings?\b',
    ], page)


def parse_availability(page: str) -> str:
    return _first([
        r'id="availability"[^>]*>.*?<span[^>]*>\s*(.*?)\s*</span>',
        r'"availability"\s*:\s*"([^"]+)"',
    ], page)


def parse_image(page: str) -> str:
    return _first([
        r'"hiRes"\s*:\s*"(https://[^"]+\.jpg[^"]*)"',
        r'"large"\s*:\s*"(https://[^"]+\.jpg[^"]*)"',
        r'id="landingImage"[^>]+src="([^"]+)"',
        r'id="imgBlkFront"[^>]+src="([^"]+)"',
    ], page)


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def fetch_product(asin: str) -> dict:
    url = build_url(asin)
    page = fetch_page(url)
    price, currency = parse_price(page)
    return {
        "asin": asin,
        "title": parse_title(page),
        "price": price,
        "currency": currency,
        "rating": parse_rating(page),
        "reviews": parse_reviews(page),
        "availability": parse_availability(page),
        "image_url": parse_image(page),
        "product_url": url,
    }


def print_table(d: dict) -> None:
    title = d.get("title", "")
    rows = [
        ("ASIN",         d.get("asin", "")),
        ("Title",        (title[:80] + "…") if len(title) > 80 else title),
        ("Price",        f"{d.get('currency','')}{d.get('price','')}"),
        ("Rating",       f"{d.get('rating','')} ⭐  ({d.get('reviews','')} reviews)"),
        ("Availability", d.get("availability", "")),
        ("Image",        (d.get("image_url","")[:70] + "…") if d.get("image_url") else ""),
        ("URL",          d.get("product_url", "")),
    ]
    width = max(len(k) for k, _ in rows)
    for k, v in rows:
        print(f"  {k:<{width}}  {v}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fetch Amazon product data — stdlib only, no API key needed."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--asin", help="Amazon ASIN (e.g. B0CX44VMKZ)")
    group.add_argument("--url",  help="Full Amazon product URL")
    parser.add_argument(
        "--json", dest="as_json", action="store_true",
        help="Output as JSON (machine-readable)"
    )
    parser.add_argument(
        "--marketplace", default=None,
        help="Amazon domain (default: www.amazon.com). Env: AMAZON_MARKETPLACE"
    )
    args = parser.parse_args()

    # Allow --marketplace flag to override env
    if args.marketplace:
        global MARKETPLACE
        MARKETPLACE = args.marketplace

    if args.url:
        asin = extract_asin_from_url(args.url)
        if not asin:
            print(f"Error: Could not extract ASIN from URL: {args.url}", file=sys.stderr)
            sys.exit(1)
    else:
        asin = args.asin.strip().upper()

    result = fetch_product(asin)

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n📦 Amazon Product — {asin}\n")
        print_table(result)
        print()


if __name__ == "__main__":
    main()