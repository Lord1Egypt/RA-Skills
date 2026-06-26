---
name: douyin-quick-search
description: >
  Search Douyin (抖音) content by natural language keyword. Supports video search,
  trending topics, and video detail extraction. Uses web search + page scraping
  (no API key required).
version: 1.0.0
---

# Douyin Scraper

> **Search Douyin videos by natural language — "搜索一下海鲜视频" just works.**

## What This Skill Does

Search and retrieve Douyin (抖音) video content using natural language queries:

- **Keyword search**: Find videos by any Chinese or English keyword phrase
- **Trending discovery**: Find what's hot on Douyin
- **Video detail**: Extract metadata from a specific Douyin video URL

## How It Works

This skill uses two layers:

1. **Web search** (Brave) → discovers Douyin search result pages and video URLs
2. **Web fetch** → extracts readable content from Douyin pages when accessible

No API keys, cookies, or login required.

---

## Activation Rules (for AI agents)

### Use this skill when the user asks about:
- Searching Douyin videos by keyword (搜索抖音/搜一下/找一下)
- Finding trending Douyin content (抖音热搜/抖音热门)
- Getting info about a specific Douyin video URL
- Any request containing "抖音" + a search intent

### Do NOT use this skill when:
- User wants to download videos (use a downloader skill instead)
- User wants to publish/upload to Douyin
- User asks about Douyin script optimization (that's the `douyin` skill)
- User asks about Douyin account/analytics management

---

## Execution Protocol

### Search: `douyin_search`

**Trigger**: User wants to search Douyin content by keyword.

**Steps**:

1. **Extract keywords** from the user's natural language request.
   - "搜索一下海鲜视频" → keyword: `海鲜视频`
   - "帮我找抖音上做菜的视频" → keyword: `做菜`
   - "抖音上最近火的猫咪内容" → keyword: `猫咪`
   - "douyin seafood cooking" → keyword: `seafood cooking`

2. **Run web_search** with the keyword targeting Douyin:
   ```
   web_search(query="<keyword> site:douyin.com", count=10)
   ```
   Also run a broader search for richer results:
   ```
   web_search(query="抖音 <keyword> 视频", count=10)
   ```

3. **Parse results** — extract from search results:
   - Video URLs: `https://www.douyin.com/video/<id>`
   - Search pages: `https://www.douyin.com/search/<keyword>`
   - Descriptions and snippets from search result titles/descriptions

4. **Enrich** — for each distinct video URL found, optionally use `web_fetch`
   to extract more detail. If the page is behind CAPTCHA, fall back to
   search result metadata only.

5. **Format output** as a clean list:

   ```
   🔍 抖音搜索：海鲜视频
   ━━━━━━━━━━━━━━━━━━━━━

   1. **盘点捞汁小海鲜** — 看哪位主播吃的最过瘾
      🔗 https://www.douyin.com/search/捞汁小海鲜

   2. **全网最火主播吃海鲜合集**
      🔗 https://www.douyin.com/search/全网最火主播吃海鲜合集

   ...
   ```

### Trending: `douyin_trending`

**Trigger**: User asks about Douyin trending/hot topics (抖音热搜/热门/趋势).

**Steps**:

1. Run web_search:
   ```
   web_search(query="抖音热搜榜 today", count=10, freshness="day")
   ```

2. Parse and format the trending topics.

### Video Detail: `douyin_detail`

**Trigger**: User provides a specific Douyin video URL or wants info about one.

**Steps**:

1. Try `web_fetch(url=<douyin_video_url>)` to extract metadata.
2. If blocked by CAPTCHA, try `web_search(query="site:douyin.com <video_id>")`.
3. Return whatever metadata is available (title, author, description).

---

## Output Format

Always include:
- **Search keyword** used
- **Result count** found
- Each result with: **title**, brief **description** (if available), **link**

For searches with no results:
- Say so clearly
- Suggest trying a different or shorter keyword
- Suggest browsing directly at `https://www.douyin.com/search/<keyword>`

---

## Limitations

- Douyin aggressively blocks automated access (CAPTCHA, auth requirements)
- Video metadata may be limited to what search engines have indexed
- Cannot download videos — only discover and describe them
- Search results depend on search engine coverage, which may lag behind live Douyin
- For real-time or comprehensive search, the user should browse Douyin directly

---

## Tips

- **Shorter keywords work better** — `海鲜` over `海鲜视频大全最新`
- **Chinese keywords** yield more results than English for Douyin content
- If a search returns few results, try the Chinese equivalent of the term
- Combine with the `douyin` script optimization skill for content creation workflows