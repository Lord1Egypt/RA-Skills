---
name: deep-research
description: Deep web research across 11 Chinese and international sources (Baidu, Bing, Sogou, Quark, ChinaSo, WeChat, Yandex, Zhihu, Bilibili, V2EX, GitHub). Use when the user asks for deep research, comprehensive search, multi-source search, or needs results from Chinese platforms (Zhihu, Bilibili, WeChat). Falls back to built-in web_search if the API is unavailable.
---

# Deep Research

Search across 11 sources simultaneously via a local Agentic RAG-CN API, then synthesize results with evidence tables and contradiction detection.

## Prerequisites

Agentic RAG-CN must be running locally. Check with:

```bash
curl -s http://localhost:18888/health
```

If unavailable, fall back to built-in `web_search` tool.

## Usage

Call the API with a POST request:

```bash
curl -s -X POST http://localhost:18888/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"question": "用户的问题"}'
```

Parse the JSON response and present results to the user in a readable format.

## Response Format

The API returns:

- `answer` — Structured answer with evidence tables
- `sources` — List of sources used (with URLs)
- `confidence` — Confidence score (0-1)
- `contradictions` — Any contradictions found across sources
- `trace` — Pipeline execution trace (16 steps)

## When to Use vs Fallback

| Condition | Action |
|-----------|--------|
| API health check succeeds | Use deep-research API |
| API health check fails | Fall back to `web_search` |
| User asks about Chinese topics (知乎, B站, 微信) | Prefer deep-research |
| User asks general English questions | `web_search` is usually sufficient |

## Presenting Results

Format the response as:

1. **Answer summary** — 2-3 sentences
2. **Evidence table** — Key findings with sources
3. **Contradictions** (if any) — Highlight conflicting info
4. **Sources** — Numbered list of URLs
