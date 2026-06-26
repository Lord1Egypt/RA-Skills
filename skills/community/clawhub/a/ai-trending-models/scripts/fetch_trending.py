#!/usr/bin/env python3
"""
fetch_trending.py — AI Trending Open-Source Projects Collector
Covers: GitHub API, HuggingFace Hub, arXiv, Papers With Code, Hacker News
Output: trending_report.json (raw data for report generation)

Usage:
    python3 fetch_trending.py [--days 7] [--top 20] [--output trending_report.json]
"""

from __future__ import annotations

import json
import sys
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any


# ─── Config ───────────────────────────────────────────────────────────────────

AI_TOPICS = [
    "llm", "large-language-model", "generative-ai", "ai", "deep-learning",
    "transformer", "diffusion-model", "multimodal", "rag", "agent",
    "fine-tuning", "inference", "text-to-image", "text-to-video",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (AI-Trending-Collector/1.0)",
    "Accept": "application/json",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def fetch_json(url: str, retries: int = 3, timeout: int = 15) -> dict | list | None:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  ⚠️  Failed: {url} — {e}", file=sys.stderr)
    return None


def fetch_html(url: str, timeout: int = 15) -> str | None:
    try:
        req = urllib.request.Request(url, headers={**HEADERS, "Accept": "text/html"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode(errors="replace")
    except Exception as e:
        print(f"  ⚠️  Failed HTML fetch: {url} — {e}", file=sys.stderr)
    return None


# ─── Source 1: GitHub Search API ──────────────────────────────────────────────

def fetch_github_trending(days: int = 7, top: int = 30) -> list[dict]:
    """Query GitHub Search API for recently-starred AI repos."""
    since_date = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    results = []
    seen = set()

    for topic in AI_TOPICS[:6]:  # limit to avoid rate limits
        query = f"topic:{topic} pushed:>={since_date}"
        url = (
            "https://api.github.com/search/repositories"
            f"?q={urllib.parse.quote(query)}"
            "&sort=stars&order=desc&per_page=10"
        )
        data = fetch_json(url)
        if not data or "items" not in data:
            continue

        for item in data["items"]:
            repo_id = item.get("id")
            if repo_id in seen:
                continue
            seen.add(repo_id)

            results.append({
                "source": "github",
                "name": item.get("full_name", ""),
                "url": item.get("html_url", ""),
                "description": item.get("description") or "",
                "stars": item.get("stargazers_count", 0),
                "forks": item.get("forks_count", 0),
                "watchers": item.get("watchers_count", 0),
                "language": item.get("language") or "",
                "topics": item.get("topics", []),
                "license": (item.get("license") or {}).get("spdx_id", "Unknown"),
                "pushed_at": item.get("pushed_at", ""),
                "created_at": item.get("created_at", ""),
                "open_issues": item.get("open_issues_count", 0),
            })

        time.sleep(1)  # respect rate limit

    # Sort by stars descending, deduplicate, return top N
    results.sort(key=lambda x: x["stars"], reverse=True)
    unique = {r["name"]: r for r in results}
    return list(unique.values())[:top]


# ─── Source 2: HuggingFace Hub API ────────────────────────────────────────────

def fetch_huggingface_trending(limit: int = 20) -> list[dict]:
    """Fetch trending models from HuggingFace Hub."""
    url = f"https://huggingface.co/api/models?sort=trending&limit={limit}&full=false"
    data = fetch_json(url)
    if not data:
        return []

    results = []
    for item in data:
        results.append({
            "source": "huggingface",
            "name": item.get("id", ""),
            "url": f"https://huggingface.co/{item.get('id', '')}",
            "description": (item.get("cardData") or {}).get("summary", ""),
            "downloads": item.get("downloads", 0),
            "likes": item.get("likes", 0),
            "pipeline_tag": item.get("pipeline_tag", ""),
            "tags": item.get("tags", []),
            "license": item.get("license", "Unknown"),
            "created_at": item.get("createdAt", ""),
            "updated_at": item.get("lastModified", ""),
        })
    return results


def fetch_huggingface_spaces(limit: int = 10) -> list[dict]:
    """Fetch trending Spaces from HuggingFace."""
    url = f"https://huggingface.co/api/spaces?sort=trending&limit={limit}"
    data = fetch_json(url)
    if not data:
        return []

    results = []
    for item in data:
        results.append({
            "source": "huggingface_spaces",
            "name": item.get("id", ""),
            "url": f"https://huggingface.co/spaces/{item.get('id', '')}",
            "likes": item.get("likes", 0),
            "sdk": item.get("sdk", ""),
            "tags": item.get("tags", []),
        })
    return results


# ─── Source 3: arXiv Recent Papers ────────────────────────────────────────────

def fetch_arxiv_recent(categories: list[str] = None, max_results: int = 20) -> list[dict]:
    """Fetch recent arXiv papers via the official API."""
    if categories is None:
        categories = ["cs.AI", "cs.CL", "cs.CV", "cs.LG"]

    cat_query = " OR ".join(f"cat:{c}" for c in categories)
    # Also look for papers mentioning GitHub
    query = f"({cat_query}) AND (github OR open-source OR code)"

    url = (
        "http://export.arxiv.org/api/query"
        f"?search_query={urllib.parse.quote(query)}"
        f"&sortBy=submittedDate&sortOrder=descending"
        f"&max_results={max_results}"
    )

    html = fetch_html(url)
    if not html:
        return []

    results = []
    # Simple XML parsing without external deps
    import re
    entries = re.findall(r"<entry>(.*?)</entry>", html, re.DOTALL)

    for entry in entries:
        def extract(tag):
            m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", entry, re.DOTALL)
            return m.group(1).strip() if m else ""

        arxiv_id = extract("id").split("/abs/")[-1]
        title = re.sub(r"\s+", " ", extract("title"))
        summary = re.sub(r"\s+", " ", extract("summary"))[:300] + "..."
        published = extract("published")[:10]
        authors = re.findall(r"<name>(.*?)</name>", entry)

        # Extract GitHub link from summary if present
        github_link = ""
        gh_match = re.search(r"github\.com/[\w\-]+/[\w\-\.]+", entry)
        if gh_match:
            github_link = "https://" + gh_match.group(0)

        results.append({
            "source": "arxiv",
            "arxiv_id": arxiv_id,
            "title": title,
            "summary": summary,
            "published": published,
            "authors": authors[:3],
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "github_link": github_link,
        })

    return results


# ─── Source 4: Papers With Code (via simple scrape) ───────────────────────────

def fetch_papers_with_code(limit: int = 10) -> list[dict]:
    """Fetch trending papers from Papers With Code API."""
    url = f"https://paperswithcode.com/api/v1/papers/?ordering=-github_link_count&items_per_page={limit}"
    data = fetch_json(url)
    if not data or "results" not in data:
        return []

    results = []
    for item in data["results"]:
        results.append({
            "source": "paperswithcode",
            "title": item.get("title", ""),
            "url": f"https://paperswithcode.com/paper/{item.get('id', '')}",
            "arxiv_id": item.get("arxiv_id", ""),
            "github_link": item.get("official_code_url", ""),
            "stars": item.get("github_link_count", 0),
            "published": item.get("published", ""),
            "abstract": (item.get("abstract") or "")[:300],
        })
    return results


# ─── Source 5: Hacker News AI Stories ─────────────────────────────────────────

def fetch_hackernews_ai(limit: int = 10) -> list[dict]:
    """Fetch recent AI-related stories from HN Algolia API."""
    query = "LLM OR \"open source\" OR \"language model\" OR \"AI model\""
    since_ts = int((datetime.now(timezone.utc) - timedelta(days=7)).timestamp())
    url = (
        "https://hn.algolia.com/api/v1/search_by_date"
        f"?query={urllib.parse.quote(query)}"
        f"&tags=story"
        f"&numericFilters=created_at_i>{since_ts},points>50"
        f"&hitsPerPage={limit}"
    )
    data = fetch_json(url)
    if not data or "hits" not in data:
        return []

    results = []
    for hit in data["hits"]:
        results.append({
            "source": "hackernews",
            "title": hit.get("title", ""),
            "url": hit.get("url", ""),
            "hn_url": f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
            "points": hit.get("points", 0),
            "comments": hit.get("num_comments", 0),
            "created_at": hit.get("created_at", ""),
        })
    return results


# ─── Aggregator ───────────────────────────────────────────────────────────────

def build_report(days: int, top: int) -> dict:
    """Run all fetchers and combine into a unified report object."""
    now = datetime.now(timezone.utc)
    print("🔍 Fetching GitHub trending repos...", file=sys.stderr)
    github_repos = fetch_github_trending(days=days, top=top)

    print("🤗 Fetching HuggingFace trending models...", file=sys.stderr)
    hf_models = fetch_huggingface_trending(limit=20)

    print("🤗 Fetching HuggingFace trending spaces...", file=sys.stderr)
    hf_spaces = fetch_huggingface_spaces(limit=10)

    print("📄 Fetching arXiv recent papers...", file=sys.stderr)
    arxiv_papers = fetch_arxiv_recent(max_results=20)

    print("📊 Fetching Papers With Code...", file=sys.stderr)
    pwc_papers = fetch_papers_with_code(limit=10)

    print("📰 Fetching Hacker News AI stories...", file=sys.stderr)
    hn_stories = fetch_hackernews_ai(limit=10)

    report = {
        "generated_at": now.isoformat(),
        "period_days": days,
        "collection_date": now.strftime("%Y-%m-%d"),
        "summary": {
            "github_repos": len(github_repos),
            "hf_models": len(hf_models),
            "hf_spaces": len(hf_spaces),
            "arxiv_papers": len(arxiv_papers),
            "pwc_papers": len(pwc_papers),
            "hn_stories": len(hn_stories),
        },
        "github": github_repos,
        "huggingface_models": hf_models,
        "huggingface_spaces": hf_spaces,
        "arxiv": arxiv_papers,
        "papers_with_code": pwc_papers,
        "hackernews": hn_stories,
    }
    return report


# ─── Entry Point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch trending AI open-source projects")
    parser.add_argument("--days", type=int, default=7, help="Look-back window in days (default: 7)")
    parser.add_argument("--top", type=int, default=20, help="Max projects per source (default: 20)")
    parser.add_argument("--output", default="trending_report.json", help="Output JSON file path")
    args = parser.parse_args()

    print(f"\n🚀 AI Trending Models Collector — lookback: {args.days}d, top: {args.top}\n")

    report = build_report(days=args.days, top=args.top)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Report saved → {args.output}", file=sys.stderr)
    print(f"   GitHub repos   : {report['summary']['github_repos']}", file=sys.stderr)
    print(f"   HF models      : {report['summary']['hf_models']}", file=sys.stderr)
    print(f"   HF spaces      : {report['summary']['hf_spaces']}", file=sys.stderr)
    print(f"   arXiv papers   : {report['summary']['arxiv_papers']}", file=sys.stderr)
    print(f"   PapersWithCode : {report['summary']['pwc_papers']}", file=sys.stderr)
    print(f"   HN stories     : {report['summary']['hn_stories']}", file=sys.stderr)

    # Also print JSON to stdout so WorkBuddy can capture it directly
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
