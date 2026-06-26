#!/usr/bin/env python3
"""
FlowCrawl — Stealth web scraper with automatic bot-bypass escalation.
Uses Scrapling's three-tier fetcher cascade to punch through Cloudflare and friends.

Usage:
  flowcrawl <url> [options]

Options:
  --deep            Spider the whole site (follow internal links)
  --depth N         Max crawl depth (default: 3)
  --limit N         Max pages to crawl (default: 50)
  --format md|txt   Output format: markdown (default) or plain text
  --output DIR      Output directory (default: ./flowcrawl-output)
  --combine         Merge all pages into a single file
  --quiet           Suppress progress output
  --json            Output metadata as JSON
"""

import sys
import os
import re
import json
import time
import argparse
from pathlib import Path
from urllib.parse import urlparse, urljoin, urldefrag
from collections import deque

try:
    from scrapling import Fetcher, StealthyFetcher, DynamicFetcher
except ImportError:
    print("❌ Scrapling not installed. Run: pip install scrapling", file=sys.stderr)
    sys.exit(1)


# ─── ANSI colors ──────────────────────────────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

BANNER = f"""
{CYAN}{BOLD}  ███████╗██╗      ██████╗ ██╗    ██╗███████╗ ██████╗██████╗  █████╗ ██████╗ {RESET}
{CYAN}{BOLD}  ██╔════╝██║     ██╔═══██╗██║    ██║██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗{RESET}
{CYAN}{BOLD}  █████╗  ██║     ██║   ██║██║ █╗ ██║███████╗██║     ██████╔╝███████║██████╔╝{RESET}
{CYAN}{BOLD}  ██╔══╝  ██║     ██║   ██║██║███╗██║╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ {RESET}
{CYAN}{BOLD}  ██║     ███████╗╚██████╔╝╚███╔███╔╝███████║╚██████╗██║  ██║██║  ██║██║     {RESET}
{CYAN}{BOLD}  ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     {RESET}
{DIM}  Stealth web scraper. Like Firecrawl. But free.{RESET}
"""


# ─── Bot detection heuristics ─────────────────────────────────────────────────
BOT_STATUS_CODES  = {403, 429, 503, 520, 521, 522, 523, 524, 525, 526}
BOT_BODY_SIGNALS  = [
    "checking your browser", "cf-browser-verification", "just a moment",
    "enable javascript", "ddos protection", "ray id", "cloudflare",
    "access denied", "captcha", "bot detection",
]
SKIP_EXTENSIONS = {
    ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",
    ".mp4", ".mp3", ".zip", ".gz", ".tar", ".exe", ".dmg",
    ".css", ".js", ".ico", ".woff", ".woff2", ".ttf",
}
SKIP_URL_PATTERNS = [
    r"/cdn-cgi/", r"/wp-admin/", r"#", r"\?.*utm_",
    r"/reservations?/", r"/booking/", r"/checkout/", r"/cart/",
    r"/login", r"/logout", r"/signin", r"/register",
]


def is_bot_blocked(page) -> bool:
    """Detect if a page response indicates bot blocking."""
    if page is None:
        return True
    status = getattr(page, "status", 200)
    if status in BOT_STATUS_CODES:
        return True
    content = ""
    try:
        content = page.html_content.lower() if hasattr(page, "html_content") else str(page).lower()
    except Exception:
        pass
    return any(sig in content for sig in BOT_BODY_SIGNALS)


def should_skip_url(url: str) -> bool:
    """Skip non-content URLs."""
    parsed = urlparse(url)
    ext = Path(parsed.path).suffix.lower()
    if ext in SKIP_EXTENSIONS:
        return True
    for pat in SKIP_URL_PATTERNS:
        if re.search(pat, url, re.IGNORECASE):
            return True
    return False


def normalize_url(url: str) -> str:
    """Remove fragments, trailing slashes normalisation."""
    url, _ = urldefrag(url)
    return url.rstrip("/") if url.endswith("/") and url.count("/") > 3 else url


def is_internal(url: str, base_domain: str) -> bool:
    """Check if a URL belongs to the same domain."""
    return urlparse(url).netloc == base_domain or urlparse(url).netloc == ""


def extract_links(page, base_url: str, base_domain: str) -> list[str]:
    """Pull all internal links from a page."""
    links = []
    try:
        anchors = page.css("a[href]")
        for a in anchors:
            href = a.attrib.get("href", "").strip()
            if not href:
                continue
            full = normalize_url(urljoin(base_url, href))
            parsed = urlparse(full)
            if parsed.scheme not in ("http", "https"):
                continue
            if not is_internal(full, base_domain):
                continue
            if should_skip_url(full):
                continue
            links.append(full)
    except Exception:
        pass
    return links


def page_to_markdown(page, url: str) -> str:
    """Extract clean markdown from a page."""
    lines = [f"# {url}\n"]
    try:
        # Try markdown property first
        if hasattr(page, "markdown"):
            md = page.markdown
            if md and len(md.strip()) > 50:
                return f"# Source: {url}\n\n{md}"
    except Exception:
        pass

    # Fallback: extract text content
    try:
        # Remove script/style noise
        title_els = page.css("title")
        title = title_els[0].text if title_els else ""
        if title:
            lines.append(f"# {title}\n")

        # Try to get main content area
        for selector in ["main", "article", '[role="main"]', ".content", "#content", "body"]:
            els = page.css(selector)
            if els:
                text = els[0].get_text(separator="\n", strip=True) if hasattr(els[0], "get_text") else els[0].text
                if text and len(text.strip()) > 100:
                    lines.append(text)
                    break
    except Exception as e:
        lines.append(f"[extraction error: {e}]")

    return "\n".join(lines)


# ─── Three-tier fetcher cascade ────────────────────────────────────────────────
def fetch_page(url: str, quiet: bool = False) -> tuple:
    """
    Try fetchers in escalating order:
      Tier 1: Fetcher        — fast plain HTTP, no overhead
      Tier 2: StealthyFetcher — TLS fingerprint spoof, Cloudflare bypass
      Tier 3: DynamicFetcher  — full JS execution fallback

    Returns (page, tier_used) or (None, None) on total failure.
    """
    def log(msg):
        if not quiet:
            print(msg)

    # Tier 1: Plain HTTP
    try:
        log(f"  {DIM}[T1]{RESET} Plain HTTP...")
        page = Fetcher().get(url, timeout=15, follow_redirects=True)
        if not is_bot_blocked(page):
            log(f"  {GREEN}✓ Tier 1 succeeded{RESET}")
            return page, 1
        log(f"  {YELLOW}⚡ Tier 1 blocked — escalating to stealth{RESET}")
    except Exception as e:
        log(f"  {YELLOW}⚡ Tier 1 failed ({e}) — escalating{RESET}")

    # Tier 2: StealthyFetcher (Playwright + stealth plugins)
    try:
        log(f"  {DIM}[T2]{RESET} Stealth mode (TLS spoof + browser fingerprint)...")
        page = StealthyFetcher().fetch(url, timeout=30, headless=True)
        if not is_bot_blocked(page):
            log(f"  {GREEN}✓ Tier 2 succeeded{RESET}")
            return page, 2
        log(f"  {YELLOW}⚡ Tier 2 blocked — escalating to dynamic{RESET}")
    except Exception as e:
        log(f"  {YELLOW}⚡ Tier 2 failed ({e}) — escalating{RESET}")

    # Tier 3: DynamicFetcher (full JS execution)
    try:
        log(f"  {DIM}[T3]{RESET} Dynamic mode (full JS execution)...")
        page = DynamicFetcher().fetch(url, timeout=45, headless=True)
        if not is_bot_blocked(page):
            log(f"  {GREEN}✓ Tier 3 succeeded{RESET}")
            return page, 3
        log(f"  {RED}✗ All tiers blocked{RESET}")
        return None, None
    except Exception as e:
        log(f"  {RED}✗ Tier 3 failed ({e}){RESET}")
        return None, None


# ─── Core scraping logic ───────────────────────────────────────────────────────
def scrape_single(url: str, args) -> dict:
    """Scrape a single URL."""
    if not args.quiet:
        print(f"\n{CYAN}→{RESET} {url}")

    page, tier = fetch_page(url, args.quiet)
    if page is None:
        return {"url": url, "success": False, "error": "All fetcher tiers blocked"}

    content = page_to_markdown(page, url)
    return {
        "url": url,
        "success": True,
        "tier": tier,
        "content": content,
        "length": len(content),
    }


def scrape_deep(start_url: str, args) -> list[dict]:
    """Spider an entire site, following internal links."""
    parsed = urlparse(start_url)
    base_domain = parsed.netloc
    visited = set()
    queue = deque([(start_url, 0)])
    results = []
    page_count = 0

    if not args.quiet:
        print(f"\n{CYAN}{BOLD}Deep crawl:{RESET} {start_url}")
        print(f"{DIM}Domain: {base_domain} | Max depth: {args.depth} | Max pages: {args.limit}{RESET}\n")

    while queue and page_count < args.limit:
        url, depth = queue.popleft()
        url = normalize_url(url)

        if url in visited or should_skip_url(url):
            continue
        visited.add(url)

        if not args.quiet:
            print(f"\n{BOLD}[{page_count + 1}/{args.limit}]{RESET} depth={depth} {url}")

        page, tier = fetch_page(url, args.quiet)
        if page is None:
            results.append({"url": url, "success": False, "error": "All tiers blocked"})
            page_count += 1
            continue

        content = page_to_markdown(page, url)
        results.append({
            "url": url,
            "success": True,
            "tier": tier,
            "content": content,
            "length": len(content),
            "depth": depth,
        })
        page_count += 1

        # Queue new links if not at max depth
        if depth < args.depth:
            links = extract_links(page, url, base_domain)
            new_links = [l for l in links if l not in visited]
            if not args.quiet and new_links:
                print(f"  {DIM}Found {len(new_links)} new links{RESET}")
            for link in new_links:
                if link not in visited:
                    queue.append((link, depth + 1))

        time.sleep(0.5)  # Polite delay

    if not args.quiet:
        print(f"\n{GREEN}✓ Crawl complete: {page_count} pages scraped{RESET}")

    return results


# ─── Output helpers ────────────────────────────────────────────────────────────
def save_results(results: list[dict], args, start_url: str):
    """Write results to output directory."""
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = re.sub(r"[^\w\-]", "-", urlparse(start_url).netloc)
    saved = []

    for i, r in enumerate(results):
        if not r.get("success"):
            continue
        content = r.get("content", "")
        ext = ".md" if args.format == "md" else ".txt"
        filename = f"page-{i+1:03d}{ext}" if args.deep else f"{slug}{ext}"
        filepath = out_dir / filename
        filepath.write_text(content, encoding="utf-8")
        saved.append(str(filepath))

    if args.combine and len(saved) > 1:
        combined = "\n\n---\n\n".join(
            Path(f).read_text(encoding="utf-8") for f in saved
        )
        combined_path = out_dir / f"{slug}-combined.md"
        combined_path.write_text(combined, encoding="utf-8")
        if not args.quiet:
            print(f"\n{GREEN}📄 Combined output:{RESET} {combined_path}")

    return saved


# ─── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="FlowCrawl — stealth web scraper with auto bot-bypass escalation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  flowcrawl https://example.com
  flowcrawl https://example.com --deep --limit 20 --combine
  flowcrawl https://example.com --format txt --output ./data
  flowcrawl https://example.com --json
        """
    )
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--deep",    action="store_true",  help="Spider the whole site")
    parser.add_argument("--depth",   type=int, default=3,  help="Max crawl depth (default: 3)")
    parser.add_argument("--limit",   type=int, default=50, help="Max pages (default: 50)")
    parser.add_argument("--format",  choices=["md", "txt"], default="md", help="Output format")
    parser.add_argument("--output",  default="./flowcrawl-output", help="Output directory")
    parser.add_argument("--combine", action="store_true",  help="Merge all pages into one file")
    parser.add_argument("--quiet",   action="store_true",  help="Suppress progress output")
    parser.add_argument("--json",    action="store_true",  help="Print metadata as JSON")

    args = parser.parse_args()

    if not args.quiet:
        print(BANNER)

    # Validate URL
    if not args.url.startswith(("http://", "https://")):
        args.url = "https://" + args.url

    start = time.time()

    if args.deep:
        results = scrape_deep(args.url, args)
    else:
        result = scrape_single(args.url, args)
        results = [result]

    # Print to stdout if no output dir specified and single URL
    if not args.deep and results and results[0].get("success"):
        content = results[0]["content"]
        if not args.json:
            print(f"\n{'-'*60}\n")
            print(content)
        else:
            print(json.dumps({
                "url": args.url,
                "tier": results[0].get("tier"),
                "length": results[0].get("length"),
                "content": content,
            }, indent=2))
        return

    # Save to files for deep crawl
    if results:
        saved = save_results(results, args, args.url)
        successes = sum(1 for r in results if r.get("success"))
        elapsed = time.time() - start

        if args.json:
            print(json.dumps({
                "url": args.url,
                "pages_scraped": successes,
                "pages_failed": len(results) - successes,
                "elapsed_seconds": round(elapsed, 2),
                "files": saved,
            }, indent=2))
        elif not args.quiet:
            print(f"\n{GREEN}{BOLD}✓ Done!{RESET}")
            print(f"  Pages: {successes}/{len(results)} successful")
            print(f"  Time:  {elapsed:.1f}s")
            print(f"  Files: {args.output}/")


if __name__ == "__main__":
    main()
