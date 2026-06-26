#!/usr/bin/env python3
"""
scrape.py — Playwright + curl scraper for competitor-radar.

Modes:
  --discover <homepage_url>          Auto-detect pricing, blog, RSS from sitemap + common paths
  --baseline <slug>                  First-time snapshot of all configured URLs
  --weekly <slug>                    Weekly scrape run (all configured URLs)
  --page <slug> <page_type> <url>    Scrape a single page by type
"""

from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
COMPETITORS_FILE = DATA_DIR / "competitors.json"

TODAY = date.today().isoformat()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_competitors() -> dict:
    if not COMPETITORS_FILE.exists():
        return {"competitors": []}
    return json.loads(COMPETITORS_FILE.read_text())


def get_competitor(slug: str) -> dict | None:
    data = load_competitors()
    return next((c for c in data["competitors"] if c["slug"] == slug), None)


def snapshot_path(slug: str, page_type: str, suffix: str = "html") -> Path:
    d = SNAPSHOTS_DIR / slug
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{page_type}_{TODAY}.{suffix}"


def latest_snapshot(slug: str, page_type: str, suffix: str = "html") -> Path | None:
    d = SNAPSHOTS_DIR / slug
    if not d.exists():
        return None
    files = sorted(d.glob(f"{page_type}_*.{suffix}"), reverse=True)
    return files[0] if files else None


def previous_snapshot(slug: str, page_type: str, suffix: str = "html") -> Path | None:
    """Second-most-recent snapshot — used for diffing against today's scrape."""
    d = SNAPSHOTS_DIR / slug
    if not d.exists():
        return None
    files = sorted(d.glob(f"{page_type}_*.{suffix}"), reverse=True)
    return files[1] if len(files) > 1 else files[0] if files else None


# ---------------------------------------------------------------------------
# curl-based scrape (fast, for simple/server-rendered pages)
# ---------------------------------------------------------------------------

def curl_scrape(url: str, timeout: int = 15) -> str | None:
    """Fetch page HTML via curl. Returns text or None on failure."""
    try:
        result = subprocess.run(
            [
                "curl", "-sL",
                "--max-time", str(timeout),
                "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/122.0.0.0 Safari/537.36",
                "--compressed",
                url,
            ],
            capture_output=True, text=True, timeout=timeout + 5
        )
        if result.returncode != 0 or not result.stdout.strip():
            return None
        return result.stdout
    except Exception as e:
        print(f"[curl] Error fetching {url}: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Playwright-based scrape (for JS-rendered pages like pricing)
# ---------------------------------------------------------------------------

def playwright_scrape(url: str, wait_selector: str | None = None) -> str | None:
    """
    Fetch page HTML via Playwright headless Chromium.
    Falls back to curl if playwright is not installed.
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        print("[playwright] Not installed, falling back to curl", file=sys.stderr)
        return curl_scrape(url)

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            ctx = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/122.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 900},
            )
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            if wait_selector:
                try:
                    page.wait_for_selector(wait_selector, timeout=5000)
                except PWTimeout:
                    pass  # proceed with whatever loaded
            html = page.content()
            browser.close()
            return html
    except Exception as e:
        print(f"[playwright] Error fetching {url}: {e}", file=sys.stderr)
        return curl_scrape(url)


# ---------------------------------------------------------------------------
# Text extraction (strips HTML tags + boilerplate)
# ---------------------------------------------------------------------------

def extract_text(html: str) -> str:
    """
    Strip HTML to readable text. Removes nav, footer, script, style.
    Uses html2text if available, otherwise a simple regex approach.
    """
    try:
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_emphasis = False
        h.body_width = 0
        return h.handle(html)
    except ImportError:
        # Basic fallback: strip tags
        text = re.sub(r"<(script|style|nav|footer|header)[^>]*>.*?</\1>", "", html,
                      flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()


# ---------------------------------------------------------------------------
# RSS feed detection
# ---------------------------------------------------------------------------

def detect_rss(homepage_url: str, html: str) -> str | None:
    """Find RSS/Atom feed URL from page HTML or common paths."""
    # From <link rel="alternate"> tags
    matches = re.findall(
        r'<link[^>]+(?:application/rss\+xml|application/atom\+xml)[^>]+'
        r'href=["\']([^"\']+)["\']',
        html, re.IGNORECASE
    )
    if not matches:
        matches = re.findall(
            r'<link[^>]+href=["\']([^"\']+)["\'][^>]+'
            r'(?:application/rss\+xml|application/atom\+xml)',
            html, re.IGNORECASE
        )
    if matches:
        return urljoin(homepage_url, matches[0])

    # Try common paths
    base = f"{urlparse(homepage_url).scheme}://{urlparse(homepage_url).netloc}"
    for path in ["/feed.xml", "/feed", "/rss.xml", "/rss", "/atom.xml",
                 "/blog/feed.xml", "/blog/rss.xml", "/blog/feed"]:
        candidate = base + path
        resp = curl_scrape(candidate, timeout=5)
        if resp and ("<rss" in resp or "<feed" in resp or "<channel" in resp):
            return candidate
    return None


# ---------------------------------------------------------------------------
# URL auto-discovery
# ---------------------------------------------------------------------------

def discover_urls(homepage_url: str) -> dict:
    """
    Given only a homepage URL, attempt to find pricing, blog, changelog, RSS.
    Returns dict of page_type -> url.
    """
    print(f"[discover] Probing {homepage_url}...")
    found: dict[str, str] = {}

    homepage_html = curl_scrape(homepage_url)
    if not homepage_html:
        homepage_html = playwright_scrape(homepage_url)
    if not homepage_html:
        print("[discover] Could not fetch homepage", file=sys.stderr)
        return found

    base = f"{urlparse(homepage_url).scheme}://{urlparse(homepage_url).netloc}"

    # Pricing
    for path in ["/pricing", "/plans", "/price", "/buy", "/upgrade"]:
        url = base + path
        resp = curl_scrape(url, timeout=5)
        if resp and len(resp) > 500:
            found["pricing"] = url
            print(f"[discover] pricing → {url}")
            break

    # Blog
    for path in ["/blog", "/news", "/updates", "/articles", "/posts"]:
        url = base + path
        resp = curl_scrape(url, timeout=5)
        if resp and len(resp) > 500:
            found["blog"] = url
            print(f"[discover] blog → {url}")
            break

    # Changelog
    for path in ["/changelog", "/releases", "/whatsnew", "/updates", "/release-notes"]:
        url = base + path
        resp = curl_scrape(url, timeout=5)
        if resp and len(resp) > 500:
            found["changelog"] = url
            print(f"[discover] changelog → {url}")
            break

    # RSS
    rss = detect_rss(homepage_url, homepage_html)
    if rss:
        found["rss"] = rss
        print(f"[discover] rss → {rss}")

    # Sitemap fallback
    sitemap = curl_scrape(base + "/sitemap.xml", timeout=5)
    if sitemap:
        if "pricing" not in found:
            m = re.search(r'<loc>([^<]+/pric[^<]+)</loc>', sitemap, re.IGNORECASE)
            if m:
                found["pricing"] = m.group(1)
                print(f"[discover] pricing (sitemap) → {found['pricing']}")
        if "blog" not in found:
            m = re.search(r'<loc>([^<]+/blog[^<]*)</loc>', sitemap, re.IGNORECASE)
            if m:
                found["blog"] = m.group(1)
                print(f"[discover] blog (sitemap) → {found['blog']}")

    return found


# ---------------------------------------------------------------------------
# Single-page scrape + save snapshot
# ---------------------------------------------------------------------------

def scrape_and_save(slug: str, page_type: str, url: str,
                    use_playwright: bool = False) -> dict:
    """
    Scrape url, save HTML + text snapshots. Returns result dict.
    """
    print(f"[scrape] {slug}/{page_type} → {url}")

    html = playwright_scrape(url) if use_playwright else curl_scrape(url)
    if not html:
        # Retry with playwright if curl failed
        html = playwright_scrape(url) if not use_playwright else None
    if not html:
        return {"success": False, "slug": slug, "page_type": page_type,
                "url": url, "error": "fetch_failed"}

    text = extract_text(html)

    # Save HTML snapshot
    html_path = snapshot_path(slug, page_type, "html")
    html_path.write_text(html, encoding="utf-8")

    # Save text snapshot
    txt_path = snapshot_path(slug, page_type, "txt")
    txt_path.write_text(text, encoding="utf-8")

    # Compute content hash (for quick change detection)
    content_hash = hashlib.md5(text.encode()).hexdigest()

    print(f"[scrape] Saved {html_path.name} ({len(text)} chars, hash={content_hash[:8]})")
    return {
        "success": True,
        "slug": slug,
        "page_type": page_type,
        "url": url,
        "char_count": len(text),
        "content_hash": content_hash,
        "snapshot_html": str(html_path),
        "snapshot_txt": str(txt_path),
    }


# ---------------------------------------------------------------------------
# RSS feed scrape (returns new posts since last_run date)
# ---------------------------------------------------------------------------

def scrape_rss(slug: str, rss_url: str, last_run: str | None = None) -> list[dict]:
    """
    Fetch RSS/Atom feed, return list of new posts since last_run.
    Each post: {title, url, published, summary}
    """
    try:
        import feedparser
    except ImportError:
        print("[rss] feedparser not installed, skipping RSS", file=sys.stderr)
        return []

    print(f"[rss] Fetching {rss_url}")
    feed = feedparser.parse(rss_url)
    posts = []
    cutoff = datetime.fromisoformat(last_run) if last_run else None

    for entry in feed.entries:
        pub = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            import time
            pub = datetime(*entry.published_parsed[:6])
        if cutoff and pub and pub < cutoff:
            continue
        posts.append({
            "title": getattr(entry, "title", ""),
            "url": getattr(entry, "link", ""),
            "published": pub.isoformat() if pub else None,
            "summary": getattr(entry, "summary", "")[:500],
        })

    print(f"[rss] Found {len(posts)} new posts")
    return posts


# ---------------------------------------------------------------------------
# Blog scrape fallback (no RSS)
# ---------------------------------------------------------------------------

def scrape_blog_fallback(slug: str, blog_url: str) -> list[dict]:
    """
    Scrape blog index page, extract post titles + URLs.
    Compares to previous snapshot to find new posts.
    """
    html = curl_scrape(blog_url) or playwright_scrape(blog_url)
    if not html:
        return []

    # Extract all internal links that look like blog post URLs
    base = f"{urlparse(blog_url).scheme}://{urlparse(blog_url).netloc}"
    links = re.findall(r'href=["\']([^"\'#?]+)["\']', html)
    post_links = set()
    for link in links:
        full = urljoin(base, link)
        # Heuristic: longer paths with date or slug pattern are likely posts
        path = urlparse(full).path
        if (len(path.split("/")) >= 3 and
                urlparse(full).netloc == urlparse(blog_url).netloc and
                not path.endswith(("/", ".css", ".js", ".png", ".jpg"))):
            post_links.add(full)

    # Compare to previous snapshot
    prev = previous_snapshot(slug, "blog", "txt")
    prev_content = prev.read_text(encoding="utf-8") if prev else ""
    new_posts = [{"url": u, "title": "", "published": None, "summary": ""}
                 for u in post_links if u not in prev_content]

    # Save current snapshot
    txt_path = snapshot_path(slug, "blog", "txt")
    txt_path.write_text("\n".join(sorted(post_links)), encoding="utf-8")

    print(f"[blog_fallback] Found {len(new_posts)} new posts")
    return new_posts


# ---------------------------------------------------------------------------
# Homepage hero extraction (positioning tracking)
# ---------------------------------------------------------------------------

def extract_hero(html: str) -> str:
    """Extract H1, first H2, and hero subheading text from homepage HTML."""
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL | re.IGNORECASE)
    h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.DOTALL | re.IGNORECASE)
    # Strip tags from matches
    clean = lambda s: re.sub(r"<[^>]+>", "", s).strip()
    parts = [clean(h) for h in (h1s[:1] + h2s[:2]) if clean(h)]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="competitor-radar scraper")
    parser.add_argument("--discover", metavar="URL", help="Auto-discover URLs for homepage")
    parser.add_argument("--baseline", metavar="SLUG", help="First-time baseline snapshot")
    parser.add_argument("--weekly", metavar="SLUG", help="Weekly snapshot run")
    parser.add_argument("--page", nargs=3, metavar=("SLUG", "TYPE", "URL"),
                        help="Scrape a single page")
    args = parser.parse_args()

    if args.discover:
        found = discover_urls(args.discover)
        print(json.dumps(found, indent=2))
        return

    if args.page:
        slug, page_type, url = args.page
        use_pw = page_type in ("pricing", "homepage")
        result = scrape_and_save(slug, page_type, url, use_playwright=use_pw)
        print(json.dumps(result, indent=2))
        return

    slug = args.baseline or args.weekly
    if not slug:
        parser.print_help()
        sys.exit(1)

    competitor = get_competitor(slug)
    if not competitor:
        print(f"[error] No competitor found with slug '{slug}'", file=sys.stderr)
        sys.exit(1)

    urls = competitor.get("urls", {})
    results = []

    # Pricing — use Playwright (JS-rendered)
    if urls.get("pricing"):
        results.append(scrape_and_save(slug, "pricing", urls["pricing"],
                                       use_playwright=True))

    # Homepage hero — curl is fine
    if urls.get("homepage"):
        html = curl_scrape(urls["homepage"])
        if html:
            hero = extract_hero(html)
            hero_path = snapshot_path(slug, "homepage_hero", "txt")
            hero_path.write_text(hero, encoding="utf-8")
            results.append({"success": True, "slug": slug,
                             "page_type": "homepage_hero", "url": urls["homepage"]})

    # Blog / RSS
    if urls.get("rss"):
        last_run = competitor.get("last_run")
        posts = scrape_rss(slug, urls["rss"], last_run)
        rss_path = snapshot_path(slug, "rss_posts", "json")
        rss_path.write_text(json.dumps(posts, indent=2, default=str), encoding="utf-8")
        results.append({"success": True, "slug": slug,
                         "page_type": "rss_posts", "post_count": len(posts)})
    elif urls.get("blog"):
        posts = scrape_blog_fallback(slug, urls["blog"])
        results.append({"success": bool(posts), "slug": slug,
                         "page_type": "blog_fallback", "post_count": len(posts)})

    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
