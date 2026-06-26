---
name: big-ai-news
description: Aggregate and deduplicate AI news from multiple Chinese and English tech news sources into a single merged digest. Use when the user asks for "AI news", "AI news digest", "big AI news", "merge AI news", "AI新闻汇总", "AI资讯汇总", or wants AI news from multiple sources combined. Supports fetching from TechNews 科技新報, 量子位 QbitAI, 科技岛 TechNice, AIBase, and other AI news sites. Outputs deduplicated, categorized news with titles, briefs, and links.
---

# Big AI News — Multi-Source AI News Aggregator

Fetch AI news from multiple sources, deduplicate overlapping stories, merge into one categorized digest.

## Default Sources

Fetch from all sources in parallel (independent, no ordering dependency):

| # | Source | URL | Method |
|---|--------|-----|--------|
| 1 | TechNews 科技新報 | `https://technews.tw/category/ai/` | web_fetch; fallback `web_search` with `site:technews.tw AI` + `freshness: day` |
| 2 | 量子位 QbitAI | `https://www.qbitai.com/` | web_search `site:qbitai.com` + `freshness: day` (direct fetch returns 403) |
| 3 | 科技岛 TechNice | `https://www.technice.com.tw/category/issues/ai/` | web_fetch; fallback `web_search` with `site:technice.com.tw AI` + `freshness: day` |
| 4 | AIBase | `https://news.aibase.com/zh/daily` | web_fetch to get latest digest link, then fetch the first (most recent) digest page |

If the user specifies specific sources, only use those. If they say "all" or don't specify, use all four defaults.

## Workflow

1. **Fetch all sources in parallel** — use independent tool calls for each source simultaneously.
2. **Extract** — for each source, collect: title, brief summary (1-2 sentences), and link URL.
3. **Deduplicate** — compare titles and topics across sources. If the same story appears in multiple sources (e.g., same model release, same company announcement), merge into one entry and list all source links.
4. **Categorize** — group into categories:
   - 🧠 大模型发布 (Model Releases)
   - 🤖 AI Agent & 工具 (Agents & Tools)
   - 💰 AI 市场 & 应用 (Market & Applications)
   - ⚡ AI 芯片 & 硬件 (Chips & Hardware)
   - 🔐 AI 安全 & 风险 (Security & Risks)
   - 📊 行业 & 政策 (Industry & Policy)
   - Adjust categories if the news doesn't fit neatly.
5. **Output** — numbered list per category, each item with: bold title, 1-2 sentence brief, and link(s).

## Output Format

```markdown
## 📰 YYYY-MM-DD AI 新闻汇总（N 源合并）

### 🧠 大模型发布

**1. Title — Subtitle**
Brief summary here.
🔗 https://example.com/link

### 🤖 AI Agent & 工具
...
```

- Title in bold, one-line subtitle after " — "
- Brief: 1-2 concise sentences, no fluff
- Link on its own line with 🔗 prefix
- If merged from multiple sources, list all links
- End with a short "today's top picks" callout (2-3 most significant items)

## Fallback Handling

- If a source fails to fetch, note it and continue with remaining sources.
- If all sources fail, use `web_search` with broad queries like "AI news today 2026" as last resort.
- Never block the whole digest because one source is down.

## Language

- Output in the same language the user uses (Chinese or English).
- If mixed, default to Chinese (中文) since sources are predominantly Chinese.
