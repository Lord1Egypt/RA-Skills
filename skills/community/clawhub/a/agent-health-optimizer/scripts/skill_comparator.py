#!/usr/bin/env python3
"""Skill Comparator — compare installed skills against ClawHub catalog.

Usage: python3 skill_comparator.py [workspace_path]

This tool is intentionally conservative: it suggests adjacent or overlapping
skills, not authoritative replacements.
"""

import sys, json, time, re
from pathlib import Path
from urllib.request import Request, urlopen

ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / ".openclaw" / "workspace"
API = "https://clawhub.ai/api/v1"

CATEGORIES = {
    "stock-analysis": {
        "keywords": {"stock", "equity", "portfolio tracker", "trading", "valuation", "ticker", "shares", "invest", "yfinance", "yahoo finance"},
        "exclude": {"crypto", "blockchain", "nft", "defi", "polymarket", "academic", "research paper", "literature"}
    },
    "ai-news": {
        "keywords": {"ai news", "ai 新闻", "llm news", "ai briefing", "ai daily", "大模型日报", "ai 动态"},
        "exclude": set()
    },
    "academic": {
        "keywords": {"academic", "research paper", "paper writer", "literature review", "citation", "scholarly", "论文", "ieee", "arxiv"},
        "exclude": {"stock", "market"}
    },
    "productivity": {
        "keywords": {"productivity", "focus", "todo", "task management", "time management", "pomodoro", "deep work", "energy management"},
        "exclude": {"stock", "ai news", "agent"}
    },
    "weather": {
        "keywords": {"weather", "forecast", "temperature", "天气"},
        "exclude": set()
    },
    "web-search": {
        "keywords": {"web search", "search engine", "brave search", "tavily", "multi search"},
        "exclude": {"ai news"}
    },
    "browser": {
        "keywords": {"browser automat", "headless browser", "puppeteer", "playwright", "selenium"},
        "exclude": set()
    },
    "social": {
        "keywords": {"social network", "moltbook", "twitter", "reddit", "community post"},
        "exclude": set()
    },
    "tts-stt": {
        "keywords": {"speech-to-text", "text-to-speech", "voice", "whisper", "tts", "transcri", "speech recogni"},
        "exclude": set()
    },
    "git-github": {
        "keywords": {"github", "git repo", "pull request", "gh cli", "git commit"},
        "exclude": set()
    },
    "image-video": {
        "keywords": {"image generat", "video generat", "photo edit", "image edit", "visual", "ffmpeg", "imagemagick"},
        "exclude": {"summarize"}
    },
    "calendar": {
        "keywords": {"calendar", "caldav", "ical", "google calendar"},
        "exclude": {"market", "stock", "news"}
    },
    "note-taking": {
        "keywords": {"obsidian", "notion", "knowledge base", "vault", "wiki", "note-taking"},
        "exclude": set()
    },
    "agent-meta": {
        "keywords": {"self-improving agent", "proactive agent", "agent architecture", "skill manager", "heartbeat", "agent memory"},
        "exclude": {"stock", "news", "weather", "calendar"}
    },
    "summarize": {
        "keywords": {"summarize", "summary", "tldr", "digest"},
        "exclude": {"stock", "news"}
    },
    "market-news": {
        "keywords": {"market news", "stock news", "financial news", "earnings report", "市场新闻", "stock digest"},
        "exclude": {"self-improving", "proactive", "agent memory", "correction", "error"}
    },
    "speed-network": {
        "keywords": {"speedtest", "bandwidth", "latency", "network speed", "internet speed"},
        "exclude": set()
    },
}


def fetch_json(url, timeout=10):
    req = Request(url)
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def fetch_skill_stats(slug):
    try:
        data = fetch_json(f"{API}/skills/{slug}", timeout=8)
        sk = data.get("skill", {})
        stats = sk.get("stats", {})
        return {
            "slug": slug,
            "name": sk.get("displayName", slug),
            "summary": sk.get("summary", ""),
            "stars": stats.get("stars", 0),
            "downloads": stats.get("downloads", 0),
            "installs": stats.get("installsCurrent", 0),
            "comments": stats.get("comments", 0),
        }
    except Exception:
        return None


def fetch_catalog(sort="stars", limit=50):
    try:
        data = fetch_json(f"{API}/skills?sort={sort}&limit={limit}", timeout=10)
        return [item["slug"] for item in data.get("items", [])]
    except Exception:
        return []


def categorize_skill(slug, summary):
    slug_lower = slug.lower()
    summary_lower = summary.lower()
    full_text = f"{slug_lower} {summary_lower}"
    matched = []
    for cat, spec in CATEGORIES.items():
        if any(ex in full_text for ex in spec["exclude"]):
            continue
        score = 0
        for kw in spec["keywords"]:
            if kw in slug_lower:
                score += 3
            elif kw in summary_lower:
                score += 1
        if score >= 1:
            matched.append((cat, score))
    matched.sort(key=lambda x: x[1], reverse=True)
    return [cat for cat, _ in matched[:2]]


def get_installed_skills():
    skills_dir = ws / "skills"
    if not skills_dir.exists():
        return {}
    installed = {}
    for d in skills_dir.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists():
            content = (d / "SKILL.md").read_text()
            desc_match = re.search(r'description:\s*["\']?(.+?)["\']?\s*\n', content)
            desc = desc_match.group(1) if desc_match else ""
            installed[d.name] = {"description": desc}
    return installed


def is_strong_overlap(a, b):
    cats_a = set(a.get("categories", []))
    cats_b = set(b.get("categories", []))
    shared = cats_a & cats_b
    if len(shared) >= 2:
        return True
    return len(shared) == 1 and len(cats_a) == 1 and len(cats_b) == 1


def main():
    print("\n📦 Skill Comparator — Checking installed skills against ClawHub")
    print("=" * 60)
    installed = get_installed_skills()
    if not installed:
        print("No skills installed.")
        return

    print(f"Found {len(installed)} installed skills. Fetching stats...\n")
    installed_stats = {}
    for slug in installed:
        stats = fetch_skill_stats(slug)
        if stats:
            stats["categories"] = categorize_skill(slug, stats.get("summary", ""))
            installed_stats[slug] = stats
        time.sleep(0.1)

    print("Fetching ClawHub catalog...")
    top_slugs = fetch_catalog("stars", 50)
    catalog_stats = {}
    for slug in top_slugs:
        if slug not in installed_stats:
            stats = fetch_skill_stats(slug)
            if stats:
                stats["categories"] = categorize_skill(slug, stats.get("summary", ""))
                catalog_stats[slug] = stats
            time.sleep(0.1)

    print(f"\n📊 Installed Skills ({len(installed_stats)} with ClawHub data):")
    print("-" * 60)
    sorted_installed = sorted(installed_stats.values(), key=lambda x: x["stars"], reverse=True)
    for s in sorted_installed:
        cats = ", ".join(s.get("categories", [])) or "uncategorized"
        print(f"  ⭐{s['stars']:>4} 📥{s['downloads']:>6} | {s['slug']} [{cats}]")

    print(f"\n🏆 Top ClawHub Skills NOT Installed:")
    print("-" * 60)
    missing_top = [(slug, catalog_stats[slug]) for slug in top_slugs if slug in catalog_stats and slug not in installed]
    for slug, stats in missing_top[:15]:
        cats = ", ".join(stats.get("categories", [])) or "general"
        print(f"  ⭐{stats['stars']:>4} 📥{stats['downloads']:>6} | {slug} [{cats}] — {stats['summary'][:50]}")

    print(f"\n🔎 Adjacent / Overlapping Skills (not authoritative replacements):")
    print("-" * 60)
    suggestions_found = False
    seen = set()
    adjacent = []

    for slug, info in installed_stats.items():
        candidates = []
        for other_slug, other in catalog_stats.items():
            if not is_strong_overlap(info, other):
                continue
            if other["stars"] < max(10, info["stars"]):
                continue
            key = (slug, other_slug)
            if key in seen:
                continue
            seen.add(key)
            candidates.append(other)
        candidates.sort(key=lambda x: x["stars"], reverse=True)
        if candidates:
            suggestions_found = True
            adjacent.append({
                "installed": slug,
                "installedStars": info["stars"],
                "categories": info.get("categories", []),
                "alternatives": candidates[:2],
            })
            print(f"\n  {slug} (⭐{info['stars']}) [{', '.join(info.get('categories', [])) or 'uncategorized'}] — adjacent options:")
            for c in candidates[:2]:
                print(f"    → {c['slug']} (⭐{c['stars']} 📥{c['downloads']}) [{', '.join(c.get('categories', [])) or 'general'}]")
                print(f"      {c['summary'][:80]}")

    if not suggestions_found:
        print("  ✅ No strong-overlap adjacent skills found.")

    print(f"\n📋 Category Coverage:")
    print("-" * 60)
    covered_cats = set()
    for info in installed_stats.values():
        covered_cats.update(info.get("categories", []))
    uncovered = set(CATEGORIES.keys()) - covered_cats
    if uncovered:
        print(f"  Covered: {', '.join(sorted(covered_cats))}")
        print(f"  Not covered: {', '.join(sorted(uncovered))}")
    else:
        print("  ✅ All categories covered!")

    report = {
        "installed": sorted_installed,
        "missing_top": [{"slug": s, **st} for s, st in missing_top[:15]],
        "adjacent_skills": [
            {
                "installed": item["installed"],
                "installedStars": item["installedStars"],
                "categories": item["categories"],
                "alternatives": item["alternatives"],
            }
            for item in adjacent
        ],
        "covered_categories": sorted(covered_cats),
        "uncovered_categories": sorted(uncovered) if uncovered else [],
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }
    report_path = ws / "memory" / "skill-comparator.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n📊 Report saved: {report_path}")


if __name__ == "__main__":
    main()
