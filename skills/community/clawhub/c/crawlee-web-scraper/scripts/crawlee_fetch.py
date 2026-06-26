#!/usr/bin/env python3
"""
crawlee_fetch.py — Resilient web scraping with bot-detection evasion.

Use this instead of web_fetch when:
- Sites are blocking requests (rate limits, bot detection)
- Need to scrape multiple URLs in bulk
- Need persistent progress (won't lose data on crash)

Usage:
  python3 crawlee_fetch.py --url "https://example.com"
  python3 crawlee_fetch.py --urls-file /path/to/urls.txt --output /path/to/out.json
  python3 crawlee_fetch.py --url "https://example.com" --extract-text

Dependencies: pip install crawlee
"""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


async def scrape_urls(urls: list[str], extract_text: bool = False) -> list[dict]:
    from crawlee.crawlers import HttpCrawler, HttpCrawlingContext

    results = []

    async def handler(context: HttpCrawlingContext):
        url = context.request.url
        html = await context.http_response.read()
        text = html.decode("utf-8", errors="replace")

        result = {
            "url": url,
            "status": context.http_response.status_code,
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "length": len(text),
        }

        if extract_text:
            # Basic text extraction — strip tags
            import re
            clean = re.sub(r'<[^>]+>', ' ', text)
            clean = re.sub(r'\s+', ' ', clean).strip()
            result["text"] = clean[:10000]  # cap at 10k chars
        else:
            result["html_preview"] = text[:2000]

        results.append(result)
        print(f"✅ {url} ({context.http_response.status_code})", file=sys.stderr)

    crawler = HttpCrawler(
        max_requests_per_crawl=len(urls),
        request_handler=handler,
    )

    await crawler.run(urls)
    return results


def main():
    parser = argparse.ArgumentParser(description="Resilient scraper using Crawlee")
    parser.add_argument("--url", help="Single URL to scrape")
    parser.add_argument("--urls-file", help="File with one URL per line")
    parser.add_argument("--output", help="Output JSON file path (default: stdout)")
    parser.add_argument("--extract-text", action="store_true", help="Strip HTML tags, return text only")
    args = parser.parse_args()

    urls = []
    if args.url:
        urls.append(args.url)
    if args.urls_file:
        urls.extend(Path(args.urls_file).read_text().strip().splitlines())

    if not urls:
        print("ERROR: --url or --urls-file required", file=sys.stderr)
        sys.exit(1)

    results = asyncio.run(scrape_urls(urls, extract_text=args.extract_text))

    output = json.dumps(results, indent=2)
    if args.output:
        Path(args.output).write_text(output)
        print(f"Saved {len(results)} results to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
