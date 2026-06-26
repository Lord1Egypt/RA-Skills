#!/usr/bin/env python3
"""
Phase 2: Candidate Selection — prepare per-topic data for agent judgment.

Reads latest_search.json, groups by topic, writes per-topic JSON files
that the agent reads to decide candidates (0-3 per topic).

Also manages domain crawl success rate statistics.

Output:
  data/v9/topics/  — per-topic JSON files for agent judgment
  data/domain_stats.json — domain-level crawl success rates

Usage:
  python3 -m pipeline.candidate_selector
  python3 -m pipeline.candidate_selector --dry-run
"""

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse

from .config import (
    V9_DIR, CANDIDATES_FILE, DIRECTIVES_FILE, FRESHNESS_DAYS, DATA_DIR,
    ensure_dirs, load_json,
)

TOPICS_DIR = V9_DIR / "topics"
DOMAIN_STATS_FILE = DATA_DIR / "domain_stats.json"


# ─── Domain stats ────────────────────────────────────────────────────────────


def load_domain_stats():
    """Load domain crawl success rate stats."""
    return load_json(DOMAIN_STATS_FILE, {})


def save_domain_stats(stats):
    DOMAIN_STATS_FILE.write_text(json.dumps(stats, indent=2, ensure_ascii=False))


def get_domain(url):
    return urlparse(url).netloc.replace("www.", "")


def domain_success_rate(stats, domain):
    """Return success rate for a domain (0.0-1.0). Unknown domains = 0.5."""
    d = stats.get(domain, {})
    total = d.get("ok", 0) + d.get("fail", 0)
    if total == 0:
        return 0.5  # unknown domain gets neutral score
    return d["ok"] / total


def rank_urls_by_domain(urls, domain_stats):
    """Sort URLs by domain success rate (highest first), preserving order within same rate."""
    def sort_key(url):
        domain = get_domain(url)
        rate = domain_success_rate(domain_stats, domain)
        return -rate  # negative for descending
    return sorted(urls, key=sort_key)


# ─── Search results loading ─────────────────────────────────────────────────


def load_search_results():
    """Load latest search results."""
    path = V9_DIR / "latest_search.json"
    data = load_json(path)
    if not data.get("results"):
        print("❌ No search results found in latest_search.json")
        sys.exit(1)
    return data


def group_by_topic(results):
    """Group results by their directive topic_slug."""
    by_topic = {}
    for r in results:
        slug = r.get("topic_slug", "unknown")
        by_topic.setdefault(slug, []).append(r)
    return by_topic


# ─── Per-topic file generation ───────────────────────────────────────────────


def build_topic_file(slug, articles, directive, domain_stats):
    """Build a per-topic JSON file with all articles and metadata."""
    topic_name = directive.get("label") or directive.get("topic", slug)
    tier = directive.get("tier") or directive.get("type", "unknown")
    freshness = directive.get("freshness", "7d")

    # Enrich articles with domain info
    enriched = []
    for a in articles[:12]:  # cap at 12 per topic
        domain = get_domain(a.get("url", ""))
        rate = domain_success_rate(domain_stats, domain)
        enriched.append({
            "url": a["url"],
            "title": a.get("title", ""),
            "snippet": (a.get("snippet") or "")[:200],
            "publishedDate": a.get("publishedDate"),
            "domain": domain,
            "domain_crawl_rate": round(rate, 2),
        })

    return {
        "slug": slug,
        "topic_name": topic_name,
        "tier": tier,
        "freshness": freshness,
        "article_count": len(articles),
        "articles": enriched,
    }


# ─── Main ────────────────────────────────────────────────────────────────────


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Candidate Selection — Prepare topics")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_dirs()
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    print("📋 Candidate Selection — Topic Preparation")

    # Load search results
    search_data = load_search_results()
    results = search_data["results"]
    print("  %d search results from run %s" % (len(results), search_data.get("run_id", "?")))

    # Load directives
    directives_data = load_json(DIRECTIVES_FILE, {})
    all_directives = directives_data.get("directives", []) + directives_data.get("tracked", [])
    directives_map = {d["slug"]: d for d in all_directives}

    # Load domain stats
    domain_stats = load_domain_stats()
    print("  %d domains tracked" % len(domain_stats))

    # Group by topic
    topic_groups = group_by_topic(results)
    print("  %d topic groups:" % len(topic_groups))

    if args.dry_run:
        for slug, arts in sorted(topic_groups.items()):
            print("    %s: %d articles" % (slug, len(arts)))
        return

    # Write per-topic files
    topic_summary = []
    for slug, articles in sorted(topic_groups.items()):
        directive = directives_map.get(slug, {})
        topic_data = build_topic_file(slug, articles, directive, domain_stats)

        # Write topic file
        topic_path = TOPICS_DIR / ("%s.json" % slug)
        topic_path.write_text(json.dumps(topic_data, indent=2, ensure_ascii=False))

        fresh_count = sum(1 for a in topic_data["articles"] if a.get("publishedDate"))
        topic_summary.append({
            "slug": slug,
            "topic_name": topic_data["topic_name"],
            "tier": topic_data["tier"],
            "freshness": topic_data["freshness"],
            "article_count": topic_data["article_count"],
            "fresh_articles": fresh_count,
        })
        print("    %s: %d articles (%d with dates) → %s" % (
            slug, len(articles), fresh_count, topic_path.name))

    # Write summary index
    index = {
        "prepared_at": datetime.now(timezone.utc).isoformat(),
        "run_id": search_data.get("run_id", ""),
        "topics": topic_summary,
    }
    index_path = TOPICS_DIR / "index.json"
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False))

    print("\n📝 %d topic files written to %s" % (len(topic_summary), TOPICS_DIR))
    print("   Agent should read each topic file and decide candidates (0-3 per topic)")


if __name__ == "__main__":
    main()
