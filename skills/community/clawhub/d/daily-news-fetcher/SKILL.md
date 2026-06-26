---
name: daily-news
description: Fetch and summarize daily news headlines from mainstream news sources. Use when user asks for news summary with phrases like "给我今天新闻摘要", "news", "今日新闻", "新闻摘要", "头条新闻", or any request for current news updates. Returns 5 top headlines with brief summaries in a structured format.
---

# Daily News

## Overview

This skill fetches the latest news from mainstream news sources and presents 5 top headlines with brief summaries in a clean, structured format.

## Usage

When user triggers this skill:

1. Run the `scripts/fetch_news.py` script to fetch and summarize news
2. Return the structured output to the user

**Trigger phrases:**
- "给我今天新闻摘要"
- "news"
- "今日新闻"
- "新闻摘要"
- "头条新闻"
- "最新新闻"

## Output Format

The script returns news in this structure:

```
📰 今日新闻摘要
━━━━━━━━━━━━━━━━━━━━

1️⃣ [标题]
   来源：BBC/新华网/等
   摘要：[一句话摘要]

2️⃣ [标题]
   来源：[来源]
   摘要：[摘要]

...
```

## News Sources

Primary sources (prioritized):
- BBC News (国际新闻)
- 新华网 (国内新闻)
- Reuters (财经/国际)

The script handles:
- Language detection and auto-translation if needed
- Deduplication of similar stories
- Relevance ranking for "hot" topics

## Scripts

### scripts/fetch_news.py

Main script that fetches and formats news. Run without arguments:

```bash
python3 scripts/fetch_news.py
```

Returns structured text output ready to send to user.
