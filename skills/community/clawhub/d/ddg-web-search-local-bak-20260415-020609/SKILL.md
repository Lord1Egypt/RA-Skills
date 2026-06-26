---
name: ddg-web-search
description: Search the web with DuckDuckGo instant answer API and return concise results. Use when the user asks to look something up online, fetch quick facts, or do lightweight web search without browser automation.
---

# ddg-web-search

Use the bundled script for deterministic web lookups:

```bash
{baseDir}/scripts/ddg_search.py "<query>"
```

Rules:
- Prefer short, relevant summaries.
- Return the source URLs when available.
- If no good result exists, say so clearly.

Examples:

```bash
{baseDir}/scripts/ddg_search.py "OpenClaw tools profile"
{baseDir}/scripts/ddg_search.py "weather Amsterdam"
```
