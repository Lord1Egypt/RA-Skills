#!/usr/bin/env python3
"""Flatten a sitemap index or urlset into a simple URL list.

Supports local XML files or https URLs. Uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import ssl
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import deque
from pathlib import Path
from typing import Iterable

NS = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
}


def read_xml(source: str) -> bytes:
    if source.startswith("http://") or source.startswith("https://"):
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(source, context=ctx, timeout=30) as resp:
            return resp.read()
    return Path(source).read_bytes()


def parse_urls(source: str) -> list[str]:
    seen_sitemaps = set()
    urls: list[str] = []
    queue = deque([source])

    while queue:
        current = queue.popleft()
        if current in seen_sitemaps:
            continue
        seen_sitemaps.add(current)

        data = read_xml(current)
        root = ET.fromstring(data)
        tag = root.tag.split("}")[-1]

        if tag == "sitemapindex":
            for loc in root.findall("sm:sitemap/sm:loc", NS):
                if loc.text:
                    queue.append(loc.text.strip())
        elif tag == "urlset":
            for loc in root.findall("sm:url/sm:loc", NS):
                if loc.text:
                    urls.append(loc.text.strip())
        else:
            raise ValueError(f"Unsupported sitemap root tag: {root.tag}")

    return urls


def main() -> int:
    parser = argparse.ArgumentParser(description="Flatten sitemap index or urlset into URLs")
    parser.add_argument("source", help="HTTPS sitemap URL or local XML file")
    parser.add_argument("--output", help="Optional file path for URL output")
    args = parser.parse_args()

    urls = parse_urls(args.source)
    lines = "\n".join(urls) + ("\n" if urls else "")
    if args.output:
        Path(args.output).write_text(lines, encoding="utf-8")
    else:
        sys.stdout.write(lines)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
