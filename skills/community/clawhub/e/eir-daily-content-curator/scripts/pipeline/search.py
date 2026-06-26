#!/usr/bin/env python3
"""
Phase 1: Search - news-first, general-fallback.

For each directive topic:
  1. Search SearXNG news category → filter by publishedDate within freshness
  2. If news < 3 results, supplement with general category
  3. URL dedup, used-source exclusion
  4. Output: data/v9/raw_results/{run_id}.json

Usage:
  python3 -m pipeline.search                    # normal run
  python3 -m pipeline.search --topic ai-health  # single topic
  python3 -m pipeline.search --dry-run
"""

import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

from .config import (
    SEARXNG_URL, PUSHED_TITLES_FILE, USED_SOURCE_URLS_FILE,
    RAW_RESULTS_DIR, V9_DIR, FRESHNESS_DAYS, FRESHNESS_TO_TIME_RANGE,
    NEWS_MIN_RESULTS, MAX_RESULTS_PER_QUERY,
    ensure_dirs, load_json,
)
from .directives import load_directives
from . import grounding


# Directive loading functions moved to directives.py


# API directive fetching moved to eir_sync.py


# Directive loading moved to directives.py


def load_used_urls():
    """Load already-published source URLs (uses bloom filter for fast check)."""
    from .run_state import get_all_used_urls
    return get_all_used_urls()


def url_is_used(url):
    """Fast bloom filter check if URL is likely already used."""
    from .run_state import url_is_used as _url_is_used
    return _url_is_used(url)


def _detect_query_language(query):
    """Detect if query is primarily Chinese or English."""
    cjk_count = sum(1 for c in query if '\u4e00' <= c <= '\u9fff')
    return "zh" if cjk_count > len(query) * 0.2 else "en"


def _lang_to_region(lang):
    """Map detected language to region code for search API."""
    return "CN" if lang == "zh" else "US"


def grounding_search(query, category="news", limit=MAX_RESULTS_PER_QUERY):
    """Search via search API. Returns results in the same format as searxng_search.
    
    category: 'news' uses news endpoint, anything else uses web endpoint.
    """
    if not grounding.is_available():
        return []
    lang = _detect_query_language(query)
    region = _lang_to_region(lang)
    try:
        if category == "news":
            raw = grounding.search_news(query, max_results=min(limit, 10),
                                        language=lang, region=region, max_length=5000)
        else:
            raw = grounding.search_web(query, max_results=limit,
                                       language=lang, region=region,
                                       content_format="passage", max_length=3000)
        results = []
        for r in raw:
            results.append({
                "url": r.get("url", ""),
                "title": r.get("title", ""),
                "snippet": r.get("snippet") or r.get("content", "")[:300],
                "publishedDate": r.get("publishedDate"),
                "engines": [r.get("source_api", "search")],
                "score": 1.0,
                "category": category,
                "source_api": r.get("source_api", "search"),
                "full_content": r.get("content", ""),
                "thumbnail": r.get("thumbnail"),
                "source_name": r.get("source_name", ""),
            })
        return results
    except Exception as e:
        print("    ⚠️ Search API %s failed: %s" % (category, e))
        return []

def searxng_search(query, category="news", limit=MAX_RESULTS_PER_QUERY, time_range=None):
    """Search SearXNG and return results list.
    time_range: 'day', 'week', 'month', or None (all time).
    """
    if not SEARXNG_URL:
        return []
    lang = _detect_query_language(query)
    params_dict = {
        "q": query,
        "format": "json",
        "categories": category,
        "language": lang,
        "pageno": 1,
    }
    if time_range:
        params_dict["time_range"] = time_range
    params = urllib.parse.urlencode(params_dict)
    url = "%s/search?%s" % (SEARXNG_URL, params)
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        results = data.get("results", [])[:limit]
        return [
            {
                "url": r["url"],
                "title": r.get("title", ""),
                "snippet": r.get("content", ""),
                "publishedDate": r.get("publishedDate"),
                "engines": r.get("engines", []),
                "score": r.get("score", 0),
                "category": category,
            }
            for r in results if r.get("url")
        ]
    except Exception as e:
        print("    ⚠️ SearXNG %s search failed: %s" % (category, e), file=sys.stderr)
        return []


def filter_by_freshness(results, freshness_str):
    """Filter results by publishedDate within freshness window."""
    max_days = FRESHNESS_DAYS.get(freshness_str, 7)
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_days)
    filtered = []
    for r in results:
        pub = r.get("publishedDate")
        if not pub:
            # No date - mark as unknown, keep but deprioritize
            r["freshness_status"] = "unknown"
            filtered.append(r)
            continue
        try:
            from dateutil import parser as dateparser
            pub_dt = dateparser.parse(pub)
            if pub_dt.tzinfo is None:
                pub_dt = pub_dt.replace(tzinfo=timezone.utc)
            if pub_dt >= cutoff:
                r["freshness_status"] = "fresh"
                filtered.append(r)
            else:
                r["freshness_status"] = "stale"
                # Drop stale results
        except Exception:
            r["freshness_status"] = "unknown"
            filtered.append(r)
    return filtered


# Stop words for query building — common verbs, prepositions, articles
_QUERY_STOP_WORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "with",
    "is", "are", "was", "were", "that", "this", "from", "into", "its",
    "has", "have", "had", "be", "been", "being", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "can",
    "while", "also", "just", "more", "less", "new", "says", "about",
    "latest", "news", "update", "updates", "recent", "how", "what", "why",
    # Description-style verbs that aren't useful as search terms
    "tracks", "covers", "monitors", "follows", "explores", "discusses",
    "examines", "investigates", "analyzes", "reviews", "focuses",
    "including", "related", "general", "specific", "various",
}


def _inject_time_qualifier(query, freshness):
    """For short-freshness queries, replace broad year qualifiers with precise time words.
    
    '2026' → 'today' for 1d, 'this week' for 2-3d.
    If the query already has a time qualifier, leave it alone.
    """
    import re as _re
    lower = query.lower()
    # Already has a good time qualifier
    if any(t in lower for t in ['today', 'this week', 'yesterday', '今天', '今日', '本周', '昨天', 'latest', '最新']):
        return query
    # Map freshness to qualifier
    qualifier_map = {
        '1d': ('today', '今天'),
        '24h': ('today', '今天'),
        '2d': ('this week', '本周'),
        '3d': ('this week', '本周'),
    }
    en_qual, zh_qual = qualifier_map.get(freshness, ('', ''))
    if not en_qual:
        return query
    # Detect language
    is_zh = any('\u4e00' <= c <= '\u9fff' for c in query)
    qual = zh_qual if is_zh else en_qual
    # Replace year references ("2025", "2026") with time qualifier
    replaced = _re.sub(r'\b20[2-3]\d\b', qual, query)
    if replaced != query:
        return replaced
    # No year found, append qualifier
    return "%s %s" % (query, qual)


def _extract_key_terms(text, max_terms=5):
    """Extract key terms from text, prioritizing proper nouns and entities.

    Returns a concise list ideal for search queries.
    """
    import re as _re
    if not text:
        return []
    words = _re.sub(r"[^\w\s%]", " ", text).split()
    # Separate proper nouns (capitalized) and numbers
    proper = [w for w in words if w[0:1].isupper() and w.lower() not in _QUERY_STOP_WORDS and len(w) > 1]
    numbers = [w for w in words if any(c.isdigit() for c in w)]
    others = [w for w in words if w not in proper and w not in numbers
              and w.lower() not in _QUERY_STOP_WORDS and len(w) > 2]
    tokens = []
    seen = set()
    for w in proper + numbers + others:
        if w.lower() not in seen:
            seen.add(w.lower())
            tokens.append(w)
        if len(tokens) >= max_terms:
            break
    return tokens


def build_queries(directive):
    """Build search queries from a directive.

    Priority: searchHints (API) > entity-focused from description > topic name > keywords.
    Produces 2-4 queries per topic, each concise and entity-rich.
    For explore/seed tiers, adds event-oriented modifiers to find concrete stories.
    """
    queries = []
    # API returns searchHints as string[] (camelCase)
    hints = directive.get("searchHints") or directive.get("search_hints") or []
    if isinstance(hints, dict):
        suggested = hints.get("suggested_queries") or []
    else:
        suggested = hints  # already a list of query strings
    topic_name = directive.get("label") or directive.get("topic") or directive.get("slug") or ""
    if isinstance(topic_name, list):
        topic_name = topic_name[0] if topic_name else ""
    description = directive.get("description") or ""
    keywords = directive.get("keywords") or []
    freshness = directive.get("freshness", "7d")
    tier = directive.get("tier", "")

    seen_queries = set()
    def _add(q):
        q = q.strip()
        if q and q.lower() not in seen_queries:
            seen_queries.add(q.lower())
            queries.append({"q": q, "freshness": freshness})

    # For explore/seed: supplement hints with event-oriented queries
    # These modifiers turn generic topics into queries that find specific news
    is_seed = tier in ("explore", "seed")
    
    # 1. Use suggested queries from API (highest quality)
    #    For short freshness, inject time qualifiers to avoid stale results
    is_short_freshness = freshness in ("1d", "24h", "2d", "3d")
    for q in suggested:
        if is_short_freshness:
            q = _inject_time_qualifier(q, freshness)
        _add(q)

    # 2. Entity-focused query from description
    if description:
        terms = _extract_key_terms(description, max_terms=5)
        if terms:
            _add(" ".join(terms))

    # 3. Topic name query (combine with description terms, avoid duplication)
    if len(queries) < 3 and topic_name:
        has_zh = any('\u4e00' <= c <= '\u9fff' for c in topic_name)
        if has_zh:
            _add("%s 最新" % topic_name)
        else:
            # Add description terms that aren't already in topic name
            if description:
                topic_lower = topic_name.lower()
                desc_terms = [t for t in _extract_key_terms(description, max_terms=3)
                              if t.lower() not in topic_lower]
                if desc_terms:
                    _add("%s %s" % (topic_name, " ".join(desc_terms)))
                else:
                    _add(topic_name)
            else:
                _add(topic_name)

    # 4. Keywords query
    if len(queries) < 3 and keywords:
        kw = keywords[:4] if isinstance(keywords, list) else []
        if kw:
            # Filter out stop words from keywords too
            kw = [k for k in kw if k.lower() not in _QUERY_STOP_WORDS]
            if kw:
                _add(" ".join(kw))

    # 5. For short freshness topics without good time qualifiers, add a direct "today" query
    if is_short_freshness and topic_name and len(queries) < 5:
        has_zh = any('\u4e00' <= c <= '\u9fff' for c in topic_name)
        if has_zh:
            _add("%s 今天" % topic_name)
        else:
            _add("%s today" % topic_name)

    # 6. For seed/explore: enhance queries with specificity modifiers
    if is_seed and len(queries) < 5:
        # Add year to existing hint for time-anchoring ("ML advances" → "ML advances 2026")
        from datetime import datetime as _dt
        year = str(_dt.now().year)
        for hint in suggested[:1]:
            q_with_year = "%s %s" % (hint, year)
            _add(q_with_year)
        # Add event-oriented query in topic's primary language
        has_zh = any('\u4e00' <= c <= '\u9fff' for c in topic_name)
        if has_zh:
            _add("%s 突破 发布" % topic_name)
        else:
            _add("%s new launch announce %s" % (topic_name, year))

    return queries


def _post_filter(results):
    """Common post-processing: skip junk URLs, short titles, sort."""
    skip_patterns = [".pdf", ".zip", ".mp4", "youtube.com/watch", "twitter.com/", "x.com/"]
    results = [r for r in results if not any(p in r["url"].lower() for p in skip_patterns)]
    results = [r for r in results if len(r.get("title", "")) >= 10]

    def sort_key(r):
        fresh = 0 if r.get("freshness_status") == "fresh" else 1
        return (fresh, -r.get("score", 0))
    results.sort(key=sort_key)
    return results


def _extract_entities_from_titles(results, max_entities=5):
    """Extract specific entities from search result titles for refinement search.
    Focus on proper nouns that appear across multiple titles."""
    import re as _re
    from collections import Counter
    
    entity_counts = Counter()
    for r in results:
        title = r.get("title", "")
        # Multi-word proper noun phrases: "John Snow Labs", "Netflix AI"
        for m in _re.finditer(r'(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', title):
            entity_counts[m.group()] += 1
        # Single capitalized words not at sentence start (likely brand/org)
        words = title.split()
        for idx, w in enumerate(words):
            if (idx > 0 and w[0:1].isupper() and len(w) >= 3
                and w.lower() not in _QUERY_STOP_WORDS
                and w.isalpha()):
                entity_counts[w] += 1
        # Alphanumeric product names: "GPT-4", "A2UI", "Win11"
        for m in _re.finditer(r'[A-Z][A-Za-z]*[-]?\d[\w.]*', title):
            entity_counts[m.group()] += 1
        # CJK proper nouns (2-4 chars, skip generic)
        _skip_cjk = {
            '最新', '技术', '研究', '发展', '应用', '系统', '方法', '分析',
            '报告', '趋势', '未来', '全球', '行业', '领域', '设计',
            '平台', '模型', '数据', '产品', '服务', '开发', '管理',
            '发布', '更新', '内容', '用户', '市场', '企业', '关注',
            '智能', '学习', '网络', '人工', '语言', '处理', '中国',
        }
        for m in _re.finditer(r'[\u4e00-\u9fff]{2,4}', title):
            w = m.group()
            if w not in _skip_cjk:
                entity_counts[w] += 1
    
    # Keep entities appearing 2+ times (cross-title confirmation)
    # Exception: versioned product names (GPT-5.5, Claude-4) are high-signal
    # even at count=1 — they indicate specific product launches/updates
    import re as _re2
    _versioned_product = _re2.compile(r'^[A-Z][A-Za-z]*[-]?\d[\w.]*$')
    entities = []
    for e, c in entity_counts.most_common(max_entities * 2):
        if c >= 2:
            entities.append(e)
        elif _versioned_product.match(e) and c >= 1:
            entities.append(e)  # versioned product name, keep at count=1
        if len(entities) >= max_entities:
            break
    return entities


def _entity_refinement_pass(initial_results, slug, topic_name, freshness,
                            time_range, seen_urls, used_urls):
    """2-pass refinement: extract entities from initial results, search again
    with entity-specific queries for better, more concrete results."""
    entities = _extract_entities_from_titles(initial_results)
    if not entities:
        return []
    
    print("    🔬 Refinement pass: extracted entities: %s" % ", ".join(entities[:5]))
    
    refined = []
    use_grounding = grounding.is_available()
    
    # Build 2-3 targeted queries from entities
    queries = []
    for entity in entities[:3]:
        queries.append(entity if len(entity) > 6 else "%s %s" % (entity, topic_name))
    
    for q in queries:
        results = []
        if use_grounding:
            results = grounding_search(q, category="news", limit=5)
        if not results:
            results = searxng_search(q, category="news", time_range=time_range)
        results = filter_by_freshness(results, freshness)
        for r in results:
            if r["url"] not in seen_urls and r["url"] not in used_urls:
                r["topic_slug"] = slug
                r["topic_name"] = topic_name
                r["search_query"] = q
                refined.append(r)
                seen_urls.add(r["url"])
        time.sleep(0.3)
    
    if refined:
        print("    🔬 Refinement: +%d results from entity queries" % len(refined))
    return refined


def _cross_topic_entity_search(all_results, directives, used_urls):
    """After all topics searched, extract hot entities across ALL results
    and do supplementary news searches for entities that span multiple topics.
    
    This catches breaking news (e.g. GPT-5.5 launch) that searchHints missed.
    """
    import re as _re
    from collections import Counter, defaultdict
    
    if not all_results:
        return []
    
    # Extract entities and track which topics they appear in
    entity_topics = defaultdict(set)  # entity -> set of topic_slugs
    entity_counts = Counter()
    
    for r in all_results:
        title = r.get("title", "")
        slug = r.get("topic_slug", "unknown")
        # Product names with version: GPT-4, Claude-3.5, Gemini-2.0
        for m in _re.finditer(r'[A-Z][A-Za-z]*[-]?\d[\w.]*', title):
            e = m.group()
            entity_topics[e].add(slug)
            entity_counts[e] += 1
        # Multi-word proper nouns
        for m in _re.finditer(r'(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', title):
            e = m.group()
            if e.lower() not in _QUERY_STOP_WORDS and len(e) > 5:
                entity_topics[e].add(slug)
                entity_counts[e] += 1
    
    # Find entities that appear across 2+ topics (signal of hot event)
    # OR appear 3+ times in any context (high frequency = breaking news)
    hot_entities = []
    for entity, topics in entity_topics.items():
        count = entity_counts[entity]
        if len(topics) >= 2 or count >= 3:
            hot_entities.append((entity, len(topics), count))
    
    if not hot_entities:
        return []
    
    # Sort by cross-topic breadth, then frequency
    hot_entities.sort(key=lambda x: (-x[1], -x[2]))
    
    # Only search top 3 entities to avoid API abuse
    hot_entities = hot_entities[:3]
    print("\n🔥 Cross-topic hot entities: %s" % 
          ", ".join("%s (%dt/%dc)" % (e, t, c) for e, t, c in hot_entities))
    
    # Search each hot entity
    seen_urls = {r["url"] for r in all_results}
    supplementary = []
    use_grounding = grounding.is_available()
    
    # Find the most relevant directive for each entity
    directive_map = {d["slug"]: d for d in directives}
    
    for entity, n_topics, n_count in hot_entities:
        # Find which topic this entity is most associated with
        topics_for_entity = entity_topics[entity]
        # Pick the topic with shortest freshness (most time-sensitive)
        best_topic = None
        best_freshness_days = 999
        for t in topics_for_entity:
            d = directive_map.get(t, {})
            fd = FRESHNESS_DAYS.get(d.get("freshness", "7d"), 7)
            if fd < best_freshness_days:
                best_freshness_days = fd
                best_topic = t
        
        topic_directive = directive_map.get(best_topic, {})
        freshness = topic_directive.get("freshness", "7d")
        time_range = FRESHNESS_TO_TIME_RANGE.get(freshness)
        topic_name = topic_directive.get("label", best_topic or "unknown")
        
        q = "%s news" % entity if len(entity) < 8 else entity
        print("    🔥 [cross-topic news] %s (for %s)" % (q, best_topic))
        
        results = []
        if use_grounding:
            results = grounding_search(q, category="news", limit=5)
        if not results:
            results = searxng_search(q, category="news", time_range=time_range)
        results = filter_by_freshness(results, freshness)
        
        for r in results:
            if r["url"] not in seen_urls and r["url"] not in used_urls:
                r["topic_slug"] = best_topic or "cross-topic"
                r["topic_name"] = topic_name
                r["search_query"] = q
                r["cross_topic_entity"] = entity
                supplementary.append(r)
                seen_urls.add(r["url"])
        time.sleep(0.3)
    
    if supplementary:
        print("    🔥 Cross-topic: +%d supplementary results" % len(supplementary))
    return supplementary


def search_topic(directive, used_urls):
    """Search for a single topic: search API first, SearXNG fallback."""
    slug = directive["slug"]
    topic_name = directive.get("label") or directive.get("topic", slug)
    freshness = directive.get("freshness", "7d")
    queries = build_queries(directive)

    if not queries:
        print("  ⏭️  %s: no queries" % slug)
        return []

    all_results = []
    seen_urls = set()

    # Determine SearXNG time_range from freshness
    time_range = FRESHNESS_TO_TIME_RANGE.get(freshness)
    use_grounding = grounding.is_available()

    # Step 1: News search (all queries) — search API first, SearXNG fallback
    news_results = []
    for qinfo in queries:
        q = qinfo["q"]
        results = []
        if use_grounding:
            print("    🔍 [search news] %s" % q[:60])
            results = grounding_search(q, category="news", limit=MAX_RESULTS_PER_QUERY)
            if not results:
                print("    ↩️ Search API returned 0, trying web...")
                results = grounding_search(q, category="general", limit=MAX_RESULTS_PER_QUERY)
        if not results:
            print("    🔍 [searxng news] %s" % q[:60])
            results = searxng_search(q, category="news", time_range=time_range)
        results = filter_by_freshness(results, freshness)
        for r in results:
            if r["url"] not in seen_urls and r["url"] not in used_urls:
                r["topic_slug"] = slug
                r["topic_name"] = topic_name
                r["search_query"] = q
                news_results.append(r)
                seen_urls.add(r["url"])
        time.sleep(0.3)

    # Keep fresh results; when time_range is set, also keep unknown-date results
    # but cap undated results to avoid noise dominating
    fresh_results = [r for r in news_results if r.get("freshness_status") == "fresh"]
    unknown_results = [r for r in news_results if r.get("freshness_status") == "unknown"]
    if time_range:
        max_unknown = max(len(fresh_results), 2)
        usable_news = fresh_results + unknown_results[:max_unknown]
    else:
        usable_news = fresh_results
    fresh_count = len(fresh_results)
    unknown_kept = len(usable_news) - fresh_count
    print("    📰 News: %d results (%d fresh, %d unknown kept/%d total, %d usable)" % (
        len(news_results), fresh_count, unknown_kept, len(unknown_results), len(usable_news)))
    all_results.extend(usable_news)

    # Step 2: General fallback if usable < threshold
    if len(usable_news) < NEWS_MIN_RESULTS:
        print("    📎 News insufficient (%d < %d), trying general..." % (len(usable_news), NEWS_MIN_RESULTS))
        for qinfo in queries[:2]:
            q = qinfo["q"]
            results = []
            if use_grounding:
                print("    🔍 [search web] %s" % q[:60])
                results = grounding_search(q, category="general", limit=MAX_RESULTS_PER_QUERY)
            if not results:
                print("    🔍 [searxng general] %s" % q[:60])
                results = searxng_search(q, category="general", time_range=time_range)
            results = filter_by_freshness(results, freshness)
            for r in results:
                if r["url"] not in seen_urls and r["url"] not in used_urls:
                    r["topic_slug"] = slug
                    r["topic_name"] = topic_name
                    r["search_query"] = q
                    all_results.append(r)
                    seen_urls.add(r["url"])
            time.sleep(0.3)

    # Post-filter
    all_results = _post_filter(all_results)

    # Step 3: Entity refinement for ALL tiers (not just explore/seed)
    # Short freshness topics especially benefit from entity-driven 2nd pass
    tier = directive.get("tier", "")
    refinement_threshold = 5 if freshness in ("1d", "24h", "2d", "3d") else 8
    if len(all_results) < refinement_threshold and all_results:
        refined = _entity_refinement_pass(all_results, slug, topic_name,
                                          freshness, time_range, seen_urls, used_urls)
        if refined:
            all_results.extend(refined)
            all_results = _post_filter(all_results)

    print("    ✅ %s: %d results after filtering" % (slug, len(all_results)))
    return all_results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Search")
    parser.add_argument("--topic", type=str, help="Only search this topic slug")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_dirs()

    # Preflight
    from .config import preflight_check
    errors = preflight_check()
    if errors:
        for e in errors:
            print("❌ %s" % e, file=sys.stderr)
        sys.exit(1)

    start = time.time()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    print("🔍 Search starting (run=%s)" % run_id)

    # Load directives
    data = load_directives()
    all_directives = data.get("directives", []) + data.get("tracked", [])
    print("  %d directives loaded" % len(all_directives))

    # Filter by topic if specified
    if args.topic:
        all_directives = [d for d in all_directives if d["slug"] == args.topic]
        if not all_directives:
            print("  ❌ Topic '%s' not found" % args.topic)
            sys.exit(1)

    # Load used URLs
    used_urls = load_used_urls()
    print("  %d used source URLs excluded" % len(used_urls))

    # Search each topic
    all_results = []
    for directive in all_directives:
        slug = directive["slug"]
        print("\n📌 %s [%s, freshness=%s]" % (
            directive.get("label") or directive.get("topic", slug),
            directive.get("tier") or directive.get("type", "?"),
            directive.get("freshness", "7d"),
        ))

        if args.dry_run:
            queries = build_queries(directive)
            for q in queries:
                print("    [dry-run] Would search: %s" % q["q"][:60])
            continue

        results = search_topic(directive, used_urls)
        all_results.extend(results)

    if args.dry_run:
        print("\n[dry-run] Done.")
        return

    # Cross-topic entity aggregation: find hot entities across ALL results
    # and do supplementary searches for entities that appear in many topics
    cross_topic_results = _cross_topic_entity_search(
        all_results, all_directives, used_urls
    )
    if cross_topic_results:
        all_results.extend(cross_topic_results)

    # Save raw results
    output = {
        "run_id": run_id,
        "searched_at": datetime.now(timezone.utc).isoformat(),
        "topic_count": len(all_directives),
        "total_results": len(all_results),
        "results": all_results,
    }
    output_path = RAW_RESULTS_DIR / ("%s.json" % run_id)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    # Also write latest symlink
    latest_path = V9_DIR / "latest_search.json"
    latest_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    elapsed = time.time() - start
    print("\n✅ Search done in %.0fs - %d results saved to %s" % (
        elapsed, len(all_results), output_path.name))

    # Summary by topic
    by_topic = {}
    for r in all_results:
        s = r.get("topic_slug", "?")
        by_topic[s] = by_topic.get(s, 0) + 1
    for s, n in sorted(by_topic.items()):
        print("  %s: %d results" % (s, n))


if __name__ == "__main__":
    main()
