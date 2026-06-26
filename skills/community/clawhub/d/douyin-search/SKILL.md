---
name: douyin-scraper
description: >
  Search Douyin (抖音) videos by natural language keywords.
  Supports phrases like "搜索一下海鲜视频", "帮我找抖音上的猫咪视频",
  "抖音搜美食教程". Falls back to keyword suggestions when not logged in.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: {}
---

# Douyin Scraper — 抖音搜索

> 搜索抖音视频，用自然语言就行。

## What This Skill Does

Search Douyin (抖音) for videos by keyword. You say "搜索一下海鲜视频", it finds seafood videos on Douyin.

**Supports natural language input** — the agent extracts the search intent and converts it to a keyword, no rigid command format needed.

## When to Use This Skill

- User asks to search Douyin / 抖音 for videos
- "搜索一下XXX视频", "帮我找抖音上的XXX", "抖音搜XXX"
- "douyin search for XXX"
- Any request to find/browse Douyin content

## Search Protocol (Agent Instructions)

When the user wants to search Douyin, follow these steps:

### Step 1: Extract keyword

Parse the user's natural language request into a search keyword:

| User says | Keyword |
|---|---|
| 搜索一下海鲜视频 | 海鲜视频 |
| 帮我找抖音上的猫咪 | 猫咪 |
| 抖音搜美食教程 | 美食教程 |
| douyin search funny cats | funny cats |
| 找一些关于编程的短视频 | 编程 |

If the keyword is ambiguous, use the Douyin suggestion API to refine it (see Step 3).

### Step 2: Search via Playwright (persistent profile)

Run the search script:

```bash
python3 scripts/douyin_search.py "<keyword>" --count 10 --json
```

This uses a persistent browser profile at `.browser-profile/` to maintain login state.

**If the result says `login_required`:**

- Tell the user they need to log in once
- Offer to open a browser for QR code scanning: `python3 scripts/douyin_search.py --login`
- The login session persists in `.browser-profile/` — only needed once
- After login, retry the search

### Step 3: Fallback — Keyword suggestions (no login needed)

If login is not available, use the Douyin suggestion API for related keywords:

```bash
curl -s "https://www.douyin.com/aweme/v1/web/search/sug/?keyword=<url-encoded-keyword>&aid=6383" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://www.douyin.com/"
```

This returns a `sug_list` with related search terms. Present these to the user as:

> 还没登录抖音，无法直接搜视频，但找到以下相关搜索词：
> - 吃海鲜视频
> - 海鲜视频素材
> - 海鲜视频赶海
> ...
> 登录后即可搜索完整结果。需要我帮你登录吗？

### Step 4: Format and present results

Present search results clearly:

```
🔍 搜索 "海鲜视频" — 共 10 个结果

1. **小明的海鲜日记** — 今天赶海抓到超大海蟹！
   ❤️ 12.3万  💬 856  ▶️ 89.2万
   🔗 https://www.douyin.com/video/7xxx

2. ...
```

For Discord/WhatsApp (no markdown tables), use the list format above.

## Alternative: Agent-Driven Browser Search

If the Playwright script fails or isn't available, you can search using the OpenClaw `browser` tool directly:

1. `browser action=navigate url=https://www.douyin.com/search/<encoded-keyword>`
2. `browser action=snapshot` — check if results loaded or login is needed
3. `browser action=screenshot` — show the user the search page
4. If results are visible, extract them from the snapshot

## File Structure

```
douyin-scraper/
├── SKILL.md                  ← This file
├── README.md                 ← Overview
├── skill.json                ← Metadata
├── examples.md               ← Usage examples
├── scripts/
│   ├── douyin_search.py      ← Main search script (Playwright)
│   └── format_results.py     ← Result formatter
└── .browser-profile/         ← Persistent browser state (gitignored)
```

## Notes

- The persistent browser profile stores cookies — **do not commit it to git**
- First-time users must login via `--login` flag (requires a display/GUI)
- On headless servers without GUI, the suggestion API fallback still works
- The search API may rate-limit; add delays between repeated searches
- Douyin's anti-scraping measures may change; the Playwright approach is more resilient than direct HTTP calls

## Boundaries

- This skill searches for public Douyin content only
- It does NOT download videos (use a separate downloader skill)
- It does NOT post content or interact with user accounts beyond search
- Respect Douyin's Terms of Service — don't abuse search or scrape at scale