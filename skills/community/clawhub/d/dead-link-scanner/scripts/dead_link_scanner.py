#!/usr/bin/env python3
"""Scan websites and files for broken links."""

import argparse
import sys
import json
import re
import time
import urllib.request
import urllib.error
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path
from collections import defaultdict

USER_AGENT = "dead-link-scanner/1.0 (+https://clawhub.com)"

# ── HTML Link Extractor ────────────────────────────────────────────────────

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a" and "href" in attrs_dict:
            self.links.append(attrs_dict["href"])
        elif tag == "img" and "src" in attrs_dict:
            self.links.append(attrs_dict["src"])
        elif tag == "link" and "href" in attrs_dict:
            self.links.append(attrs_dict["href"])
        elif tag == "script" and "src" in attrs_dict:
            self.links.append(attrs_dict["src"])


def extract_links_html(html_content):
    parser = LinkExtractor()
    try:
        parser.feed(html_content)
    except Exception:
        pass
    return parser.links


def extract_links_markdown(md_content):
    """Extract URLs from markdown [text](url) and bare URLs."""
    links = []
    # Markdown links
    for match in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', md_content):
        url = match.group(2).strip()
        if url and not url.startswith("#"):
            links.append(url)
    # Bare URLs
    for match in re.finditer(r'(?<!\()(https?://[^\s<>\)\"\']+)', md_content):
        url = match.group(0).rstrip(".,;:!?")
        if url not in links:
            links.append(url)
    return links


# ── URL Checker ─────────────────────────────────────────────────────────────

def check_url(url, timeout=10):
    """Check a URL and return (status_code, error_message)."""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
        resp = urllib.request.urlopen(req, timeout=timeout)
        return (resp.status, None)
    except urllib.error.HTTPError as e:
        # Some servers don't support HEAD, try GET for 405
        if e.code == 405:
            try:
                req = urllib.request.Request(url, method="GET", headers={"User-Agent": USER_AGENT})
                resp = urllib.request.urlopen(req, timeout=timeout)
                return (resp.status, None)
            except urllib.error.HTTPError as e2:
                return (e2.code, None)
            except Exception as e2:
                return (None, str(e2))
        return (e.code, None)
    except urllib.error.URLError as e:
        return (None, str(e.reason))
    except Exception as e:
        return (None, str(e))


def normalize_url(url, base_url):
    """Resolve a relative URL against a base URL."""
    if url.startswith("mailto:") or url.startswith("tel:") or url.startswith("javascript:") or url.startswith("#"):
        return None
    if url.startswith("data:"):
        return None
    try:
        resolved = urllib.parse.urljoin(base_url, url)
        # Remove fragments
        parsed = urllib.parse.urlparse(resolved)
        clean = urllib.parse.urlunparse(parsed._replace(fragment=""))
        return clean
    except Exception:
        return None


def same_domain(url, base_url):
    return urllib.parse.urlparse(url).netloc == urllib.parse.urlparse(base_url).netloc


# ── Website Scanner ─────────────────────────────────────────────────────────

def cmd_scan(args):
    base_url = args.url.rstrip("/")
    max_depth = args.depth
    timeout = args.timeout
    broken_only = args.broken_only
    internal_only = args.internal_only
    max_urls = args.max_urls
    delay = args.delay

    checked = {}  # url -> (status, error, found_on)
    to_crawl = [(base_url, 0)]  # (url, depth)
    crawled = set()
    all_links = []  # (link_url, found_on_page)

    # Crawl pages to find links
    while to_crawl:
        page_url, depth = to_crawl.pop(0)
        if page_url in crawled:
            continue
        crawled.add(page_url)

        try:
            req = urllib.request.Request(page_url, headers={"User-Agent": USER_AGENT})
            resp = urllib.request.urlopen(req, timeout=timeout)
            content_type = resp.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                continue
            html = resp.read().decode("utf-8", errors="replace")
        except Exception:
            continue

        links = extract_links_html(html)
        for link in links:
            resolved = normalize_url(link, page_url)
            if resolved:
                all_links.append((resolved, page_url))
                # Crawl deeper if same domain and within depth
                if depth < max_depth and same_domain(resolved, base_url) and resolved not in crawled:
                    parsed = urllib.parse.urlparse(resolved)
                    # Only crawl HTML-looking paths
                    path = parsed.path
                    if not path or path.endswith("/") or not re.search(r'\.\w{1,5}$', path) or path.endswith(".html") or path.endswith(".htm"):
                        to_crawl.append((resolved, depth + 1))

        if delay > 0:
            time.sleep(delay)

    # Check unique links
    urls_to_check = {}
    for link_url, found_on in all_links:
        if internal_only and not same_domain(link_url, base_url):
            continue
        if link_url not in urls_to_check:
            urls_to_check[link_url] = found_on

    results = []
    count = 0
    for url, found_on in urls_to_check.items():
        if count >= max_urls:
            break
        count += 1
        status, error = check_url(url, timeout)
        is_broken = status is None or status >= 400
        results.append({
            "url": url,
            "status": status,
            "error": error,
            "found_on": found_on,
            "broken": is_broken,
        })
        if delay > 0:
            time.sleep(delay)

    _output_results(results, broken_only, args.json)


# ── File Scanner ────────────────────────────────────────────────────────────

def cmd_file(args):
    results = []
    timeout = args.timeout
    broken_only = args.broken_only
    checked_cache = {}

    for file_path in args.files:
        p = Path(file_path)
        if not p.exists():
            print(f"Warning: File not found: {file_path}", file=sys.stderr)
            continue

        content = p.read_text(errors="replace")

        if p.suffix.lower() in (".md", ".markdown", ".mdx"):
            links = extract_links_markdown(content)
        elif p.suffix.lower() in (".html", ".htm"):
            links = extract_links_html(content)
        else:
            # Try markdown extraction as fallback
            links = extract_links_markdown(content)

        for url in links:
            if not url.startswith("http"):
                continue  # Skip relative links in files
            if url in checked_cache:
                status, error = checked_cache[url]
            else:
                status, error = check_url(url, timeout)
                checked_cache[url] = (status, error)

            is_broken = status is None or status >= 400
            results.append({
                "url": url,
                "status": status,
                "error": error,
                "found_on": str(file_path),
                "broken": is_broken,
            })

    _output_results(results, broken_only, args.json)


# ── Output ──────────────────────────────────────────────────────────────────

def _output_results(results, broken_only, as_json):
    if as_json:
        output = results if not broken_only else [r for r in results if r["broken"]]
        print(json.dumps(output, indent=2))
        return

    ok_count = 0
    broken_count = 0

    for r in results:
        if r["broken"]:
            broken_count += 1
            status_str = str(r["status"]) if r["status"] else "ERR"
            error_str = f" — {r['error']}" if r["error"] else ""
            print(f"✗ {status_str:>4}  {r['url']}  (found on: {r['found_on']}){error_str}")
        else:
            ok_count += 1
            if not broken_only:
                print(f"✓ {r['status']:>4}  {r['url']}")

    total = ok_count + broken_count
    print(f"\nChecked {total} links: {ok_count} OK, {broken_count} broken")
    if broken_count > 0:
        sys.exit(1)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Scan websites and files for broken links.")
    sub = parser.add_subparsers(dest="command", help="Command")

    # scan
    s = sub.add_parser("scan", help="Crawl a website for broken links")
    s.add_argument("url", help="URL to scan")
    s.add_argument("--depth", type=int, default=1, help="Max crawl depth (default: 1)")
    s.add_argument("--timeout", type=int, default=10, help="Request timeout seconds (default: 10)")
    s.add_argument("--json", action="store_true", help="JSON output")
    s.add_argument("--broken-only", action="store_true", help="Only show broken links")
    s.add_argument("--internal-only", action="store_true", help="Only check same-domain links")
    s.add_argument("--max-urls", type=int, default=200, help="Max URLs to check (default: 200)")
    s.add_argument("--delay", type=float, default=0.2, help="Delay between requests (default: 0.2)")

    # file
    f = sub.add_parser("file", help="Scan local files for broken links")
    f.add_argument("files", nargs="+", help="File paths to scan")
    f.add_argument("--timeout", type=int, default=10, help="Request timeout seconds")
    f.add_argument("--json", action="store_true", help="JSON output")
    f.add_argument("--broken-only", action="store_true", help="Only show broken links")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "file":
        cmd_file(args)


if __name__ == "__main__":
    main()
