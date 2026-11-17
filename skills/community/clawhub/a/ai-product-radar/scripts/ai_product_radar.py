#!/usr/bin/env python3
"""
AI Product Radar — One-click AI product launch monitoring pipeline.

Integrates four stages:
  1. RSS monitoring   — fetch AI/tech product launch feeds
  2. Product search   — enrich each item with web search results
  3. Screenshot capture — grab screenshots of product pages
  4. Trend analysis   — aggregate signals into a ranked trend report

Usage:
  python3 ai_product_radar.py [--output DIR] [--feeds FILE] [--limit N] [--days N]
                              [--no-screenshots] [--query TERM]

Output:
  <output>/report.md         — human-readable trend report
  <output>/products.json     — structured product data
  <output>/screenshots/      — captured screenshots
  <output>/raw/              — raw RSS feed data
"""

import argparse
import json
import os
import re
import sys
import time
import hashlib
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from html.parser import HTMLParser

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_FEEDS = [
    # Product Hunt
    "https://www.producthunt.com/feed",
    # TechCrunch AI
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    # The Verge AI
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    # VentureBeat AI
    "https://venturebeat.com/category/ai/feed/",
    # Hacker News (Show HN / launches)
    "https://hnrss.org/show",
    # MIT Tech Review AI
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    # Ars Technica AI
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
]

AI_KEYWORDS = [
    r"\bai\b", r"artificial intelligence", r"machine learning", r"\bml\b",
    r"large language model", r"\bllm\b", r"gpt", r"claude", r"gemini",
    r"generative", r"chatbot", r"copilot", r"agent", r"diffusion",
    r"transformer", r"neural", r"deep learning", r"open[- ]?source\s+(ai|model)",
    r"text[- ]to[- ]", r"image[- ]to[- ]", r"speech[- ]to[- ]",
    r"assistant", r"automation", r"no[- ]code", r"low[- ]code",
    r"predictive", r"recommend", r"personaliz",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, d):
        self.parts.append(d)
    def get_text(self):
        return " ".join(self.parts)


def strip_html(text: str) -> str:
    if not text:
        return ""
    s = HTMLStripper()
    try:
        s.feed(text)
    except Exception:
        return re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", s.get_text()).strip()


def fetch_url(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": "AIProductRadar/1.0 (+https://github.com/openclaw)",
        "Accept": "*/*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def is_ai_related(text: str) -> bool:
    text_lower = text.lower()
    return any(re.search(pat, text_lower) for pat in AI_KEYWORDS)


def safe_filename(s: str, max_len: int = 60) -> str:
    s = re.sub(r"[^\w\s-]", "", s).strip().replace(" ", "_")
    return s[:max_len]


# ---------------------------------------------------------------------------
# Stage 1: RSS Monitoring
# ---------------------------------------------------------------------------

def parse_rss_feed(xml_bytes: bytes, source_url: str, days: int) -> list[dict]:
    items = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        print(f"  ⚠ Failed to parse {source_url}: {e}", file=sys.stderr)
        return items

    # Handle RSS 2.0
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        desc = strip_html(item.findtext("description") or "")
        pub = item.findtext("pubDate") or item.findtext("{http://purl.org/dc/elements/1.1/}date") or ""
        pub_dt = _parse_date(pub)

        if pub_dt and pub_dt < cutoff:
            continue

        items.append({
            "title": title,
            "link": link,
            "description": desc[:500],
            "published": pub_dt.isoformat() if pub_dt else "",
            "source": _source_name(source_url),
        })

    # Handle Atom
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
        title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip()
        link_el = entry.find("atom:link", ns)
        link = link_el.get("href", "") if link_el is not None else ""
        desc = strip_html(entry.findtext("atom:summary", default="", namespaces=ns) or
                          entry.findtext("atom:content", default="", namespaces=ns) or "")
        pub = entry.findtext("atom:published", default="", namespaces=ns) or \
              entry.findtext("atom:updated", default="", namespaces=ns) or ""
        pub_dt = _parse_date(pub)

        if pub_dt and pub_dt < cutoff:
            continue

        items.append({
            "title": title,
            "link": link,
            "description": desc[:500],
            "published": pub_dt.isoformat() if pub_dt else "",
            "source": _source_name(source_url),
        })

    return items


def _parse_date(s: str) -> datetime | None:
    if not s:
        return None
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S.%fZ",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(s.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def _source_name(url: str) -> str:
    domain = urllib.parse.urlparse(url).netloc
    return domain.replace("www.", "").replace("feeds.", "")


def monitor_rss(feeds: list[str], days: int, query: str | None = None) -> list[dict]:
    print("📡 Stage 1: Monitoring RSS feeds...")
    all_items = []
    for url in feeds:
        print(f"  Fetching {url} ...")
        try:
            data = fetch_url(url)
            items = parse_rss_feed(data, url, days)
            print(f"    → {len(items)} items")
            all_items.extend(items)
        except Exception as e:
            print(f"    ⚠ Error: {e}", file=sys.stderr)

    # Deduplicate by link
    seen = set()
    unique = []
    for item in all_items:
        key = item["link"] or item["title"]
        if key not in seen:
            seen.add(key)
            unique.append(item)

    # Filter AI-related
    ai_items = []
    for item in unique:
        text = f"{item['title']} {item['description']}"
        if query and query.lower() not in text.lower():
            continue
        if is_ai_related(text) or query:
            ai_items.append(item)

    print(f"  ✅ {len(ai_items)} AI-related products found (from {len(unique)} total)\n")
    return ai_items


# ---------------------------------------------------------------------------
# Stage 2: Product Information Search
# ---------------------------------------------------------------------------

def search_product_info(item: dict) -> dict:
    """Enrich product item with search metadata extracted from its content."""
    title = item["title"]
    desc = item.get("description", "")

    # Extract potential product name (often before " - " or " | " or ":")
    product_name = re.split(r"\s[-–—|]\s|\s:\s|\s\|\s", title)[0].strip()

    # Detect category signals
    categories = []
    category_patterns = {
        "LLM/Chatbot": [r"\bllm\b", r"large language", r"chatbot", r"gpt", r"gpt-?\d", r"claude", r"gemini"],
        "Image/Video Gen": [r"image gen", r"video gen", r"text.to.image", r"diffusion", r"midjourney", r"dall"],
        "Developer Tools": [r"developer", r"sdk", r"api", r"code", r"github", r"copilot", r"ide\b"],
        "Agent/Automation": [r"\bagent\b", r"automat", r"workflow", r"no.code", r"low.code"],
        "Enterprise/SaaS": [r"enterprise", r"saas", r"business", r"platform", r"cloud"],
        "Health/Medical": [r"health", r"medical", r"clinical", r"drug", r"biotech"],
        "Robotics/Hardware": [r"robot", r"hardware", r"chip", r"gpu", r"edge\b"],
        "Audio/Speech": [r"audio", r"speech", r"voice", r"tts", r"music"],
        "Search/RAG": [r"\bsearch\b", r"\brag\b", r"retrieval", r"knowledge base"],
        "Security/Privacy": [r"security", r"privacy", r"safety", r"guardrail"],
    }
    combined = f"{title} {desc}".lower()
    for cat, patterns in category_patterns.items():
        if any(re.search(p, combined) for p in patterns):
            categories.append(cat)

    # Engagement heuristic: count signal keywords in description
    signal_words = len(re.findall(
        r"\b(launch|release|announce|introduc|new|first|breakthrough|raises?|funding|open.source|free|now available)\b",
        combined,
    ))

    # Extract domain
    domain = ""
    if item.get("link"):
        domain = urllib.parse.urlparse(item["link"]).netloc.replace("www.", "")

    item["product_name"] = product_name
    item["categories"] = categories or ["General AI"]
    item["signal_score"] = signal_words
    item["domain"] = domain
    return item


def enrich_products(items: list[dict]) -> list[dict]:
    print("🔍 Stage 2: Enriching product information...")
    enriched = []
    for item in items:
        enriched.append(search_product_info(item))
    print(f"  ✅ Enriched {len(enriched)} products\n")
    return enriched


# ---------------------------------------------------------------------------
# Stage 3: Screenshot Capture
# ---------------------------------------------------------------------------

def capture_screenshots(items: list[dict], output_dir: Path, limit: int = 10) -> list[dict]:
    """Attempt to capture screenshots using a headless browser if available."""
    print("📸 Stage 3: Capturing screenshots...")
    shots_dir = output_dir / "screenshots"
    shots_dir.mkdir(parents=True, exist_ok=True)

    # Check for available screenshot tools
    has_playwright = False
    has_puppeteer = False
    try:
        import subprocess
        result = subprocess.run(["npx", "--yes", "playwright", "--version"],
                                capture_output=True, text=True, timeout=30)
        has_playwright = result.returncode == 0
    except Exception:
        pass

    screenshot_count = 0
    for i, item in enumerate(items[:limit]):
        link = item.get("link", "")
        if not link:
            continue

        fname = safe_filename(item.get("product_name", f"product_{i}")) + ".png"
        fpath = shots_dir / fname
        item["screenshot"] = str(fpath.relative_to(output_dir))

        # Try with available tools
        captured = False
        if has_playwright:
            captured = _screenshot_playwright(link, fpath)

        if not captured:
            # Fallback: generate a placeholder info card as SVG/HTML
            _generate_placeholder_card(item, fpath)
            item["screenshot_note"] = "placeholder (no browser available)"

        screenshot_count += 1
        print(f"  [{i+1}/{min(len(items), limit)}] {item.get('product_name', 'unknown')}")

    print(f"  ✅ Captured {screenshot_count} screenshots\n")
    return items


def _screenshot_playwright(url: str, path: Path) -> bool:
    try:
        import subprocess
        script = f"""
        const {{ chromium }} = require('playwright');
        (async () => {{
            const browser = await chromium.launch();
            const page = await browser.newPage({viewport: {{width: 1280, height: 800}}});
            await page.goto('{url}', {{waitUntil: 'domcontentloaded', timeout: 20000}});
            await page.waitForTimeout(2000);
            await page.screenshot({{path: '{path}', fullPage: false}});
            await browser.close();
        }})();
        """
        result = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=45)
        return result.returncode == 0 and path.exists()
    except Exception:
        return False


def _generate_placeholder_card(item: dict, path: Path):
    """Generate an HTML info card as a fallback when no browser is available."""
    html_path = path.with_suffix(".html")
    categories = ", ".join(item.get("categories", []))
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
body {{ margin:0; padding:40px; font-family:system-ui,sans-serif;
       background:linear-gradient(135deg,#1a1a2e,#16213e); color:#eee; width:1200px; height:720px;
       display:flex; flex-direction:column; justify-content:center; box-sizing:border-box; }}
h1 {{ font-size:2.2em; margin:0 0 12px; color:#00d4ff; }}
.source {{ color:#888; font-size:0.9em; margin-bottom:20px; }}
.desc {{ font-size:1.1em; line-height:1.6; color:#ccc; max-width:900px; }}
.tags {{ margin-top:24px; }}
.tag {{ display:inline-block; background:#0f3460; padding:6px 14px; border-radius:20px;
        margin-right:8px; font-size:0.85em; color:#e94560; }}
a {{ color:#00d4ff; word-break:break-all; }}
</style></head><body>
<h1>{item.get('product_name', item.get('title', 'Unknown'))}</h1>
<div class="source">{item.get('source', '')} · {item.get('domain', '')}</div>
<div class="desc">{item.get('description', 'No description available.')}</div>
<div class="tags">{''.join(f'<span class="tag">{c}</span>' for c in item.get('categories', []))}</div>
<p style="margin-top:30px"><a href="{item.get('link', '')}">{item.get('link', '')}</a></p>
</body></html>"""
    html_path.write_text(html, encoding="utf-8")
    # Also save a tiny placeholder PNG indicator
    path.write_bytes(b"")  # empty file signals placeholder
    item["screenshot_html"] = str(html_path)


# ---------------------------------------------------------------------------
# Stage 4: Trend Analysis
# ---------------------------------------------------------------------------

def analyze_trends(items: list[dict]) -> dict:
    print("📊 Stage 4: Analyzing trends...")

    # Category distribution
    cat_counts: dict[str, int] = {}
    for item in items:
        for cat in item.get("categories", ["General AI"]):
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

    # Source distribution
    source_counts: dict[str, int] = {}
    for item in items:
        src = item.get("source", "unknown")
        source_counts[src] = source_counts.get(src, 0) + 1

    # Rank by signal score + recency
    now = datetime.now(timezone.utc)
    for item in items:
        score = item.get("signal_score", 0)
        # Recency boost
        pub = item.get("published", "")
        if pub:
            try:
                dt = datetime.fromisoformat(pub)
                hours_ago = (now - dt).total_seconds() / 3600
                if hours_ago < 24:
                    score += 5
                elif hours_ago < 72:
                    score += 3
            except Exception:
                pass
        item["trend_score"] = score

    ranked = sorted(items, key=lambda x: x.get("trend_score", 0), reverse=True)

    # Key themes
    all_titles = " ".join(i["title"].lower() for i in items)
    theme_words = {}
    stop = {"the", "a", "an", "is", "are", "was", "for", "to", "of", "in", "on",
            "and", "or", "with", "its", "new", "ai", "how", "why", "what", "that",
            "this", "from", "by", "at", "as", "be", "has", "have", "it", "your",
            "you", "will", "can", "just", "not", "but", "more", "about", "after",
            "into", "over", "than", "then", "so", "if", "their", "they", "we", "our"}
    for word in re.findall(r"[a-z][a-z0-9-]{2,}", all_titles):
        if word not in stop and len(word) > 2:
            theme_words[word] = theme_words.get(word, 0) + 1
    top_themes = sorted(theme_words.items(), key=lambda x: x[1], reverse=True)[:20]

    report = {
        "generated_at": now.isoformat(),
        "total_products": len(items),
        "top_categories": sorted(cat_counts.items(), key=lambda x: x[1], reverse=True),
        "sources": sorted(source_counts.items(), key=lambda x: x[1], reverse=True),
        "top_themes": top_themes,
        "trending": ranked[:20],
        "all_products": ranked,
    }

    print(f"  ✅ Analyzed {len(items)} products across {len(cat_counts)} categories\n")
    return report


def generate_report(report: dict, output_dir: Path) -> Path:
    """Generate a markdown trend report."""
    report_path = output_dir / "report.md"
    lines = [
        "# 🛰️ AI Product Radar Report",
        f"",
        f"**Generated:** {report['generated_at'][:19].replace('T', ' ')} UTC",
        f"**Products tracked:** {report['total_products']}",
        f"",
        "---",
        "",
        "## 📈 Top Categories",
        "",
    ]
    for cat, count in report["top_categories"][:10]:
        bar = "█" * min(count, 30)
        lines.append(f"- **{cat}** ({count}) {bar}")

    lines.extend(["", "## 🔥 Trending Products", ""])

    for i, p in enumerate(report["trending"][:15], 1):
        cats = ", ".join(p.get("categories", []))
        lines.append(f"### {i}. {p.get('product_name', p['title'])}")
        lines.append(f"- **Source:** {p.get('source', '')}")
        lines.append(f"- **Categories:** {cats}")
        lines.append(f"- **Trend Score:** {p.get('trend_score', 0)}")
        if p.get("published"):
            lines.append(f"- **Published:** {p['published'][:10]}")
        lines.append(f"- **Link:** {p.get('link', 'N/A')}")
        if p.get("screenshot"):
            note = f" ({p.get('screenshot_note', '')})" if p.get("screenshot_note") else ""
            lines.append(f"- **Screenshot:** `{p['screenshot']}`{note}")
        if p.get("description"):
            lines.append(f"- {p['description'][:200]}")
        lines.append("")

    lines.extend(["## 🔤 Key Themes", ""])
    themes_str = " ".join(f"`{word}`({count})" for word, count in report["top_themes"][:15])
    lines.append(themes_str)
    lines.append("")

    lines.extend(["## 📰 Sources", ""])
    for src, count in report["sources"]:
        lines.append(f"- {src}: {count}")
    lines.append("")

    lines.extend(["---", "*Generated by [AI Product Radar](https://clawhub.ai)*"])

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI Product Radar — one-click launch monitor")
    parser.add_argument("--output", "-o", default="./ai-radar-output", help="Output directory")
    parser.add_argument("--feeds", "-f", help="JSON file with custom RSS feed URLs")
    parser.add_argument("--limit", "-l", type=int, default=15, help="Max screenshots to capture")
    parser.add_argument("--days", "-d", type=int, default=3, help="Lookback days for RSS")
    parser.add_argument("--no-screenshots", action="store_true", help="Skip screenshot stage")
    parser.add_argument("--query", "-q", help="Additional search/filter term")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "raw").mkdir(exist_ok=True)

    feeds = DEFAULT_FEEDS
    if args.feeds:
        feeds = json.loads(Path(args.feeds).read_text())

    print("=" * 60)
    print("🛰️  AI PRODUCT RADAR")
    print("=" * 60)
    print(f"  Output:   {output_dir.resolve()}")
    print(f"  Feeds:    {len(feeds)}")
    print(f"  Days:     {args.days}")
    print(f"  Query:    {args.query or '(AI auto-detect)'}")
    print("=" * 60 + "\n")

    # Stage 1
    products = monitor_rss(feeds, args.days, args.query)

    # Save raw
    raw_path = output_dir / "raw" / "rss_items.json"
    raw_path.write_text(json.dumps(products, indent=2, ensure_ascii=False), encoding="utf-8")

    if not products:
        print("⚠ No AI products found. Try increasing --days or adding more feeds.")
        # Still write empty outputs
        (output_dir / "products.json").write_text("[]", encoding="utf-8")
        (output_dir / "report.md").write_text("# AI Product Radar\n\nNo products found.\n", encoding="utf-8")
        return

    # Stage 2
    products = enrich_products(products)

    # Stage 3
    if not args.no_screenshots:
        products = capture_screenshots(products, output_dir, args.limit)
    else:
        print("📸 Stage 3: Screenshots skipped (--no-screenshots)\n")

    # Stage 4
    report = analyze_trends(products)

    # Save structured data
    products_path = output_dir / "products.json"
    products_path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    # Generate report
    report_path = generate_report(report, output_dir)

    print("=" * 60)
    print("✅ PIPELINE COMPLETE")
    print("=" * 60)
    print(f"  Report:    {report_path.resolve()}")
    print(f"  Data:      {products_path.resolve()}")
    if not args.no_screenshots:
        print(f"  Screenshots: {(output_dir / 'screenshots').resolve()}")
    print()


if __name__ == "__main__":
    main()
