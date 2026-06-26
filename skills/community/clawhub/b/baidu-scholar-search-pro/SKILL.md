---
name: baidu-scholar-search
slug: baidu-scholar-search-pro
description: Baidu Scholar Search — Search Chinese and English academic literature including journals, conferences, dissertations. Best for Chinese research context.
metadata:
  openclaw:
    emoji: 🔬
    requires:
      bins: ["curl"]
---

# Baidu Scholar Search 🔬

## When to Use

Trigger this skill when user asks to:
- Search Chinese academic papers or journals
- Find Chinese dissertation or thesis
- Research topics with Chinese context
- Access CNKI or Wanfang databases via Baidu Scholar

## Workflow

1. **Accept search query** — Chinese or English keywords
2. **Query Baidu Scholar API** — get paper metadata
3. **Parse results** — title, author, source, citation count
4. **Return structured data** — with links and metadata

## API Setup

Required: `BAIDU_API_KEY` environment variable
Register at: https://xueshu.baidu.com/

## Notes

- Works best for Chinese academic literature
- Integrates with CNKI, Wanfang, VIP databases
- Supports bilingual search (Chinese + English)
