---
name: ai-news
description: Fetch and display AI news digest from AI资讯速览 (https://ai-digest.liziran.com/zh/). Use when the user asks for AI news, today's AI digest, latest AI updates, or mentions "AI资讯速览". Fetches the latest digest and presents each item as a titled summary.
---

# AI News Digest

Fetch and present the latest AI news from AI资讯速览.

## Source

- Index: `https://ai-digest.liziran.com/zh/`
- Each daily digest is a linked page from the index (first item = most recent)

## Workflow

1. Fetch the index page at `https://ai-digest.liziran.com/zh/` with `web_fetch`
2. Extract the **first (most recent) digest link** from the list
3. Fetch that digest page
4. Present each numbered item with its **title** and **summary** in a clean, readable format

## Output Format

For each news item, output:

```
**NN [Title]**
[Summary in 1–3 sentences]
```

Separate items with `---`. Use the original Chinese titles and summaries as-is (do not translate unless user asks).

## Notes

- The index lists digests in reverse chronological order; always pick the first one unless the user specifies a date
- Short items (04, 05 …) may only have a one-liner — keep them brief
- If the user asks for a specific date, find the matching link from the archive at `https://ai-digest.liziran.com/zh/archive.html`
