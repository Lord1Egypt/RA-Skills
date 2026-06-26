---
name: content-summary
description: Short alias for content-search-summarization. Use this to search public content platforms, rank the top relevant items, and summarize them with links.
license: Proprietary session artifact for local Copilot use
---

# Content summary skill

This is the short public alias for:

- `content-search-summarization`

Also available as simpler aliases:

- `summary`
- `内容摘要`

Use this skill when you want to:

- search Bilibili, YouTube, or similar public content platforms
- pick the top N relevant results for a topic
- summarize each item in Chinese with links

## Primary guidance

1. Prefer `opencli` for supported platforms.
2. If `opencli` is unavailable, fall back to Playwright scraping of public result pages.
3. Rank by relevance first, popularity second.
4. Open selected result pages and use metadata to improve summaries.
5. Use a structured output with source, capture time, link, summary, and confidence.

## Key rules

- Always include source links.
- Include capture time or say when the timestamp is not visible.
- Do not pretend a full video was watched if only metadata was collected.
- Phrase summaries conservatively when based on public page metadata.
- Add a confidence label and a short caveat when the summary is metadata-based.

## Quick invocation template

You do not need to use only `/content-summary`.

Reliable invocation patterns include:

1. `/content-summary`
2. `use the content-summary skill`
3. a natural-language request that clearly asks for content search, ranking, and summary output

Use prompts like:

```text
Use /content-summary to find the top 5 results for <topic> on <platform> and summarize each item with links and confidence labels.
```

```text
使用 /content-summary 在 <平台> 搜索 <主题>，筛选 Top 5，并输出带链接与置信度的摘要。
```

```text
Please find the top results for <topic> on <platform>, rank them by relevance, and summarize each item with links and confidence notes.
```

## Output contract

The skill output should always include:

1. search method used (`opencli` or fallback)
2. keyword and capture scope
3. ranked results with links
4. per-item confidence and caveat
5. explicit note when summaries are metadata-inferred

## Pointer

For the full detailed playbook, also see:

- `skills/content-search-summarization/SKILL.md` in this repository
