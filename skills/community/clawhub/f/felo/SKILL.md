---
name: felo
description: "AI-synthesized web search via Felo API — aggregates 15-40 sources into structured summaries. Use when: (1) researching a topic that needs multi-source synthesis, (2) scanning community trends (Reddit, GitHub, X, blogs), (3) market news requiring cross-source analysis, (4) phrases like '幫我查', '搜尋一下', 'research', 'what's trending'. NOT for: single-site lookups (use web_fetch), time-critical queries needing exact timestamps (use web_search), or quick 1-second lookups."
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires":
          {
            "bins": ["curl", "jq"],
            "env": ["FELO_API_KEY"],
            "optionalPaths": ["~/.config/felo/api_key"],
          },
      },
  }
---

# Felo AI Search

Use Felo AI for comprehensive, AI-summarized web search when you need:
- Multiple sources consolidated into structured insights
- Trending topics with context (community scanning)
- Research questions requiring cross-source synthesis

**Do NOT use for:**
- Time-sensitive queries requiring exact timestamps
- Single-source lookups (use web_fetch instead)
- When speed is critical (Felo takes ~15 seconds vs web_search ~1 second)

## Setup

1. Sign up at [felo.ai](https://felo.ai) and get an API key from **Settings → API Keys**
2. Store the key in one of these ways:
   - **Environment variable** (recommended): `export FELO_API_KEY="your-key-here"`
   - **File** (set strict permissions):
     ```bash
     mkdir -p ~/.config/felo
     echo "your-key-here" > ~/.config/felo/api_key
     chmod 600 ~/.config/felo/api_key
     ```

## Basic Usage

```bash
curl -s -X POST https://openapi.felo.ai/v2/chat \
  -H "Authorization: Bearer ${FELO_API_KEY:-$(cat ~/.config/felo/api_key 2>/dev/null)}" \
  -H "Content-Type: application/json" \
  -d '{"query": "Your search query here (1-2000 chars)"}' | jq .
```

## Response Structure

```json
{
  "status": "ok",
  "data": {
    "answer": "AI-generated summary...",
    "query_analysis": {
      "queries": ["optimized", "search", "terms"]
    },
    "resources": [
      {
        "link": "https://...",
        "title": "Source title",
        "snippet": "Relevant excerpt"
      }
    ]
  }
}
```

**Key fields:**
- `data.answer` — AI-synthesized answer (use for summaries)
- `data.resources` — Source links (typically 15-40 sources)

## Common Patterns

### Community Scanning

```bash
curl -s -X POST https://openapi.felo.ai/v2/chat \
  -H "Authorization: Bearer ${FELO_API_KEY:-$(cat ~/.config/felo/api_key 2>/dev/null)}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the top 5 trending topics in the OpenClaw AI agent community this week? Include specific discussions from Reddit, GitHub, X (Twitter), forums, and blogs. Provide source links."
  }' > /tmp/felo_result.json

ANSWER=$(jq -r '.data.answer' /tmp/felo_result.json)
SOURCES=$(jq -r '.data.resources[0:10] | .[] | "- [\(.title)](\(.link))"' /tmp/felo_result.json)
SOURCE_COUNT=$(jq '.data.resources | length' /tmp/felo_result.json)
```

## Rate Limits

- Default: 100 requests/minute per API key
- Response headers: `X-RateLimit-*`
- Handle 429 errors with exponential backoff

## Error Handling

Common errors:
- `INVALID_API_KEY` (401) — Check your API key
- `QUERY_TOO_LONG` (400) — Max 2000 chars
- `RATE_LIMIT_EXCEEDED` (429) — Slow down requests

## When to Use vs web_search

| Use Case | Tool | Reason |
|----------|------|--------|
| Community trends (5+ sources) | **Felo** | AI synthesis, broader coverage |
| Specific site search | **web_search** | Precise site: operator |
| Need timestamps | **web_search** | Felo has no time metadata |
| Cross-source analysis | **Felo** | AI-generated insights |
| Speed-critical | **web_search** | ~1s vs ~15s |

## Notes

- Felo returns 15-40 sources but no timestamps
- Query can include time hints ("this week", "recent") but results are not guaranteed to be time-filtered
- Best for **trend detection** and **topic synthesis**, not **time-sensitive monitoring**
