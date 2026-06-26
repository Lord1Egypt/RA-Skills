---
name: polymarket-monitor
description: "Monitor Polymarket prediction markets for price movements, volume spikes, and new listings. Track specific markets, check order book depth, and surface trending predictions. Use when asked about Polymarket, prediction market prices, market volume, or contract probabilities."
metadata:
  openclaw:
    emoji: "🔮"
    requires:
      bins: ["curl", "jq"]
---

# Polymarket Monitor

Track prediction market prices, volume, and liquidity on Polymarket using the Gamma API and CLOB API.

## When to Use

Use this skill when the user asks about:
- Trending or popular Polymarket markets
- Current price or probability for a prediction market
- Volume or trading activity on a market
- Order book depth or liquidity for a specific outcome
- New or recently created prediction markets
- Price movements or volume spikes on Polymarket

## Key Concepts

- **Price = Implied Probability**: A contract at $0.65 means 65% implied probability
- **Token ID**: Each outcome (Yes/No) has a unique token ID used by the CLOB API
- **Condition ID**: The unique identifier for a market (question) in the Gamma API
- **CLOB**: Central Limit Order Book — where bids and asks are matched

## Operations

### 1. List Trending Markets

Show the top active markets sorted by 24-hour volume:

```bash
curl -s "https://gamma-api.polymarket.com/markets?closed=false&active=true&order=volume24hr&ascending=false&limit=10" \
  | jq '[.[] | {
    question: .question,
    price_yes: (.outcomePrices // "[]" | fromjson | .[0] // "N/A"),
    price_no: (.outcomePrices // "[]" | fromjson | .[1] // "N/A"),
    volume_24h: ((.volume24hr // 0) | tonumber | round),
    total_volume: ((.volumeNum // 0) | tonumber | round),
    liquidity: ((.liquidityNum // 0) | tonumber | round),
    end_date: .endDate
  }]'

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-polymarket-monitor-skill/](https://agentbets.ai/guides/openclaw-polymarket-monitor-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
