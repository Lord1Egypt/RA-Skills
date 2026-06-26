#!/usr/bin/env python3
"""Sitemap Generator — crawl a website or scan local files to generate sitemap.xml."""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urlunparse
from collections import deque

__version__ = "1.0.0"

# Max pages to crawl to prevent infinite loops
DEFAULT_MAX_PAGES = 500
DEFAULT_TIMEOUT = 10


class LinkExtractor(HTMLParser):
    """Extract href links from HTML content."""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, value in attrs:
                if attr == "href" and value:
                    self.links.append(value)


def normalize_url(url):
    """Normalize a URL for deduplication."""
    parsed = urlparse(url)
    # Remove fragment
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path.rstrip("/") or "/",
        parsed.params,
        parsed.query,
        "",
    ))
    return normalized


def is_same_domain(url, base_domain):
    """Check if URL belongs to the same domain."""
    parsed = urlparse(url)
    return parsed.netloc.lower() == base_domain.lower()


def should_skip(url):
    """Check if URL should be skipped (non-page resources)."""
    skip_extensions = (
        ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico",
        ".css", ".js", ".woff", ".woff2", ".ttf", ".eot",
        ".pdf", ".zip", ".tar", ".gz", ".rar",
        ".mp3", ".mp4", ".avi", ".mov", ".wmv",
        ".xml", ".json", ".rss", ".atom",
    )
    parsed = urlparse(url)
    path_lower = parsed.path.lower()
    return any(path_lower.endswith(ext) for ext in skip_extensions)


def fetch_page(url, timeout=DEFAULT_TIMEOUT):
    """Fetch a page and return (status_code, content, content_type)."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {"User-Agent": "SitemapGenerator/1.0 (+https://clawhub.com/skills/sitemap-generator)"}
    req = urllib.request.Request(url, headers=headers)

    try:
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        content_type = resp.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            return resp.getcode(), "", content_type
        content = resp.read().decode("utf-8", errors="replace")
        return resp.getcode(), content, content_type
    except urllib.error.HTTPError as e:
        return e.code, "", ""
    except Exception:
        return None, "", ""


def extract_links(html, base_url):
    """Extract and resolve links from HTML content."""
    parser = LinkExtractor()
    try:
        parser.feed(html)
    except Exception:
        pass

    links = []
    for href in parser.links:
        # Skip javascript:, mailto:, tel:, etc.
        if re.match(r'^(javascript|mailto|tel|data|ftp):', href, re.I):
            continue
        resolved = urljoin(base_url, href)
        links.append(resolved)

    return links


def crawl(start_url, max_pages=DEFAULT_MAX_PAGES, timeout=DEFAULT_TIMEOUT, verbose=False):
    """Crawl a website starting from start_url, return list of discovered pages."""
    parsed_start = urlparse(start_url)
    base_domain = parsed_start.netloc.lower()

    visited = set()
    queue = deque([normalize_url(start_url)])
    pages = []

    while queue and len(visited) < max_pages:
        url = queue.popleft()

        if url in visited:
            continue

        visited.add(url)

        if not is_same_domain(url, base_domain):
            continue

        if should_skip(url):
            continue

        if verbose:
            print(f"  Crawling: {url}", file=sys.stderr)

        status, content, ctype = fetch_page(url, timeout=timeout)

        if status and 200 <= status < 400:
            pages.append({
                "url": url,
                "status": status,
            })

            # Extract links from the page
            if content:
                links = extract_links(content, url)
                for link in links:
                    norm_link = normalize_url(link)
                    if norm_link not in visited and is_same_domain(norm_link, base_domain):
                        queue.append(norm_link)

    return pages


def scan_local_files(directory, base_url):
    """Scan local HTML/MD files and generate sitemap entries."""
    pages = []
    base_url = base_url.rstrip("/")

    for root, dirs, files in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for fname in sorted(files):
            if not fname.lower().endswith((".html", ".htm", ".md", ".php")):
                continue

            fpath = os.path.join(root, fname)
            relpath = os.path.relpath(fpath, directory)

            # Convert file path to URL path
            url_path = relpath.replace(os.sep, "/")
            if url_path == "index.html":
                url_path = ""
            elif url_path.endswith("/index.html"):
                url_path = url_path[:-len("/index.html")]

            url = f"{base_url}/{url_path}" if url_path else f"{base_url}/"

            # Get last modified time
            mtime = os.path.getmtime(fpath)
            lastmod = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%d")

            pages.append({
                "url": url,
                "lastmod": lastmod,
            })

    return pages


def generate_sitemap_xml(pages, pretty=True):
    """Generate sitemap.xml content."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in pages:
        if pretty:
            lines.append("  <url>")
            lines.append(f"    <loc>{_xml_escape(page['url'])}</loc>")
            if "lastmod" in page:
                lines.append(f"    <lastmod>{page['lastmod']}</lastmod>")
            if "changefreq" in page:
                lines.append(f"    <changefreq>{page['changefreq']}</changefreq>")
            if "priority" in page:
                lines.append(f"    <priority>{page['priority']}</priority>")
            lines.append("  </url>")
        else:
            parts = [f"<loc>{_xml_escape(page['url'])}</loc>"]
            if "lastmod" in page:
                parts.append(f"<lastmod>{page['lastmod']}</lastmod>")
            lines.append(f"<url>{''.join(parts)}</url>")

    lines.append("</urlset>")
    return "\n".join(lines)


def generate_robots_txt(sitemap_url, additional_rules=None):
    """Generate a robots.txt with sitemap reference."""
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {sitemap_url}",
    ]
    if additional_rules:
        lines.insert(2, "")
        for rule in additional_rules:
            lines.insert(2, rule)
    return "\n".join(lines)


def _xml_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")


def format_text(pages, sitemap_xml):
    """Format output as human-readable text."""
    lines = []
    lines.append(f"Sitemap Generator Results")
    lines.append(f"Pages found: {len(pages)}")
    lines.append("=" * 50)
    for page in pages:
        extra = ""
        if "lastmod" in page:
            extra = f" (modified: {page['lastmod']})"
        lines.append(f"  {page['url']}{extra}")
    lines.append("")
    lines.append("--- sitemap.xml ---")
    lines.append(sitemap_xml)
    return "\n".join(lines)


def format_json(pages, sitemap_xml):
    """Format output as JSON."""
    return json.dumps({
        "pages_count": len(pages),
        "pages": pages,
        "sitemap_xml": sitemap_xml,
    }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Sitemap Generator — crawl website or scan local files to generate sitemap.xml",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Crawl a website
  python3 sitemap_gen.py https://example.com

  # Crawl with limit
  python3 sitemap_gen.py https://example.com --max-pages 100

  # Scan local files
  python3 sitemap_gen.py --local ./public --base-url https://example.com

  # Save sitemap.xml to file
  python3 sitemap_gen.py https://example.com --output sitemap.xml

  # Generate robots.txt too
  python3 sitemap_gen.py https://example.com --robots""")

    parser.add_argument("url", nargs="?", help="URL to crawl")
    parser.add_argument("--local", help="Local directory to scan instead of crawling")
    parser.add_argument("--base-url", help="Base URL for local file mode")
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES,
                        help=f"Maximum pages to crawl (default: {DEFAULT_MAX_PAGES})")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})")
    parser.add_argument("--output", "-o", help="Save sitemap.xml to file")
    parser.add_argument("--robots", action="store_true", help="Also generate robots.txt")
    parser.add_argument("--format", choices=["xml", "text", "json"], default="xml",
                        help="Output format (default: xml)")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--version", action="version", version=f"sitemap-generator {__version__}")

    args = parser.parse_args()

    if args.local:
        if not args.base_url:
            print("Error: --base-url required with --local mode", file=sys.stderr)
            sys.exit(1)
        if not os.path.isdir(args.local):
            print(f"Error: Directory not found: {args.local}", file=sys.stderr)
            sys.exit(1)
        pages = scan_local_files(args.local, args.base_url)
    elif args.url:
        url = args.url
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        if args.verbose:
            print(f"Crawling {url} (max {args.max_pages} pages)...", file=sys.stderr)
        pages = crawl(url, max_pages=args.max_pages, timeout=args.timeout, verbose=args.verbose)
    else:
        parser.print_help()
        sys.exit(1)

    if not pages:
        print("No pages found.", file=sys.stderr)
        sys.exit(1)

    sitemap_xml = generate_sitemap_xml(pages)

    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(sitemap_xml)
        print(f"Sitemap saved to {args.output} ({len(pages)} pages)", file=sys.stderr)

        if args.robots:
            robots_path = os.path.join(os.path.dirname(args.output) or ".", "robots.txt")
            parsed = urlparse(args.url or args.base_url)
            sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
            with open(robots_path, "w", encoding="utf-8") as f:
                f.write(generate_robots_txt(sitemap_url))
            print(f"robots.txt saved to {robots_path}", file=sys.stderr)
    else:
        if args.format == "json":
            print(format_json(pages, sitemap_xml))
        elif args.format == "text":
            print(format_text(pages, sitemap_xml))
        else:
            print(sitemap_xml)


if __name__ == "__main__":
    main()
