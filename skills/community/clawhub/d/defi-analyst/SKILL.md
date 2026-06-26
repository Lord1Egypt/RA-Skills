---
name: defi-analyst
description: DeFi research and analysis via Tavily MCP, GeckoTerminal API, and DeFiLlama. Use for protocol research, TVL tracking, yield analysis, token discovery, and competitive landscape research.
---

# DeFi Analyst Skill

Research DeFi protocols, track yields, analyze TVL trends, and monitor the competitive landscape.

## Prerequisites

- **Tavily API key** — free at [tavily.io](https://tavily.io)
- **mcporter** — OpenClaw skill for MCP tool calling
- **curl + jq** — for GeckoTerminal/DeFiLlama API calls

### Setup Tavily MCP

```bash
mcporter config add tavily https://mcp.tavily.com/mcp/?tavilyApiKey=<YOUR_KEY>
```

## Core Operations

### Protocol Research (Tavily)

```bash
mcporter call tavily.tavily_search query="Aave V3 protocol overview yield lending" max_results=5 search_depth="advanced"
```

### TVL Tracking (DeFiLlama)

```bash
# Get protocol TVL
curl -s "https://api.llama.fi/protocol/aave" | jq '{name: .name, tvl: .tvl, change_1d: .change_1d, change_7d: .change_7d}'

# Top DeFi protocols by TVL
curl -s "https://api.llama.fi/tvl" | jq '.[0:10]'

# Lending rates overview
curl -s "https://api.llama.fi/overview/lending" | jq '.categories[0:10]'
```

### Token Price + Volume (GeckoTerminal)

```bash
# Pool data for a token
curl -s "https://api.geckoterminal.com/api/v2/networks/eth/tokens/0x.../info" | jq '{name, base_volume, quote_volume, pool_count}'

# Trending pools on a network
curl -s "https://api.geckoterminal.com/api/v2/networks/eth/pools" | jq '.[0:5] | .[].attributes | {pool: .name, volume_24h: .volume_usd.h24s, tvl: .tvl_usd}'

# Specific pool APY
curl -s "https://api.geckoterminal.com/api/v2/networks/bsc/pools/0x..." | jq '.data.attributes | {apy: .apy_7d, tvl: .tvl_usd}'
```

### DEX Aggregator Research

```bash
# Compare yields across DEXes
curl -s "https://api.llama.fi/overview/dex?exclude_bridge=true" | jq '.dexes[0:5]'
```

## Analyst Agents

### Technical Analyst
On top of classic candlestick patterns, pulls 24h volume delta, liquidity depth ratios, and cross DEX price variance. Output: `{direction, confidence, key_levels}`.

### Sentiment Analyst
Aggregates social sentiment via Tavily (`{token} sentiment today`) + Moltbook agent network pulse. Output: sentiment score (-1 to +1) with weighted breakdown by source credibility.

### Debate Round
Bull Agent → Tavily for bull cases + on-chain growth metrics.
Bear Agent → Tavily for risk factors + whale wallet outflows.
Synthesized output: `{bull_probability, bear_probability, reconciled_direction, confidence}`.

## Use Cases

### Research a Protocol

```bash
# 1. TVL + metrics
TVL=$(curl -s "https://api.llama.fi/protocol/your-protocol" | jq '.tvl')
# 2. Recent news via Tavily
mcporter call tavily.tavily_search query="protocol audit exploit update 2026" max_results=5
# 3. Competitor comparison
mcporter call tavily.tavily_search query="protocol vs aave vs compound defi" max_results=3
```

### Track Yield Opportunities

```bash
# Get all lending rates
curl -s "https://api.llama.fi/overview/lending" | jq '.categories[0:10]'
```

### DeFi Landscape Analysis

```bash
mcporter call tavily.tavily_search query="DeFi trends 2026 yield farming liquid staking real yield" max_results=10 search_depth="advanced"
```

## Rate Limits

- GeckoTerminal: 30 req/min, no auth needed
- DeFiLlama: ~60 req/min, public API
- Tavily: 20 req/min free tier, 1000 req/month free
