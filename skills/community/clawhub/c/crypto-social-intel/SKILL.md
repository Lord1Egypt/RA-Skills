---
name: crypto-social-intel
version: 1.0.0
description: Crypto social intelligence skill for AI agents. Activate when user mentions social trends, sentiment analysis, KOL signals, mention surge, Fear & Greed Index, 社交热度, 情绪分析, 恐惧贪婪指数, 热词爆发, KOL提及, 舆情监控, which tokens are trending on social media, is sentiment bullish or bearish, unusual social activity around a token, crypto social alpha, what's the Fear and Greed Index today.
metadata: {"openclaw":{"requires":{},"mcp":{"antalpha":{"url":"https://mcp-skills.ai.antalpha.com/mcp","tools":["crypto-social-trending","crypto-sentiment-score","crypto-kol-signals","crypto-mention-surge","crypto-fear-greed"]}}}}
---

# Crypto Social Intel

Social intelligence layer for crypto tokens. Powered by Santiment GraphQL API + alternative.me Fear & Greed Index.

**5 Tools:**
- `crypto-social-trending` — Top tokens by social volume
- `crypto-sentiment-score` — Sentiment score for a specific token
- `crypto-kol-signals` — Social dominance anomaly (KOL proxy, v1.0: social dominance as proxy, not real Twitter KOL data)
- `crypto-mention-surge` — Detect abnormal mention spikes
- `crypto-fear-greed` — Fear & Greed Index (real-time, free)

## MCP Endpoint

```
https://mcp-skills.ai.antalpha.com/mcp
```

> **Environment switching:** For local dev/test, replace with `http://localhost:3000/mcp`.

Protocol: MCP Streamable HTTP (JSON-RPC over HTTP with `mcp-session-id` header).

### Connection Flow

```
1. POST /mcp → initialize (get mcp-session-id from response header)
2. POST /mcp → tools/call  (with mcp-session-id header)
```

## Data Sources

| Tool | Source | Real-time | API Key |
|------|--------|-----------|---------|
| crypto-social-trending | Santiment | ⚠️ Free tier: ~35-day lag | Required |
| crypto-sentiment-score | Santiment | ⚠️ Free tier: ~35-day lag | Required |
| crypto-kol-signals | Santiment | ⚠️ Free tier: ~35-day lag | Required |
| crypto-mention-surge | Santiment | ⚠️ Free tier: ~35-day lag | Required |
| crypto-fear-greed | alternative.me | ✅ Real-time | None |

> **Note:** Santiment free tier has ~35-day data lag. For real-time social data, upgrade to Santiment Basic ($49/mo) and update `SANTIMENT_API_KEY` on the server — no code changes needed.

## MCP Tools (5)

### crypto-social-trending
Get top crypto tokens ranked by social volume.

**Parameters:**
- `limit` (optional): 1-50, default 10
- `time_range` (optional): `"24h"` | `"7d"`, default `"7d"`

**Response example:**
```json
{
  "items": [
    {
      "rank": 1,
      "slug": "bitcoin",
      "symbol": "BTC",
      "social_volume": 2413,
      "sentiment_score": 57,
      "signal_level": "LOW",
      "trend_change": "N/A",
      "data_source": "santiment"
    }
  ],
  "meta": { "data_source": "santiment", "note": "Free tier: ~35-day lag" }
}
```

---

### crypto-sentiment-score
Get sentiment score and trend for a specific token.

**Parameters:**
- `symbol` (required): Token symbol or slug, e.g. `"BTC"`, `"ETH"`, `"bitcoin"`
- `time_range` (optional): `"7d"` | `"30d"`, default `"7d"`

**Response example:**
```json
{
  "symbol": "BTC",
  "sentiment_score": 57,
  "social_volume": 19301,
  "trend_direction": "down",
  "change_vs_prev": "-17.4%",
  "signal_level": "LOW",
  "data_source": "santiment"
}
```

---

### crypto-kol-signals
Detect social dominance anomalies as KOL activity proxy.

> v1.0 uses `social_dominance_total` as KOL proxy. Real Twitter KOL data planned for v2.0.

**Parameters:**
- `symbol` (required): Token symbol or slug
- `time_range` (optional): `"7d"` | `"30d"`, default `"7d"`
- `threshold` (optional): Surge multiplier threshold, 1-10, default 1.5

**Response example:**
```json
{
  "symbol": "BTC",
  "social_dominance": 1.16,
  "dominance_change": -33,
  "surge_ratio": 0.67,
  "sentiment_direction": "bullish",
  "signal_level": "LOW",
  "note": "Social dominance anomaly used as KOL proxy. Real KOL data (Twitter API) planned for v2.0."
}
```

---

### crypto-mention-surge
Detect tokens with abnormal social mention spikes.

**Parameters:**
- `threshold` (optional): Surge ratio vs historical avg, default 2.0
- `time_window` (optional): `"7d"` | `"30d"`, default `"7d"`
- `limit` (optional): 1-50, default 10

**Response example:**
```json
{
  "items": [
    {
      "rank": 1,
      "symbol": "SOL",
      "current_volume": 1200,
      "historical_avg": 400,
      "surge_ratio": 3.0,
      "sentiment_direction": "bullish",
      "signal_level": "HIGH"
    }
  ],
  "total_found": 1
}
```

---

### crypto-fear-greed
Get the Crypto Fear & Greed Index. **Real-time, no API key required.**

**Parameters:**
- `days` (optional): History days to return, 1-30, default 7

**Response example:**
```json
{
  "current": {
    "value": 23,
    "classification": "Extreme Fear",
    "date": "2026-04-15"
  },
  "trend": "improving",
  "signal_level": "MEDIUM",
  "market_note": "市场偏恐慌，情绪面有支撑，注意底部信号。",
  "history": [...],
  "data_source": "alternative.me"
}
```

**Contrarian signal logic:**
- Extreme Fear (≤20) → 🔴 HIGH (historical buy opportunity)
- Fear (21-40) → 🟡 MEDIUM
- Neutral (41-60) → 🟢 LOW
- Greed (61-79) → 🟢 LOW
- Extreme Greed (≥80) → 🔴 HIGH (caution, potential top)

## Signal Levels

| Level | Condition | Badge |
|-------|-----------|-------|
| HIGH | sentiment>70 + surge>3x, OR Extreme Fear/Greed | 🔴 |
| MEDIUM | sentiment≥50 + surge≥2x, OR Fear | 🟡 |
| LOW | otherwise | 🟢 |

> **Note:** `crypto-kol-signals` signal_level is based on `dominance_change` (independent of the sentiment+surge rule above). Extreme dominance change (>50% or <-50%) → HIGH; moderate change → MEDIUM; otherwise LOW.

## Workflow

### Check Market Sentiment (most common)

```
1. crypto-fear-greed { days: 7 }           ← overall market mood
2. crypto-social-trending { limit: 10 }    ← what's hot
3. Present combined view to user
```

### Analyze Specific Token

```
1. crypto-sentiment-score { symbol: "ETH" }
2. crypto-kol-signals { symbol: "ETH", threshold: 1.5 }
3. Combine: sentiment score + dominance signal → final assessment
```

### Early Warning Scan

```
1. crypto-mention-surge { threshold: 2.0, limit: 10 }
2. For tokens with HIGH/MEDIUM signals → crypto-sentiment-score to confirm
3. Alert user to tokens with multiple converging signals
```

### Combined with Smart Money

When social signal + on-chain signal converge:
```
1. crypto-mention-surge detects abnormal spike
2. → Call smart-money-signal to check if whales are buying
3. Two signals converging → stronger conviction
```

## Message Template

When presenting social intel to user:

```
📊 市场情绪总览
恐惧贪婪指数: 23 — Extreme Fear 🔴
趋势: improving ↗
注记: 历史上极度恐慌区间往往是逆向机会，但需结合链上数据确认。

🔥 社交热榜 Top 5
#1 BTC  vol=2413  sentiment=57  🟢 LOW
#2 ETH  vol=491   sentiment=52  🟢 LOW
#3 SOL  vol=386   sentiment=52  🟢 LOW
```

**Mention surge alert:**
```
🚨 社交提及暴增预警
SOL: 当前3000 vs 均值400 → 7.5x ↑ 🔴 HIGH (bullish)
建议: 关注链上是否有聪明钱跟进
```

## Agent Behavior Rules

### On "市场情绪怎么样" / "market sentiment"
1. Call `crypto-fear-greed` first (real-time, fast)
2. Optionally call `crypto-social-trending` for top tokens
3. Present combined view
4. **When Santiment data is involved, always append:** `⚠️ 社交数据来自 Santiment 免费层，存在约 35 天延迟，仅供参考。`

### On "BTC情绪" / "SOL sentiment" / specific token
1. Call `crypto-sentiment-score { symbol }`
2. If signal_level is HIGH or MEDIUM, also call `crypto-kol-signals`
3. Present score + trend + signal
4. **Always append disclaimer:** `⚠️ 数据来自 Santiment 免费层，存在约 35 天延迟，仅供参考，勿作实时决策依据。`
5. **For kol-signals output, always note:** `注：v1.0 KOL 信号以社交主导度代理，非真实 Twitter KOL 数据，v2.0 将接入 Twitter API。`

### On "哪些币在暴涨社交" / "mention surge" / "异常热度"
1. Call `crypto-mention-surge { threshold: 2.0 }`
2. For HIGH signal items, offer to do deeper analysis
3. **Always append disclaimer:** `⚠️ 数据来自 Santiment 免费层，存在约 35 天延迟，仅供参考。`

### On "恐惧贪婪" / "fear greed" / "市场贪婪指数"
1. Directly call `crypto-fear-greed`
2. Present value, classification, trend, market note

## Supported Token Slugs

Common symbol → slug mapping (Santiment):

| Symbol | Slug |
|--------|------|
| BTC | bitcoin |
| ETH | ethereum |
| SOL | solana |
| BNB | binance-coin |
| XRP | ripple |
| DOGE | dogecoin |
| ADA | cardano |
| AVAX | avalanche |
| DOT | polkadot |
| LINK | chainlink |
| UNI | uniswap |
| ARB | arbitrum |
| OP | optimism |
| SUI | sui |

For unlisted tokens, pass the full Santiment slug directly (e.g. `"pepe"`, `"floki"`).

---

由 Antalpha AI 提供聚合服务 | Powered by Antalpha AI
