---
name: crypto-lens
description: >
  CryptoLens — AI-driven multi-coin crypto analysis. Compare 2-5 coins (relative performance,
  correlation matrix, volatility ranking), get single-coin technical analysis charts with
  MA(7/25/99), RSI, MACD, and Bollinger Bands, or run AI market analysis with scoring engine
  (0-100 composite score + actionable signals). Dark-theme PNG output.
  Per-call billing via SkillPay: 1 token (0.001 USDT) per call for all commands.
  Use when user asks for crypto comparison, portfolio analysis, technical indicators,
  RSI, MACD, Bollinger Bands, multi-coin analysis, or "should I buy/sell" questions.
metadata:
  {
    "clawdbot": {
      "emoji": "📊",
      "requires": { "bins": ["python3"] }
    },
    "skillpay": {
      "pricing": [
        { "command": "chart", "tokens": 1, "usd": "0.001" },
        { "command": "compare", "tokens": 1, "usd": "0.001" },
        { "command": "analyze", "tokens": 1, "usd": "0.001" }
      ],
      "currency": "USDT",
      "chain": "BNB Chain"
    },
    "credentials": {
      "embedded": true,
      "description": "SkillPay billing API key and Skill ID are embedded in the script. This is the standard SkillPay integration pattern — the key can only charge users, not withdraw funds.",
      "services": ["skillpay.me"]
    }
  }
---

# CryptoLens 📊

AI-driven multi-coin cryptocurrency analysis with technical indicators.

## ⚠️ Billing Disclosure

This is a **paid skill**. Each command costs 1 token (0.001 USDT) via [SkillPay.me](https://skillpay.me).

**How billing works:**
1. You provide your BNB Chain wallet address via `--user-id` — this is your billing identity
2. The skill calls SkillPay to deduct 1 token from your balance before executing
3. If you have no balance, you receive a payment link to top up with USDT (BNB Chain)
4. You are **never charged without explicit action** — you must click the payment link and approve the transaction in your wallet
5. The embedded API key belongs to the skill publisher and can only initiate charges, not access your wallet or withdraw funds

**You control your spending:** deposit only what you want to use. No subscriptions, no auto-renewal.

## Commands

### 1. Multi-Coin Compare

Compare 2-5 cryptocurrencies — relative performance overlay, volatility ranking, and correlation matrix.

```bash
python3 {baseDir}/scripts/crypto_lens.py compare BTC ETH SOL [--duration 7d] [--user-id UID]
```

**Examples:**
- `python3 {baseDir}/scripts/crypto_lens.py compare BTC ETH SOL`
- `python3 {baseDir}/scripts/crypto_lens.py compare BTC ETH SOL HYPE ARB --duration 7d`
- `python3 {baseDir}/scripts/crypto_lens.py compare PEPE WIF BONK --duration 3d`

**Output:**
- Price comparison table with change %, volatility ranking
- Normalized performance overlay chart (who outperformed)
- Return correlation matrix heatmap
- Chart saved as PNG

**Billing:** 1 token (0.001 USDT) per call.

### 2. Technical Analysis Chart

Single-coin candlestick chart with full technical indicator stack.

```bash
python3 {baseDir}/scripts/crypto_lens.py chart BTC [--duration 24h] [--user-id UID]
```

**Examples:**
- `python3 {baseDir}/scripts/crypto_lens.py chart BTC`
- `python3 {baseDir}/scripts/crypto_lens.py chart ETH --duration 12h`
- `python3 {baseDir}/scripts/crypto_lens.py chart HYPE --duration 2d`

**Indicators included:**
- **MA(7/25/99)** — Short / Medium / Long-term moving averages
- **RSI(14)** — Relative Strength Index with 30/70 zones
- **MACD(12,26,9)** — MACD line, signal line, histogram
- **Bollinger Bands(20,2)** — Volatility envelope

**Billing:** 1 token (0.001 USDT) per call.

### 3. AI Market Analysis

AI-driven scoring engine — comprehensive technical analysis with actionable signal and score.

```bash
python3 {baseDir}/scripts/crypto_lens.py analyze BTC [--duration 24h] [--user-id WALLET]
```

**Examples:**
- `python3 {baseDir}/scripts/crypto_lens.py analyze BTC`
- `python3 {baseDir}/scripts/crypto_lens.py analyze ETH --duration 7d`
- `python3 {baseDir}/scripts/crypto_lens.py analyze HYPE --duration 2d --user-id 0x1234...`

**Output:**
- 🎯 Composite score 0-100 (Strong Bearish → Strong Bullish)
- 🏷️ Signal label: 强烈看涨 / 看涨 / 中性 / 看跌 / 强烈看跌
- 📝 Per-indicator breakdown with point contribution:
  - RSI(14) zone analysis
  - MACD crossover + histogram momentum
  - MA(7/25/99) trend alignment
  - Price vs MA25 position
  - Bollinger Band position
  - Volume trend (price-volume confirmation)
  - Short-term momentum
- 💡 Actionable suggestion (one-line conclusion)
- 📈 Full TA chart attached

**Scoring rules:**
- RSI <30: +20 (oversold bullish) / RSI >70: -20 (overbought bearish)
- MACD golden cross: +15 / death cross: -15
- MA7>MA25>MA99 bullish alignment: +15
- Price at BB lower band: +15 / upper band: -15
- Volume + price confirmation: ±8
- Weighted sum → normalized to 0-100

**Billing:** 1 token (0.001 USDT) per call.

## Duration Format

`30m`, `3h`, `12h`, `24h` (default), `2d`, `7d`, `14d`, `30d`

## Output Format

Returns JSON with:
- `text_plain` — Formatted text summary
- `chart_path` — Path to generated PNG chart

**Chart as image (always when chart_path is present):**
You must send the chart as a **photo**, not as text. In your reply, output `text_plain` and on a new line: `MEDIA: ` followed by the exact `chart_path` value (e.g. `MEDIA: /tmp/cryptolens_chart_BTC_1769204734.png`). Do **not** write `[chart: path]` or any other text placeholder — only the `MEDIA: <chart_path>` line makes the image appear.

## Billing

All commands cost 1 token (0.001 USDT) per call via SkillPay.me (BNB Chain USDT).
Billing credentials (API key and Skill ID) are embedded in the script — this is the standard SkillPay integration pattern for paid skills.

**`--user-id` is required.** Pass the end user's BNB Chain wallet address (e.g. `0x1234...abcd`) as the user_id. This is the same address the user will use to top up balance via the payment link. The wallet address ensures billing identity is consistent across devices and sessions.

Example: `--user-id 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18`

If the user hasn't provided their wallet address yet, ask them for it before running this skill.

If the user's balance is insufficient, a `payment_url` is returned — send it to the user to top up via BNB Chain USDT.

## Data Sources

1. **Hyperliquid API** — Preferred for supported tokens (HYPE, BTC, ETH, SOL, etc.)
2. **CoinGecko API** — Fallback for all other tokens
