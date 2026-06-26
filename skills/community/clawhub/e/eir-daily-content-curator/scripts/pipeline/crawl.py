#!/usr/bin/env python3
"""
Phase 3: Selective Crawl — only crawl URLs that are in candidates.json.

Reads candidates.json, crawls full text via Crawl4AI (with web_fetch fallback),
extracts publish dates, saves to snippets/.

Usage:
  python3 -m pipeline.crawl
  python3 -m pipeline.crawl --dry-run
"""

import hashlib
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

from .config import (
    CANDIDATES_FILE, SNIPPETS_DIR, CRAWL4AI_URL, V9_DIR, FRESHNESS_DAYS,
    DIRECTIVES_FILE, DATA_DIR, SEARXNG_URL, SOURCE_QUALITY,
    ensure_dirs, load_json,
)
from .date_extractor import extract_publish_date
from . import grounding

CRAWL_TIMEOUT = 30          # HTTP client timeout (seconds)
PAGE_TIMEOUT_MS = 20000     # Crawl4AI Playwright navigation timeout (ms)
MIN_CONTENT_LEN = 500
MAX_CONTENT_LEN = 8000

DOMAIN_STATS_FILE = DATA_DIR / "domain_stats.json"

# Module-level cache for grounding search content (populated in main())
_search_content_cache = {}

# Build reverse lookup: domain -> tier rank (0=tier1, 1=tier2, 3=tier3, 2=unknown)
_DOMAIN_TIER = {}
for _d in SOURCE_QUALITY.get("tier1", []):
    _DOMAIN_TIER[_d] = 0
for _d in SOURCE_QUALITY.get("tier2", []):
    _DOMAIN_TIER[_d] = 1
for _d in SOURCE_QUALITY.get("tier3_unreliable", []):
    _DOMAIN_TIER[_d] = 3


def _get_tier_rank(domain):
    """Return tier rank for a domain: 0=tier1, 1=tier2, 2=unknown, 3=tier3."""
    return _DOMAIN_TIER.get(domain, 2)


# ─── Error page detection ────────────────────────────────────────────────────

_ERROR_PAGE_PATTERNS = [
    "page doesn't exist", "page not found", "404",
    "page can't be found", "no longer available",
    "article has been removed", "content you requested",
    "couldn't find the page", "ooops",
]


def is_error_page(content):
    """Detect 404/error pages by checking for common error patterns."""
    if not content:
        return False
    # Only check first 2000 chars — error messages appear early
    # Normalize smart quotes to ASCII for matching
    sample = content[:2000].lower().replace("\u2019", "'").replace("\u2018", "'")
    return any(p in sample for p in _ERROR_PAGE_PATTERNS)


# ─── Fallback search ─────────────────────────────────────────────────────────


def _build_fallback_query(slug, suggested_angle=None):
    """Build a concise, entity-focused search query from suggested_angle or slug.
    
    Strategy: prioritize proper nouns (capitalized), numbers, then remaining
    significant words. Produces 4-6 token queries ideal for news search.
    """
    import re as _re
    if suggested_angle:
        # Remove punctuation but keep alphanumeric + spaces
        words = _re.sub(r"[^\w\s%]", " ", suggested_angle).split()
        stop = {"the", "a", "an", "and", "or", "of", "to", "in", "for", "with",
                "is", "are", "was", "were", "that", "this", "from", "into", "its",
                "has", "have", "had", "be", "been", "being", "do", "does", "did",
                "will", "would", "could", "should", "may", "might", "can",
                "while", "also", "just", "more", "less", "new", "says",
                "launches", "releases", "announces", "reveals", "shows",
                "finds", "turns", "drives", "signals", "triggers",
                "signaling", "turning", "enabling"}
        # Separate proper nouns (capitalized) and numbers
        proper = [w for w in words if w[0:1].isupper() and w.lower() not in stop and len(w) > 1]
        numbers = [w for w in words if any(c.isdigit() for c in w)]
        others = [w for w in words if w not in proper and w not in numbers
                  and w.lower() not in stop and len(w) > 2]
        # Build query: proper nouns first, then numbers, then other keywords
        tokens = []
        seen = set()
        for w in proper + numbers + others:
            if w.lower() not in seen:
                seen.add(w.lower())
                tokens.append(w)
            if len(tokens) >= 5:
                break
        if tokens:
            return " ".join(tokens)
    # Fallback: convert slug hyphens to spaces, take key terms
    return " ".join(slug.split("-")[:4])


def _fallback_search(candidate, existing_urls):
    """Search SearXNG for alternative URLs when all original sources failed."""
    if not SEARXNG_URL:
        return []
    slug = candidate.get("content_slug", candidate.get("matched_topic_slug", ""))
    angle = candidate.get("suggested_angle", "")
    query = _build_fallback_query(slug, angle)
    print("    🔎 Fallback search: %s" % query)

    try:
        encoded_q = urllib.request.quote(query)
        url = "%s/search?q=%s&format=json&categories=news&language=en&pageno=1" % (SEARXNG_URL, encoded_q)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        results = data.get("results", [])
        existing_set = set(existing_urls)
        new_urls = []
        for r in results:
            u = r.get("url", "")
            if u and u not in existing_set:
                new_urls.append(u)
            if len(new_urls) >= 3:
                break
        print("    🔎 Found %d new URLs" % len(new_urls))
        return new_urls
    except Exception as e:
        print("    ⚠️ Fallback search failed: %s" % e)
        return []

# ─── Crawling ────────────────────────────────────────────────────────────────


def crawl_url(url):
    """Crawl a URL via Crawl4AI, return (markdown, raw_html) or (None, None).

    raw_html is the first ~20KB of the page, used for date extraction.
    """
    if not CRAWL4AI_URL:
        return None, None
    try:
        payload = json.dumps({
            "urls": [url],
            "word_count_threshold": 100,
            "excluded_tags": ["nav", "footer", "header", "aside"],
            "page_timeout": PAGE_TIMEOUT_MS,
        }).encode()
        req = urllib.request.Request(
            "%s/crawl" % CRAWL4AI_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=CRAWL_TIMEOUT + 10) as resp:
            data = json.loads(resp.read())

        # Parse response (Crawl4AI has varying response formats)
        if isinstance(data, dict):
            result = data.get("results", data.get("result", data))
            if isinstance(result, list) and result:
                result = result[0]
        elif isinstance(data, list) and data:
            result = data[0]
        else:
            return None, None

        content = ""
        raw_html = ""
        if isinstance(result, dict):
            # Extract markdown
            md = result.get("markdown", result.get("extracted_content", result.get("text", "")))
            if isinstance(md, dict):
                content = md.get("raw_markdown", md.get("markdown_with_citations", ""))
            elif isinstance(md, str):
                content = md
            # Extract raw HTML if available (for date extraction)
            raw_html = result.get("html", result.get("raw_html", ""))
            if isinstance(raw_html, str):
                raw_html = raw_html[:20000]  # limit for date extraction
            else:
                raw_html = ""

        if content and len(content) >= 200:
            return content, raw_html
        return None, raw_html
    except Exception as e:
        print("    ⚠️ Crawl4AI failed: %s" % e)
        return None, None


def web_fetch_fallback(url):
    """Fallback: fetch page via direct HTTP request, return (text, html_head).

    Uses a simple urllib request with browser-like headers.
    Returns stripped text (not markdown) and raw HTML head for date extraction.
    """
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read(200000).decode("utf-8", errors="replace")

        html_head = raw[:20000]

        # Remove page template elements (same tags Crawl4AI excludes)
        for tag in ["nav", "header", "footer", "aside", "menu"]:
            text = re.sub(r"<%s[^>]*>.*?</%s>" % (tag, tag), "", raw,
                          flags=re.DOTALL | re.IGNORECASE)
            raw = text  # chain removals

        # Remove script and style
        text = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)

        # Strip remaining HTML tags and collapse whitespace
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) >= 300:
            return text[:MAX_CONTENT_LEN], html_head
        return None, html_head
    except Exception as e:
        print("    ⚠️ web_fetch fallback failed: %s" % e)
        return None, None


def fetch_html_head_only(url):
    """Fetch just the HTML head (first 20KB) for date extraction.

    Lightweight — only used when we already have markdown content but no date.
    """
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read(20000).decode("utf-8", errors="replace")
    except Exception:
        return ""


# ─── Content quality ─────────────────────────────────────────────────────────

# Boilerplate phrases that indicate nav/template content rather than article body
_BOILERPLATE_PHRASES = [
    "privacy policy", "terms of use", "cookie settings", "sign up",
    "newsletter", "about us", "contact us", "all rights reserved",
    "submit press release", "press release", "advertisement",
    "subscribe", "log in", "sign in", "follow us",
]


def content_quality_score(text):
    """Return a quality score 0-100. Low score = likely boilerplate.

    Checks:
    - Ratio of boilerplate phrases to total length
    - Average sentence length (very short = nav links)
    - Presence of article-like structure (paragraphs)
    """
    if not text or len(text) < 200:
        return 0

    text_lower = text.lower()
    total_len = len(text_lower)

    # Boilerplate phrase density
    bp_count = sum(1 for phrase in _BOILERPLATE_PHRASES if phrase in text_lower)
    bp_penalty = min(bp_count * 8, 40)  # max 40 points penalty

    # Check first 500 chars — if mostly short fragments, likely nav
    first_chunk = text[:500]
    words = first_chunk.split()
    if len(words) < 20:
        return max(0, 30 - bp_penalty)

    # Avg word count per "sentence" (split by . or newline)
    sentences = [s.strip() for s in re.split(r'[.\n]', text[:2000]) if len(s.strip()) > 10]
    if not sentences:
        return max(0, 30 - bp_penalty)

    avg_sentence_words = sum(len(s.split()) for s in sentences) / len(sentences)
    # Article sentences typically 8-30 words; nav fragments < 5
    if avg_sentence_words < 4:
        return max(0, 25 - bp_penalty)

    score = 70
    if avg_sentence_words >= 8:
        score += 15
    if len(sentences) >= 5:
        score += 15
    score -= bp_penalty

    return max(0, min(100, score))



def snippet_path_for_url(url):
    """Get snippet file path for a URL."""
    url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
    return SNIPPETS_DIR / ("%s.json" % url_hash)


# ─── Main ─────────────────────────────────────────────────────────────────────


def main():
    import argparse
    from urllib.parse import urlparse
    parser = argparse.ArgumentParser(description="Selective Crawl")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_dirs()
    print("📥 Selective Crawl")

    candidates = load_json(CANDIDATES_FILE, {})
    candidate_list = candidates.get("candidates", [])
    if not candidate_list:
        print("  ❌ No candidates in candidates.json")
        sys.exit(1)

    # Load domain stats
    domain_stats = load_json(DOMAIN_STATS_FILE, {})

    # Build cache of search API results (URL -> {full_content, publishedDate})
    # from latest search results, so crawl can skip already-fetched content
    _search_content_cache_local = {}
    latest_search = load_json(V9_DIR / "latest_search.json", {})
    for r in latest_search.get("results", []):
        fc = r.get("full_content", "")
        if fc and len(fc) >= MIN_CONTENT_LEN:
            _search_content_cache_local[r["url"]] = {
                "full_content": fc,
                "publishedDate": r.get("publishedDate"),
            }
    if _search_content_cache_local:
        print("  📦 %d URLs with search inline content" % len(_search_content_cache_local))
    global _search_content_cache
    _search_content_cache = _search_content_cache_local

    def get_domain(url):
        return urlparse(url).netloc.replace("www.", "")

    def domain_rate(domain):
        d = domain_stats.get(domain, {})
        total = d.get("ok", 0) + d.get("fail", 0)
        if total == 0:
            return 0.5
        return d["ok"] / total

    def update_domain(domain, ok):
        d = domain_stats.setdefault(domain, {"ok": 0, "fail": 0})
        d["ok" if ok else "fail"] += 1

    # Collect URLs per candidate, sorted by domain success rate
    candidate_urls = []
    for c in candidate_list:
        urls = []
        for url in c.get("source_urls", []):
            path = snippet_path_for_url(url)
            if path.exists():
                existing = load_json(path)
                if len(existing.get("content", "")) >= MIN_CONTENT_LEN:
                    continue
            urls.append(url)
        # Sort by composite key: tier rank first, then domain success rate
        urls.sort(key=lambda u: (_get_tier_rank(get_domain(u)), -domain_rate(get_domain(u))))
        slug = c.get("content_slug", c.get("matched_topic_slug", "?"))
        candidate_urls.append({"slug": slug, "urls": urls, "candidate": c})

    total_urls = sum(len(cu["urls"]) for cu in candidate_urls)
    print("  %d candidates, %d URLs to crawl" % (len(candidate_list), total_urls))

    if args.dry_run:
        for cu in candidate_urls:
            print("  [%s] %d URLs" % (cu["slug"], len(cu["urls"])))
            for u in cu["urls"]:
                d = get_domain(u)
                print("    %.0f%% %s — %s" % (domain_rate(d) * 100, d, u[:60]))
        return

    # Crawl each candidate's URLs
    success = 0
    failed = 0
    start = time.time()
    MIN_GOOD_SOURCES = 1

    for cu in candidate_urls:
        slug = cu["slug"]
        good_count = 0

        for url in cu["urls"]:
            domain = get_domain(url)
            rate = domain_rate(domain)
            path = snippet_path_for_url(url)

            # Skip low-rate domains if we already have enough good sources
            if good_count >= MIN_GOOD_SOURCES and rate < 0.3:
                print("  ⏭️  [%s] skip %s (rate %.0f%%, have %d sources)" % (
                    slug, domain, rate * 100, good_count))
                continue
            # Skip tier3 unreliable domains if we already have a good source
            if good_count >= MIN_GOOD_SOURCES and _get_tier_rank(domain) == 3:
                print("  ⏭️  [%s] skip tier3 %s (have %d sources)" % (
                    slug, domain, good_count))
                continue

            print("  🔗 [%s] %s" % (slug, url[:70]))

            # Check if search API already provided full_content for this URL
            content = None
            raw_html = None
            crawl_method = None
            pub_date_from_search = None

            # Look for pre-fetched content from search API results
            search_result = _search_content_cache.get(url)
            if search_result and len(search_result.get("full_content", "")) >= MIN_CONTENT_LEN:
                content = search_result["full_content"][:MAX_CONTENT_LEN]
                crawl_method = "search_inline"
                pub_date_from_search = search_result.get("publishedDate")
                q_score = content_quality_score(content)
                if q_score < 40 or is_error_page(content):
                    print("    ⚠️ Search inline content low quality (%d), will crawl" % q_score)
                    content = None
                    crawl_method = None
                else:
                    print("    📊 Search inline: %dc, quality %d/100" % (len(content), q_score))

            # Try search browse API
            if not content and grounding.is_available():
                print("    🔍 [search browse] %s" % url[:60])
                browse_result = grounding.browse_url(url, max_length=50000)
                if browse_result:
                    bc = browse_result.get("content", "")
                    if len(bc) >= MIN_CONTENT_LEN:
                        q_score = content_quality_score(bc)
                        if q_score >= 40 and not is_error_page(bc):
                            content = bc[:MAX_CONTENT_LEN]
                            crawl_method = "search_browse"
                            pub_date_from_search = browse_result.get("publishedDate") or pub_date_from_search
                            print("    📊 Search browse: %dc, quality %d/100" % (len(content), q_score))
                        else:
                            print("    ⚠️ Search browse low quality (%d)" % q_score)

            # Fallback: Try Crawl4AI
            if not content:
                content, raw_html = crawl_url(url)
                crawl_method = "crawl4ai"

            # Error page detection (before quality check)
            if content and is_error_page(content):
                print("    ⚠️ Error page detected, discarding Crawl4AI result")
                content = None

            # Quality check on Crawl4AI result
            if content:
                q_score = content_quality_score(content)
                if q_score < 40:
                    print("    ⚠️ Crawl4AI quality low (%d/100), trying web_fetch..." % q_score)
                    content = None
                else:
                    print("    📊 Quality: %d/100" % q_score)

            if not content:
                if crawl_method == "crawl4ai":
                    print("    ↩️ Crawl4AI failed, trying web_fetch fallback...")
                wf_content, wf_html = web_fetch_fallback(url)
                if wf_content:
                    wf_score = content_quality_score(wf_content)
                    print("    📊 web_fetch quality: %d/100" % wf_score)
                    if wf_score >= 40 and not is_error_page(wf_content):
                        content = wf_content
                        raw_html = wf_html or raw_html
                        crawl_method = "web_fetch"
                    else:
                        print("    ⚠️ web_fetch also low quality")
                        if not raw_html:
                            raw_html = wf_html or ""
                if not content:
                    if not raw_html:
                        raw_html = fetch_html_head_only(url) or ""
                    crawl_method = None

            if content:
                q_score = content_quality_score(content)
                snippet_data = {
                    "url": url,
                    "content": content[:MAX_CONTENT_LEN],
                    "raw_length": len(content),
                    "crawl_status": "ok",
                    "crawl_method": crawl_method,
                    "quality_score": q_score,
                    "crawled_at": datetime.now(timezone.utc).isoformat(),
                }
                html_for_date = raw_html or ""
                if not html_for_date:
                    html_for_date = fetch_html_head_only(url)
                pub_date = pub_date_from_search  # prefer search API date
                if not pub_date:
                    pub_date = extract_publish_date(html_for_date, url) if html_for_date else None
                if not pub_date:
                    pub_date = extract_publish_date(content[:3000], url)
                if pub_date:
                    snippet_data["publishedDate"] = pub_date
                    print("    📅 Date: %s" % pub_date)
                path.write_text(json.dumps(snippet_data, indent=2, ensure_ascii=False))
                print("    ✅ %dc via %s" % (len(content), crawl_method))
                success += 1
                good_count += 1
                update_domain(domain, True)
            else:
                snippet_data = {
                    "url": url,
                    "content": "",
                    "crawl_status": "failed",
                    "crawled_at": datetime.now(timezone.utc).isoformat(),
                }
                if raw_html:
                    pub_date = extract_publish_date(raw_html, url)
                    if pub_date:
                        snippet_data["publishedDate"] = pub_date
                        print("    📅 Date (from HTML head): %s" % pub_date)
                path.write_text(json.dumps(snippet_data, indent=2, ensure_ascii=False))
                print("    ❌ No content (date-only save)")
                failed += 1
                update_domain(domain, False)

            time.sleep(1)

        # Fallback search if all URLs failed for this candidate
        if good_count == 0:
            print("  🔄 [%s] All sources failed, trying fallback search..." % slug)
            source_urls = cu["candidate"].get("source_urls", [])
            fallback_urls = _fallback_search(cu["candidate"], source_urls)
            for url in fallback_urls:
                domain = get_domain(url)
                path = snippet_path_for_url(url)
                print("  🔗 [%s] (fallback) %s" % (slug, url[:70]))

                content, raw_html = crawl_url(url)
                crawl_method = "crawl4ai"
                if content and is_error_page(content):
                    print("    ⚠️ Error page detected")
                    content = None
                if content:
                    q_score = content_quality_score(content)
                    if q_score < 40:
                        content = None
                if not content:
                    wf_content, wf_html = web_fetch_fallback(url)
                    if wf_content and not is_error_page(wf_content):
                        wf_score = content_quality_score(wf_content)
                        if wf_score >= 40:
                            content = wf_content
                            raw_html = wf_html or raw_html
                            crawl_method = "web_fetch"

                if content:
                    q_score = content_quality_score(content)
                    snippet_data = {
                        "url": url,
                        "content": content[:MAX_CONTENT_LEN],
                        "raw_length": len(content),
                        "crawl_status": "ok",
                        "crawl_method": crawl_method,
                        "quality_score": q_score,
                        "crawled_at": datetime.now(timezone.utc).isoformat(),
                        "source": "fallback_search",
                    }
                    html_for_date = raw_html or fetch_html_head_only(url)
                    pub_date = extract_publish_date(html_for_date, url) if html_for_date else None
                    if not pub_date:
                        pub_date = extract_publish_date(content[:3000], url)
                    if pub_date:
                        snippet_data["publishedDate"] = pub_date
                    path.write_text(json.dumps(snippet_data, indent=2, ensure_ascii=False))
                    print("    ✅ (fallback) %dc via %s" % (len(content), crawl_method))
                    success += 1
                    good_count += 1
                    update_domain(domain, True)
                    # Also add to candidate's source_urls
                    if url not in source_urls:
                        source_urls.append(url)
                    break  # One good fallback source is enough
                else:
                    update_domain(domain, False)
                    failed += 1
                time.sleep(1)

    elapsed = time.time() - start
    print("\n✅ Crawl done in %.0fs — %d success, %d failed" % (elapsed, success, failed))

    # Save domain stats
    DOMAIN_STATS_FILE.write_text(json.dumps(domain_stats, indent=2, ensure_ascii=False))
    print("  Domain stats saved (%d domains)" % len(domain_stats))

    # Update candidates with crawl status
    for c in candidate_list:
        crawled_sources = []
        for url in c.get("source_urls", []):
            path = snippet_path_for_url(url)
            if path.exists():
                snippet = load_json(path)
                if snippet.get("crawl_status") == "ok" and len(snippet.get("content", "")) >= MIN_CONTENT_LEN:
                    crawled_sources.append(url)
        c["crawled_sources"] = crawled_sources
        c["has_content"] = len(crawled_sources) > 0

    candidates["crawled_at"] = datetime.now(timezone.utc).isoformat()
    CANDIDATES_FILE.write_text(json.dumps(candidates, indent=2, ensure_ascii=False))
    print("  Updated candidates.json with crawl status")

    # === Freshness gate ===
    print("\n📅 Freshness gate — checking source dates...")

    directives_data = load_json(DIRECTIVES_FILE, {})
    all_directives = directives_data.get("directives", []) + directives_data.get("tracked", [])
    directives_map = {d["slug"]: d for d in all_directives}

    # Search-result dates from topic files
    topics_dir = V9_DIR / "topics"
    search_dates = {}
    if topics_dir.exists():
        for tf in topics_dir.glob("*.json"):
            if tf.name == "index.json":
                continue
            topic_data = load_json(tf, {})
            for a in topic_data.get("articles", []):
                if a.get("publishedDate"):
                    search_dates[a["url"]] = a["publishedDate"]
    # Also check legacy topic_clusters.json
    clusters = load_json(V9_DIR / "topic_clusters.json", {})
    for slug, cluster in clusters.get("clusters", {}).items():
        for a in cluster.get("articles", []):
            if a.get("publishedDate") and a["url"] not in search_dates:
                search_dates[a["url"]] = a["publishedDate"]

    for c in candidate_list:
        slug = c.get("matched_topic_slug", "")
        directive = directives_map.get(slug, {})
        freshness_str = directive.get("freshness", "7d")
        max_days = FRESHNESS_DAYS.get(freshness_str, 7)
        cutoff = datetime.now(timezone.utc) - timedelta(days=max_days)

        source_dates = {}
        for url in c.get("source_urls", []):
            if url in search_dates:
                source_dates[url] = {"publishedDate": search_dates[url], "date_source": "search"}
            path = snippet_path_for_url(url)
            if path.exists():
                snippet = load_json(path)
                pd = snippet.get("publishedDate")
                if pd and url not in source_dates:
                    source_dates[url] = {"publishedDate": pd, "date_source": "crawl_extract"}

        c["source_dates"] = source_dates

        has_fresh = False
        for url, info in source_dates.items():
            try:
                from dateutil import parser as dateparser
                pub_dt = dateparser.parse(info["publishedDate"])
                if pub_dt.tzinfo is None:
                    pub_dt = pub_dt.replace(tzinfo=timezone.utc)
                if pub_dt >= cutoff:
                    has_fresh = True
                    break
            except Exception:
                pass

        c["has_fresh_source"] = has_fresh
        dated_count = len(source_dates)
        total_sources = len(c.get("source_urls", []))
        status = "✅" if has_fresh else "❌"
        print("  %s %s: %d/%d sources dated, fresh=%s (window=%dd)" % (
            status, slug, dated_count, total_sources, has_fresh, max_days))

    CANDIDATES_FILE.write_text(json.dumps(candidates, indent=2, ensure_ascii=False))

    rejected = [c for c in candidate_list if not c.get("has_fresh_source")]
    if rejected:
        print("\n  ⚠️  %d candidates lack fresh sources:" % len(rejected))
        for c in rejected:
            print("    - %s" % c.get("matched_topic_slug", "?"))


if __name__ == "__main__":
    main()
