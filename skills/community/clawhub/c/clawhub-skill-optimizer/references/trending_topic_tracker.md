# Trending Topic Tracker for ClawHub Skills
# 全网热点追踪：让技能蹭上热度红利

## Overview / 概述

Integrate real-time trending data to identify hot keywords that can boost your skill's visibility. Skills linked to trending topics get 5-10x more downloads.

## 1. Hot Topic APIs / 热点数据接口

### Free APIs (No Auth Required):

```python
import requests
import json
from datetime import datetime

# ── Weibo Hot Search ──────────────────────────────────────
def get_weibo_trending(limit=20):
    """Real-time Weibo hot search (no auth needed)."""
    url = "https://uapis.cn/api/hotboard"
    params = {"type": "weibo", "limit": limit}
    try:
        r = requests.get(url, params=params, timeout=8)
        data = r.json()
        results = []
        for i, item in enumerate(data.get("data", [])):
            results.append({
                "rank": i + 1,
                "title": item.get("title", ""),
                "hot_value": item.get("hot", ""),
                "url": item.get("url", "")
            })
        return results
    except Exception as e:
        return [{"error": str(e)}]

# ── Zhihu Hot ─────────────────────────────────────────────
def get_zhihu_trending(limit=20):
    """Zhihu hot questions (no auth needed)."""
    url = "https://uapis.cn/api/hotboard"
    params = {"type": "zhihu", "limit": limit}
    try:
        r = requests.get(url, params=params, timeout=8)
        data = r.json()
        return [
            {"rank": i+1, "title": item.get("title",""), "url": item.get("url","")}
            for i, item in enumerate(data.get("data", [])[:limit])
        ]
    except Exception as e:
        return [{"error": str(e)}]

# ── Bilibili Trending ──────────────────────────────────────
def get_bilibili_trending(limit=20):
    """Bilibili trending videos (no auth needed)."""
    url = "https://uapis.cn/api/hotboard"
    params = {"type": "bilibili", "limit": limit}
    try:
        r = requests.get(url, params=params, timeout=8)
        data = r.json()
        return [
            {"rank": i+1, "title": item.get("title",""), "hot": item.get("hot","")}
            for i, item in enumerate(data.get("data", [])[:limit])
        ]
    except Exception as e:
        return [{"error": str(e)}]

# ── GitHub Trending ────────────────────────────────────────
def get_github_trending(language="python", limit=10):
    """GitHub trending repos (public API, no auth)."""
    url = f"https://api.github.com/search/repositories"
    params = {
        "q": f"language:{language}+pushed:>2026-04-01",
        "sort": "stars", "order": "desc",
        "per_page": limit
    }
    headers = {"Accept": "application/vnd.github.v3+json"}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        items = r.json().get("items", [])
        return [
            {"name": itm["name"], "stars": itm["stargazers_count"],
             "desc": itm["description"], "url": itm["html_url"]}
            for itm in items
        ]
    except Exception as e:
        return [{"error": str(e)}]

# ── 36Kr / 创业邦 ─────────────────────────────────────────
def get_36kr_trending(limit=15):
    """36Kr startup/tech news (no auth)."""
    url = "https://uapis.cn/api/hotboard"
    params = {"type": "36kr", "limit": limit}
    try:
        r = requests.get(url, params=params, timeout=8)
        data = r.json()
        return [
            {"rank": i+1, "title": item.get("title",""), "url": item.get("url","")}
            for i, item in enumerate(data.get("data", [])[:limit])
        ]
    except Exception as e:
        return [{"error": str(e)}]
```

### Full Hot Board Aggregator (40+ platforms):

```python
def fetch_all_trending(platforms=None, limit=10):
    """Fetch trending from all platforms."""
    if platforms is None:
        platforms = ["weibo", "zhihu", "bilibili", "github"]

    fetcher_map = {
        "weibo": get_weibo_trending,
        "zhihu": get_zhihu_trending,
        "bilibili": get_bilibili_trending,
        "github": get_github_trending,
        "36kr": get_36kr_trending,
    }

    results = {}
    for platform in platforms:
        if platform in fetcher_map:
            try:
                results[platform] = fetcher_map[platform](limit)
            except Exception as e:
                results[platform] = [{"error": str(e)}]

    return results
```

## 2. Google Trends Integration / Google趋势集成

```python
from pytrends.request import TrendReq
import pandas as pd

def get_trending_queries(keyword: str, country="CN") -> dict:
    """
    Get related queries from Google Trends.
    Requires: pip install pytrends
    """
    try:
        pytrends = TrendReq(hl='zh-CN', tz=360)
        pytrends.build_payload(
            [keyword],
            cat=0,
            timeframe='today 3-m',   # Last 3 months
            geo=country
        )

        # Related queries
        related = pytrends.related_queries()
        top_queries = []
        rising_queries = []

        if keyword in related:
            top = related[keyword].get('top', [])
            rising = related[keyword].get('rising', [])
            top_queries = [q['query'] for q in top[:10]]
            rising_queries = [q['query'] for q in rising[:10]]

        # Interest over time
        interest = pytrends.interest_over_time()
        trend_data = interest[keyword].tail(30).to_dict() if not interest.empty else {}

        return {
            "keyword": keyword,
            "top_related_queries": top_queries,
            "rising_queries": rising_queries,  # Fastest growing
            "trend_direction": "📈 Rising" if trend_data and list(trend_data.values())[-1] > list(trend_data.values())[0] else "📉 Declining",
            "peak_interest_date": max(trend_data, key=trend_data.get) if trend_data else None,
        }
    except Exception as e:
        return {"error": str(e)}

# Example: Check "AI Agent" trend
# result = get_trending_queries("AI Agent", country="")
# print(result["rising_queries"])  # Fastest growing related searches
```

## 3. Trending-to-Skill Keyword Mapper / 热点→技能关键词映射

```python
# Domain-specific trending keyword mapping
SKILL_TRENDING_MAP = {
    "insurance-skills": {
        "trending": [
            "DeepSeek", "AI Agent", "LLM", "Claude",
            "Insurance Tech", "InsurTech", "Solvency",
            "C-ROSS", "Digital Insurance", "AI Claims"
        ],
        "action": "Add to tags + description"
    },
    "stock-skills": {
        "trending": [
            "DeepSeek", "AI Trading", "Quantitative", "Quant",
            "Technical Analysis", "A-Share", "US Stock",
            "Options Trading", "Crypto", "Macro"
        ],
        "action": "Add to title prefix"
    },
    "lottery-skills": {
        "trending": [
            "Data Science", "Statistics", "Machine Learning",
            "Probability", "Number Analysis", "Random"
        ],
        "action": "Frame as 'data analysis' not 'prediction'"
    },
    "productivity-skills": {
        "trending": [
            "AI Agent", "Workflow Automation", "No-Code",
            "Low-Code", "Automation", "Productivity",
            "Cursor", "Windsurf", "Devin"
        ],
        "action": "Tie to AI agent wave"
    }
}

def suggest_keywords_for_skill(skill_tags: list[str], skill_domain: str) -> list[dict]:
    """Suggest trending keywords to add based on skill domain."""
    mapping = SKILL_TRENDING_MAP.get(skill_domain, {})
    trending = mapping.get("trending", [])

    suggestions = []
    for kw in trending:
        if kw.lower() not in [t.lower() for t in skill_tags]:
            suggestions.append({
                "keyword": kw,
                "action": mapping.get("action", "Add to tags"),
                "priority": "HIGH" if len(suggestions) < 5 else "MEDIUM",
                "reason": f"Currently trending in {skill_domain}"
            })

    return suggestions[:10]
```

## 4. Weekly Trending Report Generator / 每周热点报告生成器

```python
from datetime import datetime

def generate_trending_report(skill_name: str, skill_tags: list[str],
                               skill_domain: str) -> str:
    """Generate a weekly trending report for a skill."""
    print(f"Fetching trending data...")
    trending = fetch_all_trending(limit=15)

    report = f"""
# 🔥 Weekly Trending Report
**Skill**: {skill_name}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Skill Domain**: {skill_domain}

---

## 📊 Trending Topics This Week

### Weibo Hot Search
"""
    for item in trending.get("weibo", [])[:10]:
        if "error" not in item:
            report += f"- #{item['rank']} {item['title']} (热度:{item['hot_value']})\n"

    report += "\n### GitHub Trending (Python)\n"
    for item in trending.get("github", [])[:5]:
        if "error" not in item:
            report += f"- **{item['name']}** ⭐{item['stars']}: {item['desc']}\n"

    # Keyword suggestions
    suggestions = suggest_keywords_for_skill(skill_tags, skill_domain)

    report += f"""
---

## 🎯 Keyword Suggestions for {skill_name}

| Keyword | Priority | Why |
|---------|----------|-----|
"""
    for s in suggestions[:8]:
        report += f"| {s['keyword']} | {s['priority']} | {s['reason']} |\n"

    report += """
---

## ✅ Action Items

1. Add HIGH priority keywords to skill description
2. Update tags with trending keywords
3. Consider title rewrite if major trend match found
4. Cross-post with trending hashtag
"""
    return report
```

## 5. Real-Time Alert System / 实时热点预警

```python
import schedule
import time
import threading

def trending_alert_worker(skill_name: str, skill_tags: list[str],
                          check_interval_hours=6):
    """
    Background worker that checks for trending keyword matches.
    Run in a separate thread.
    """
    previous_trending = set()

    while True:
        try:
            trending = fetch_all_trending(limit=50)
            current_trending = set()

            for platform, items in trending.items():
                for item in items:
                    title = item.get("title", "") or item.get("name", "")
                    current_trending.add(title.lower())

            # Find new trending topics
            new_topics = current_trending - previous_trending

            for topic in new_topics:
                for tag in skill_tags:
                    if tag.lower() in topic:
                        print(f"🚨 ALERT: '{tag}' trending! Topic: {topic}")

            previous_trending = current_trending

        except Exception as e:
            print(f"Error in trending check: {e}")

        time.sleep(check_interval_hours * 3600)

# To start: thread = threading.Thread(target=trending_alert_worker,
#                                     args=("Chanlun Analysis", ["chanlun","A-share"]))
# thread.start()
```

## 6. Quick Trending Check (No Code)

If you don't want to write code, use these tools directly:

| Tool | URL | What You Get |
|------|-----|-------------|
| **今日热榜** | tophub.today | 40+ platforms aggregated |
| **聚BT** | jubt.top | All-in-one trending |
| **Google Trends** | trends.google.com | Global search trends |
| **新榜** | newrank.cn | Weibo/WeChat/抖音 hot lists |
| **腾讯指数** | index.qq.com | WeChat ecosystem trends |
| **知乎热榜** | zhihu.com | Tech discussions |

### Manual Weekly Check Process:

```
Every Monday:
1. Open tophub.today → check all platforms in 5 min
2. Note top 5 AI/finance/business trending topics
3. Cross-reference with your skill tags
4. Update skill description with 1-2 trending keywords
5. Post on social media with trending hashtag
```
