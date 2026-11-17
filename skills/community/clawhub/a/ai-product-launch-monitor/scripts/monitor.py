#!/usr/bin/env python3
"""
AI Product Launch Monitor — one-command pipeline.

Stages:
  1. RSS monitoring   — fetch AI/Tech RSS feeds, extract new product launches
  2. Product search   — enrich each launch with web search results
  3. Screenshot capture — grab screenshots of product pages
  4. Trend analysis   — score & rank launches, produce a markdown report

Usage:
  python3 monitor.py [--config CONFIG] [--output DIR] [--days N] [--no-screenshots]
                     [--feeds URL ...] [--query TERMS ...] [--verbose]

Output:
  <output>/report.md            — human-readable trend report
  <output>/launches.json        — structured data for downstream use
  <output>/screenshots/*.png    — product page screenshots
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote_plus, urlparse

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://venturebeat.com/category/ai/feed/",
    "https://feeds.feedburner.com/ProductHunt",
    "https://www.artificialintelligence-news.com/feed/",
    "https://huggingface.co/blog/feed.xml",
]

DEFAULT_QUERY_TERMS = [
    "AI product launch",
    "new AI tool release",
    "AI startup announcement",
    "generative AI product",
    "LLM launch",
]

LAUNCH_KEYWORDS = re.compile(
    r"\b(launch(?:es|ed|ing)?|release[ds]?|announce[ds]?|unveil(?:s|ed)?|"
    r"introduce[ds]?|debut(s|ed)?|roll(s|ed)? out|now available|"
    r"new (?:AI|model|tool|platform|app|product))\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Stage 1 — RSS monitoring
# ---------------------------------------------------------------------------

def fetch_rss(feed_urls, days=3, verbose=False):
    """Fetch RSS feeds and return entries within the last *days* that look like launches."""
    import feedparser
    import requests

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    entries = []

    for url in feed_urls:
        if verbose:
            print(f"[RSS] Fetching {url} …", file=sys.stderr)
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "AI-Launch-Monitor/1.0"})
            resp.raise_for_status()
            feed = feedparser.parse(resp.content)
        except Exception as exc:
            if verbose:
                print(f"[RSS] ⚠ Failed: {exc}", file=sys.stderr)
            continue

        for entry in feed.entries:
            published = _entry_date(entry)
            if published and published < cutoff:
                continue
            title = entry.get("title", "")
            summary = entry.get("summary", entry.get("description", ""))
            link = entry.get("link", "")
            if not (title and link):
                continue
            is_launch = bool(LAUNCH_KEYWORDS.search(title + " " + summary))
            entries.append({
                "title": _clean(title),
                "link": link,
                "summary": _clean(summary)[:500],
                "published": published.isoformat() if published else None,
                "source": feed.feed.get("title", urlparse(url).netloc),
                "is_launch_signal": is_launch,
            })

    # Deduplicate by link
    seen = set()
    unique = []
    for e in entries:
        key = e["link"]
        if key in seen:
            continue
        seen.add(key)
        unique.append(e)

    # Prioritise launch signals first, then by date
    unique.sort(key=lambda e: (not e["is_launch_signal"], e["published"] or ""), reverse=False)
    if verbose:
        print(f"[RSS] {len(unique)} entries collected", file=sys.stderr)
    return unique


def _entry_date(entry):
    for attr in ("published_parsed", "updated_parsed"):
        tp = entry.get(attr)
        if tp:
            try:
                return datetime(*tp[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


def _clean(text):
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()

# ---------------------------------------------------------------------------
# Stage 2 — Product info search (Brave Search API via web_search fallback)
# ---------------------------------------------------------------------------

def search_product_info(launches, query_terms, verbose=False, max_search=10):
    """Enrich launches with additional search context.

    Uses the Brave Search API if BRAVE_API_KEY is set; otherwise does a
    lightweight DuckDuckGo HTML scrape as fallback.
    Limits enrichment to top *max_search* launches to avoid hanging on network.
    """
    api_key = os.environ.get("BRAVE_API_KEY")
    # Only enrich launch signals first, then others up to max_search
    signal = [l for l in launches if l.get("is_launch_signal")]
    rest = [l for l in launches if not l.get("is_launch_signal")]
    to_enrich = (signal + rest)[:max_search]
    enriched_set = {id(l) for l in to_enrich}

    for launch in to_enrich:
        if verbose:
            print(f"[SEARCH] Enriching: {launch['title'][:60]}…", file=sys.stderr)
        query = f"{launch['title']} AI product"
        results = []
        if api_key:
            results = _brave_search(query, api_key)
        else:
            results = _ddg_search(query)
        launch["search_results"] = results[:5]
        launch["product_name"] = _guess_product_name(launch["title"])

    # Mark remaining as not enriched
    for launch in launches:
        if id(launch) not in enriched_set:
            launch["search_results"] = []
            launch["product_name"] = _guess_product_name(launch["title"])
    return launches


def _brave_search(query, api_key):
    import requests
    try:
        resp = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            params={"q": query, "count": 5},
            headers={"Accept": "application/json", "X-Subscription-Token": api_key},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        return [
            {"title": r.get("title", ""), "url": r.get("url", ""), "snippet": r.get("description", "")}
            for r in data.get("web", {}).get("results", [])
        ]
    except Exception:
        return []


def _ddg_search(query):
    """Fallback: scrape DuckDuckGo HTML (no API key needed)."""
    import requests
    from bs4 import BeautifulSoup
    try:
        resp = requests.post(
            "https://html.duckduckgo.com/html/",
            data={"q": query},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=8,
        )
        if resp.status_code != 200:
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for r in soup.select(".result")[:5]:
            a = r.select_one(".result__a")
            sn = r.select_one(".result__snippet")
            if a:
                results.append({
                    "title": a.get_text(strip=True),
                    "url": a.get("href", ""),
                    "snippet": sn.get_text(strip=True) if sn else "",
                })
        return results
    except Exception:
        return []


def _guess_product_name(title):
    """Heuristic: try to pull a product name from the title."""
    # Remove common verbs
    cleaned = re.sub(
        r"^(.*?\b(launches|releases|announces|unveils|introduces|debuts)\s+)",
        "",
        title,
        flags=re.IGNORECASE,
    )
    # Take up to first comma or dash
    cleaned = re.split(r"[,—–-]", cleaned)[0].strip()
    return cleaned[:80] if cleaned else title[:80]

# ---------------------------------------------------------------------------
# Stage 3 — Screenshot capture
# ---------------------------------------------------------------------------

def capture_screenshots(launches, output_dir, verbose=False):
    """Use Playwright (headless Chromium) to screenshot product pages."""
    shot_dir = output_dir / "screenshots"
    shot_dir.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        if verbose:
            print("[SHOTS] Playwright not installed, skipping screenshots", file=sys.stderr)
        for l in launches:
            l["screenshot"] = None
        return launches

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        for launch in launches:
            url = launch["link"]
            fname = hashlib.md5(url.encode()).hexdigest()[:10] + ".png"
            fpath = shot_dir / fname
            try:
                page.goto(url, timeout=20000, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
                page.screenshot(path=str(fpath), full_page=False)
                launch["screenshot"] = str(fpath)
                if verbose:
                    print(f"[SHOTS] ✓ {fname}", file=sys.stderr)
            except Exception as exc:
                launch["screenshot"] = None
                if verbose:
                    print(f"[SHOTS] ⚠ {url[:50]}… {exc}", file=sys.stderr)

        browser.close()
    return launches

# ---------------------------------------------------------------------------
# Stage 4 — Trend analysis
# ---------------------------------------------------------------------------

TREND_CATEGORIES = {
    "LLM / Foundation Models": re.compile(r"\b(GPT|LLM|language model|foundation model|Claude|Gemini|Llama|Mistral)\b", re.I),
    "Image / Video Gen": re.compile(r"\b(image|video|image-to-video|text-to-image|text-to-video|diffusion|Sora|Midjourney|Stable Diffusion)\b", re.I),
    "Agent / Automation": re.compile(r"\b(agent|autonomous|automation|workflow|copilot|assistant)\b", re.I),
    "Developer Tools": re.compile(r"\b(SDK|API|developer|coding|code|IDE|framework|open-source|open source)\b", re.I),
    "Enterprise / B2B": re.compile(r"\b(enterprise|business|B2B|SaaS|platform|company)\b", re.I),
    "Consumer / App": re.compile(r"\b(app|consumer|chatbot|mobile|user|personal)\b", re.I),
    "Healthcare / Science": re.compile(r"\b(health|medical|drug|science|research|biology|protein)\b", re.I),
}

def analyze_trends(launches, verbose=False):
    """Score and categorise launches; compute trend counts."""
    category_counts = {}
    for launch in launches:
        text = launch["title"] + " " + launch["summary"]
        # Categorise
        cats = [cat for cat, pat in TREND_CATEGORIES.items() if pat.search(text)]
        launch["categories"] = cats or ["Other"]
        for c in launch["categories"]:
            category_counts[c] = category_counts.get(c, 0) + 1

        # Score: launch signal + source diversity + recency
        score = 0
        if launch["is_launch_signal"]:
            score += 30
        if launch.get("search_results"):
            score += min(len(launch["search_results"]) * 5, 25)
        if launch.get("screenshot"):
            score += 10
        # Recency bonus
        if launch.get("published"):
            try:
                pub = datetime.fromisoformat(launch["published"])
                hours_ago = (datetime.now(timezone.utc) - pub).total_seconds() / 3600
                score += max(0, 35 - hours_ago * 0.5)
            except Exception:
                pass
        launch["trend_score"] = round(score, 1)

    launches.sort(key=lambda l: l["trend_score"], reverse=True)

    summary = {
        "total_launches": len(launches),
        "launch_signals": sum(1 for l in launches if l["is_launch_signal"]),
        "categories": dict(sorted(category_counts.items(), key=lambda x: -x[1])),
        "top_scored": [
            {"title": l["title"], "score": l["trend_score"], "product_name": l["product_name"]}
            for l in launches[:10]
        ],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    if verbose:
        print(f"[TRENDS] Scored {len(launches)} launches", file=sys.stderr)
    return launches, summary

# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(launches, summary, output_dir):
    """Write report.md and launches.json."""
    lines = [
        f"# 🚀 AI Product Launch Monitor Report",
        f"",
        f"**Generated:** {summary['generated_at']}",
        f"**Total entries:** {summary['total_launches']}  |  **Launch signals:** {summary['launch_signals']}",
        f"",
        f"## 📊 Trend Overview",
        f"",
        f"| Category | Count |",
        f"|----------|-------|",
    ]
    for cat, count in summary["categories"].items():
        lines.append(f"| {cat} | {count} |")

    lines += ["", "## 🔥 Top Launches", ""]
    for i, l in enumerate(summary["top_scored"], 1):
        lines.append(f"{i}. **{l['title']}** (score: {l['score']})")

    lines += ["", "## 📋 All Entries", ""]
    for l in launches:
        shot = f"  \n  📸 Screenshot: `{l['screenshot']}`" if l.get("screenshot") else ""
        cats = ", ".join(l.get("categories", []))
        lines.append(f"### {l['title']}")
        lines.append(f"- **Source:** {l['source']}")
        lines.append(f"- **Link:** {l['link']}")
        lines.append(f"- **Published:** {l.get('published', 'N/A')}")
        lines.append(f"- **Categories:** {cats}")
        lines.append(f"- **Trend Score:** {l['trend_score']}")
        lines.append(f"- **Summary:** {l['summary'][:300]}")
        if l.get("search_results"):
            lines.append(f"- **Related:**")
            for r in l["search_results"][:3]:
                lines.append(f"  - [{r['title']}]({r['url']})")
        if shot:
            lines.append(shot)
        lines.append("")

    report_path = output_dir / "report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    json_path = output_dir / "launches.json"
    json_path.write_text(
        json.dumps({"summary": summary, "launches": launches}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report_path, json_path

# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI Product Launch Monitor — full pipeline")
    parser.add_argument("--config", help="Path to JSON config file (feeds, query_terms, days)")
    parser.add_argument("--output", default="./output", help="Output directory (default: ./output)")
    parser.add_argument("--days", type=int, default=3, help="Look-back window in days (default: 3)")
    parser.add_argument("--no-screenshots", action="store_true", help="Skip screenshot stage")
    parser.add_argument("--no-search", action="store_true", help="Skip web search enrichment")
    parser.add_argument("--feeds", nargs="*", help="Override RSS feed URLs")
    parser.add_argument("--query", nargs="*", help="Extra search query terms")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    # Config
    feeds = DEFAULT_FEEDS
    query_terms = DEFAULT_QUERY_TERMS
    days = args.days
    if args.config:
        with open(args.config) as f:
            cfg = json.load(f)
        feeds = cfg.get("feeds", feeds)
        query_terms = cfg.get("query_terms", query_terms)
        days = cfg.get("days", days)
    if args.feeds:
        feeds = args.feeds
    if args.query:
        query_terms = args.query

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Stage 1
    print("▶ Stage 1/4: RSS monitoring …", file=sys.stderr)
    launches = fetch_rss(feeds, days=days, verbose=args.verbose)
    if not launches:
        print("⚠ No RSS entries found. Check feed URLs or network.", file=sys.stderr)

    # Stage 2
    if args.no_search:
        print("▶ Stage 2/4: Search skipped (--no-search)", file=sys.stderr)
        for l in launches:
            l["search_results"] = []
            l["product_name"] = _guess_product_name(l["title"])
    else:
        print("▶ Stage 2/4: Product info search …", file=sys.stderr)
        launches = search_product_info(launches, query_terms, verbose=args.verbose)

    # Stage 3
    if args.no_screenshots:
        print("▶ Stage 3/4: Screenshots skipped (--no-screenshots)", file=sys.stderr)
        for l in launches:
            l["screenshot"] = None
    else:
        print("▶ Stage 3/4: Screenshot capture …", file=sys.stderr)
        launches = capture_screenshots(launches, output_dir, verbose=args.verbose)

    # Stage 4
    print("▶ Stage 4/4: Trend analysis …", file=sys.stderr)
    launches, summary = analyze_trends(launches, verbose=args.verbose)

    # Report
    report_path, json_path = generate_report(launches, summary, output_dir)
    print(f"\n✅ Done! Report: {report_path}", file=sys.stderr)
    print(f"   Data:   {json_path}", file=sys.stderr)
    print(f"   Entries: {summary['total_launches']}  |  Launch signals: {summary['launch_signals']}", file=sys.stderr)


if __name__ == "__main__":
    main()
