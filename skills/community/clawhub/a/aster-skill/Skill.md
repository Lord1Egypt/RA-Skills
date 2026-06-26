# crypto-news-trader

A Clawhub skill that:
1) Monitors a Twitter/news stream via **OpenNews MCP** (aka “6551 news monitoring skill”).
2) Classifies news for **BTC / ETH / SOL / BNB** as **bullish / bearish / neutral** using an LLM prompt.
3) Executes **long** (BUY) or **short** (SELL) orders on **Aster** via aster-skill client.

## Strategy Logic

### Step 1 — News Monitoring (OpenNews MCP)
- Pull latest news (last 1 hour) from configured sources (Twitter + major crypto media).
- Filter to only BTC/ETH/SOL/BNB-related stories.
- Deduplicate by article id (24h cache).

### Step 2 — Bullish/Bearish Decision
- LLM analyzes:
  - source credibility
  - event importance
  - timeliness
  - market sensitivity
- Outputs strict JSON:
  - `sentiment`: bullish | bearish | neutral
  - `confidence`: 0..1
  - `signal_strength`: strong | medium | weak
  - `recommended_action`: open_long | open_short | wait | skip

Trade rules:
- Only trade if:
  - confidence >= 0.70
  - signal_strength != weak
- Open long if sentiment=bullish and confidence >= 0.65
- Open short if sentiment=bearish and confidence >= 0.65
- Otherwise wait/skip.

### Step 3 — Order Execution on Aster
- Set leverage (default 5x)
- Place MARKET order
- Attach stop-loss / take-profit
- Per-coin cooldown (default 30 minutes)

## Requirements

### Install OpenNews MCP (6551)
This skill declares the MCP in `skill.json`, and expects it to be installed via:

```bash
npx clawhub install opennews-mcp