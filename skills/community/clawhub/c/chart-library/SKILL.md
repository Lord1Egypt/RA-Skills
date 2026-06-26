---
name: chart-library
summary: Visual chart pattern search — find similar historical stock charts and see what happened next
tags: [finance, investing, technical-analysis, stock-market, charts]
author: chartlibrary
homepage: https://chartlibrary.io
api_base: https://chartlibrary.io
requires:
  - url: https://chartlibrary.io/api/v1/status
---

# Chart Library

Find historically similar stock chart patterns from 24M+ embeddings across 15K+ symbols and 10 years of data. See what happened next — 1, 3, 5, and 10-day forward returns with AI summaries.

## Usage

Ask your agent:
- "Find charts similar to AAPL on 2024-06-15"
- "What are today's most interesting chart patterns?"
- "Analyze TSLA's 3-day chart vs historical analogs"

## API Endpoints

- `POST /api/v1/analyze` — Complete analysis in one call (recommended)
- `POST /api/v1/search/text` — Search for similar patterns
- `POST /api/v1/search/batch` — Multi-symbol search
- `GET /api/v1/discover/picks` — Today's top patterns
- `POST /api/v1/follow-through` — Forward return computation
- `POST /api/v1/summary` — AI summary generation
- `GET /api/v1/status` — Database stats

## Auth

No API key required for free tier (100 req/day). For higher limits, get a key at [chartlibrary.io/developers](https://chartlibrary.io/developers).

## Links

- [OpenAPI spec](https://chartlibrary.io/api/openapi.json)
- [AI plugin manifest](https://chartlibrary.io/.well-known/ai-plugin.json)
- [MCP server](https://github.com/grahammccain/chart-library-mcp)
