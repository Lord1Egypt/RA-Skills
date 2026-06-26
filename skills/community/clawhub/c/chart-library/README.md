# Chart Library — OpenClaw Skill

**Chart Library** is a visual chart pattern search engine that finds historically similar stock charts from 24M+ pre-computed embeddings across 15,000+ symbols and 10 years of data. Given a ticker and date (or a screenshot), it returns the 10 most similar historical charts and shows what happened next -- 1, 3, 5, and 10-day forward returns, distribution stats, and AI-generated summaries.

## Quickstart

### 1. No API Key Required

All endpoints work without authentication (100 requests/day free tier). For higher limits, get an API key at [chartlibrary.io/developers](https://chartlibrary.io/developers).

### 2. Configure in OpenClaw

Add to your OpenClaw agent config:

```yaml
skills:
  - name: chart-library
    source: clawhub://chartlibrary/chart-library
```

Optionally set an API key for higher rate limits:

```bash
export CHART_LIBRARY_API_KEY=cl_your_api_key_here
```

### 3. Try a Search

Ask your agent:

> "Find charts similar to AAPL on 2024-06-15 and show me what happened next."

The agent will use `analyze_pattern` to search, compute forward returns, and summarize — all in one call.

## Example Queries

| Query | What it does |
|-------|-------------|
| `AAPL 2024-06-15` | Find patterns similar to AAPL's chart on June 15, 2024 (regular trading hours) |
| `TSLA 2024-03-10 3d` | Find 3-day window patterns similar to TSLA starting March 10 |
| `GME 2024-01-25 premarket` | Search premarket session patterns |
| `discover picks` | Get today's most interesting patterns from the daily scanner |

## Available Tools

| Tool | Description |
|------|-------------|
| `analyze_pattern` | **Recommended** — search + forward returns + AI summary in one call |
| `search_charts` | Find similar historical chart patterns (text query) |
| `search_batch` | Search multiple symbols at once (up to 20) |
| `get_follow_through` | Compute 1/3/5/10-day forward returns from matches |
| `get_pattern_summary` | AI-generated plain-English summary |
| `get_discover_picks` | Today's top patterns from the daily scanner |
| `get_status` | Database stats (embeddings, symbols, date range) |

## Agent Discovery

Chart Library supports automatic agent discovery via:

- **`/.well-known/ai-plugin.json`** — standard AI plugin manifest
- **OpenAPI spec** — `https://chartlibrary.io/api/openapi.json`
- **MCP server** — `python mcp_server.py` (stdio or SSE transport)

## Using the Python Wrapper

For direct integration without OpenClaw:

```python
from wrapper import ChartLibrary

cl = ChartLibrary()  # works without API key (free tier)

# Full analysis in one call (recommended)
analysis = cl.analyze("AAPL 2024-06-15")
print(analysis["summary"])
print(analysis["outcome_distribution"])

# Search only
results = cl.search("AAPL 2024-06-15")

# Today's picks
picks = cl.discover()
```

## API Tiers

| Tier | Rate Limit | Price | Features |
|------|-----------|-------|----------|
| Free | 100/day | $0 | Text search, follow-through, discover |
| Pro | 10K/month | $49/mo | + Image search, batch, simulator, AI summaries |
| Business | 100K/month | $199/mo | + MCP server, webhooks |

## Full API Documentation

Interactive API docs: [chartlibrary.io/developers](https://chartlibrary.io/developers)

OpenAPI spec: [chartlibrary.io/api/openapi.json](https://chartlibrary.io/api/openapi.json)
