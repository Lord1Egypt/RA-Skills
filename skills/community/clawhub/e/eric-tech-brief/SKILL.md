---
name: tech-news-daily
description: "Fetch, summarize and curate the latest tech news from major sources (Hacker News, TechCrunch, The Verge, Ars Technica, GitHub Trending). Use when the user wants: (1) Daily tech news briefing, (2) Trending topics in AI/developer/news, (3) GitHub trending repos today, (4) Custom tech news digest on specific topics, (5) Save articles to read later."
version: 1.0.0
homepage: https://clawhub.ai
metadata:
  openclaw:
    emoji: "📰"
    requires:
      bins:
        - curl
---

# Tech News Daily

Get a curated daily briefing of the most important tech news, tailored to your interests.

## When to Use

✅ **USE this skill when:**

- "What's happening in tech today?"
- "Show me today's top tech news"
- "Any big AI news this week?"
- "What's trending on GitHub?"
- "Give me a morning tech briefing"
- "Find news about [specific topic/company]"

❌ **DON'T use this skill when:**

- Need financial/stock market news → use a finance skill
- Need weather or local news → use a weather skill
- Real-time sports scores → use a sports API

## How It Works

The skill fetches from multiple free/public RSS feeds and APIs, then summarizes the results.

### News Sources (Free Tier)

| Source | Type | Access |
|--------|------|--------|
| Hacker News | Text API | `https://hacker-news.firebaseio.com/v0/` |
| GitHub Trending | Web scrape | `https://github.com/trending` |
| TechCrunch RSS | RSS Feed | `https://techcrunch.com/feed/` |
| The Verge RSS | RSS Feed | `https://www.theverge.com/rss/index.xml` |

### Commands / Natural Language Triggers

| What you say | What happens |
|---|---|
| "daily briefing" | Top 5 stories from Hacker News + TechCrunch |
| "trending on GitHub" | Top 10 GitHub repos today (by language filter) |
| "AI news this week" | Filter articles matching AI/ML keywords |
| "tech news about [topic]" | Search + summarize across sources |
| "save that article" | Bookmark to `scripts/bookmarks.json` |

## Workflow

### 1. Fetch News

When the user asks for news, the agent:

1. Checks which sources to use (default: HN + GitHub Trending)
2. Fetches the latest items using `curl`
3. Deduplicates and ranks by relevance/recent
4. Summarizes each item in 2-3 sentences

### 2. Filter by Interest

The agent can filter by:
- Topic: "AI", "cybersecurity", "open source", "startups", etc.
- Source: "HN only", "GitHub trending Python"
- Time: "today", "this week", "past 24h"

### 3. Bookmark for Later

When the user says "save that", the agent appends to `scripts/bookmarks.json` with:
- Title, URL, source, date saved
- Optional user note/tag

### 4. Generate Digest

The agent can compile a markdown summary suitable for:
- Telegram/Signal message
- Email digest
- Local markdown file

## Folder Structure

```
tech-news-daily/
├── SKILL.md
└── scripts/
    └── bookmarks.json       (created on first use)
```

## Examples

> **User**: "Give me my morning tech briefing"
> **Agent**: *Fetches HN top stories + GitHub trending, presents top 5*
>
> **User**: "Any interesting AI news today?"
> **Agent**: *Filters & summarizes AI-related articles across sources*
>
> **User**: "Show me Python trending repos"
> **Agent**: *Fetches https://github.com/trending/python?since=daily, lists top 5*

## Notes

- All sources are free/public — no API keys needed
- For RSS-based sources, the agent uses `curl` + basic XML parsing
- Respect rate limits: cache results for at least 10 minutes between fetches
