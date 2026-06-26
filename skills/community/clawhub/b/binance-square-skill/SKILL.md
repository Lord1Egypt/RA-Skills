---
name: binance-square
description: Binance Square (币安广场) signal agent. Scrapes 200+ posts via Puppeteer + API interception, detects bot-pushed narratives, runs on-chain confirmation (OI/funding/liquidation via Coinglass), and produces directional trade signals (LONG/SHORT/AVOID). Optionally pushes signal reports to Telegram. Triggers on mentions of "binance square", "广场信号", "MM 信号", "做市商扫描", crypto narrative tracking, or trading signal generation.
metadata:
  openclaw:
    requires:
      bins:
        - node
        - curl
      env:
        - COINGLASS_BASE
        - TG_BOT_TOKEN
        - TG_CHAT_ID
---

# Binance Square Signal Agent

End-to-end trading signal pipeline built on the thesis that **market makers seed narratives on Binance Square before / during accumulation**. Square is the largest unblocked Chinese crypto info source — tracking narrative flow there is the sentiment equivalent of tracking on-chain fund flow.

## First-Time Setup

The skill ships with two Node.js scripts that need `puppeteer-core` installed once. After ClawHub installs this skill to `~/.claude/skills/binance-square/`, run:

```bash
cd ~/.claude/skills/binance-square && npm install
```

Then verify Chrome/Chromium is installed (auto-detected on Win/Mac/Linux). Override with `CHROME_PATH` env var if needed.

## Optional Configuration (env vars)

| Var | Purpose | Effect if missing |
|-----|---------|-------------------|
| `COINGLASS_BASE` | Coinglass API or proxy base URL (e.g. `https://your-proxy/api`) | Step 2 (on-chain) is skipped, direction calls degrade |
| `TG_BOT_TOKEN` | Telegram bot token from @BotFather | `scan:tg` mode skips the push, returns the message text instead |
| `TG_CHAT_ID` | Telegram chat ID (use @userinfobot) | Same as above |
| `CHROME_PATH` | Override Chrome binary path | Auto-detected (Win/Mac/Linux + Edge fallback) |

## Modes (dispatch on `$ARGUMENTS`)

| Input | Action |
|-------|--------|
| `scan` (default if no args) | Full pipeline: scrape feed + drill top 3 coins + direction judgment |
| `scan:tg` | Same as `scan` plus Telegram DM push (requires TG env vars) |
| `coin:RAVE` | Deep-drill a specific coin's hashtag page (~200 posts) |
| `read:URL` | Read and summarize a single Binance Square article |
| `read:KEYWORD` | Search Square for a keyword and summarize top results |

---

## Pipeline: `scan` and `scan:tg`

### Step 1 — Scrape

```bash
node ~/.claude/skills/binance-square/scrape-square.mjs --drill --top 3 --scrolls 25 --pages 10
```

The scraper writes a `square-YYYY-MM-DD-HHmm.json` file in its own directory by default. Override with `--out PATH`. Read the JSON output. Key fields per coin in `coinRanking`:

- `mentions`, `botPct`, `verifiedPosts`
- `sentiment.label` (BULLISH / BEARISH / NEUTRAL), `sentiment.score`, `sentiment.bullish`, `sentiment.bearish`
- `views`, `likes`

`drillResults[COIN]` contains the same breakdown for each drilled hashtag page (larger sample, bot-dense — this is where coordinated narrative pushes are visible).

### Step 2 — On-chain confirmation (skip if `COINGLASS_BASE` not set)

For each non-baseline coin (not BTC/ETH/BNB/SOL/XRP/DOGE) with 2+ feed mentions:

```bash
curl -s "$COINGLASS_BASE/coinglass?type=oi-exchanges&symbol=COIN"
curl -s "$COINGLASS_BASE/coinglass?type=funding-exchanges&symbol=COIN"
curl -s "$COINGLASS_BASE/coinglass?type=liquidation"
```

Extract:
- **OI**: `total.chg24h` (24h OI change %)
- **Funding**: average `rate` across major exchanges (Binance / Bybit / OKX)
- **Liquidation**: `long24h` vs `short24h` USD per coin
- **Price 24h**: from gainers (Step 3) or derive from OI deltas

> The user must provide their own `COINGLASS_BASE` URL — either the official Coinglass API with their key, or their own proxy. Without this, direction judgment falls back to Square sentiment + price action only.

### Step 3 — Gainers cross-reference

WebFetch `https://www.binance.com/zh-CN/markets/coinInfo` — extract 领涨榜 (top gainers) with 24h% change.

### Step 4 — Direction judgment

Combine the four signal sources for each candidate coin:

```
Signal weights (strongest first):

  1. Liquidation ratio  → strongest (actual money flow)
     short_liq >> long_liq  → LONG (short squeeze in progress)
     long_liq >> short_liq  → SHORT (long cascade in progress)

  2. Funding extreme    → contrarian signal
     rate < -0.10%       → LONG bias (shorts overcrowded)
     rate > +0.10%       → SHORT bias (longs overcrowded)

  3. OI + Price         → momentum / divergence
     OI↑ price↑          → momentum continuation
     OI↑ price flat      → pre-positioning, watch breakout direction
     OI↑ price↓          → short building (may squeeze)
     OI↓ price↓          → long liquidation cascade

  4. Square sentiment   → contrarian indicator (with bot quality filter)
     Retail BEAR + funding negative + OI rising → MM accumulating vs retail → LONG
     Retail BULL + bot% > 40%                   → bot-pushed pump → AVOID
     Retail BULL organic (low bot%) + rising price → trend follow LONG
```

Direction call: **LONG ✅ / SHORT 🔻 / AVOID ⚠️ / WATCH 👀**

- `WATCH` for OI divergence with unclear direction
- `AVOID` for bot-dominated noise or event-driven moves (FUD / hack / legal)

### Step 5 — Save full report

Write detailed markdown report to `~/.claude/skills/binance-square/reports/signal-YYYY-MM-DD-HHmm.md` (create the `reports/` dir if needed). Include:

- Candidates table (coin, posts, bot%, sentiment, OI, funding, liq ratio, direction)
- Per-coin direction rationale
- Drill bot breakdown
- Gainers cross-ref
- Risk notes

### Step 6 — Telegram push (only if `scan:tg` and TG env vars set)

Write condensed summary (<4000 chars) to a temp file:

```bash
cat > /tmp/tg-signal.txt <<'EOF'
*广场信号* YYYY-MM-DD HH:MM

*Feed* (N posts, X% bot)
COIN: N mentions, BEAR/BULL | ...

*Drill Bot%*
#COIN: N posts, X% bot, sentiment Y

*方向判断*
COIN: *LONG/SHORT/AVOID* [emoji]
  OI +X% | Funding X% | Liq 多M:空M | 广场 BEAR/BULL
  理由: [one sentence]

*涨幅榜* TOP1 +X% | TOP2 +X%
EOF

node ~/.claude/skills/binance-square/send-telegram.mjs --file /tmp/tg-signal.txt
```

If `TG_BOT_TOKEN` or `TG_CHAT_ID` env var is missing, skip this step and return the message text in the response instead.

---

## Mode: `coin:TICKER`

Deep-drill a specific coin's topic page (~200 posts vs ~20 on main feed):

```bash
node ~/.claude/skills/binance-square/scrape-square.mjs --coin TICKER --pages 10
```

Then run Step 2 (on-chain) + Step 4 (direction) for just this coin. Report:

```
#TICKER deep dive — N posts scanned

Bot activity: X% bot (top bot authors: ...)
Sentiment: BULL / BEAR / NEUTRAL  (N bull / N bear / N neutral)
OI 24h: +X%   |   Funding: X%   |   Liq L:S
Price 24h: +X%

Direction: LONG / SHORT / AVOID — [reason]

Top 3 sample posts: ...
```

---

## Mode: `read:URL` or `read:KEYWORD`

### URL form (`read:https://www.binance.com/...`)

WebFetch the article. Extract: title, author, publish time, content, engagement, coin mentions, hashtags. Flag author if username matches `Square-Creator-xxx` → potential bot.

### Keyword form (`read:RAVE 爆仓`)

WebSearch `site:binance.com/square KEYWORD`, then WebFetch top 3-5 results. For each, extract summary + sentiment + author type. Aggregate: overall sentiment, bot %, narrative theme.

---

## Bot Detection (built into scraper)

**Layer 1** (username pattern):
- Display name matches `/^Square-Creator-[a-f0-9]+$/` → BOT_SUSPECT (never customized profile)
- Otherwise → tentatively LIKELY_HUMAN

**Layer 2** (behavioral, post-hoc):
- Default username (`square-creator-*` profile ID) + 3+ posts in batch + avg views < 200 → BOT_SUSPECT
- Any author with 5+ posts + avg views < 100 → BOT_SUSPECT (catches custom-named bots)

Sentiment scoring **only counts non-bot posts** to avoid contamination.

The drill mode reveals **bot rings** — accounts that appear across multiple coin hashtags with high post counts and low engagement = signature of coordinated narrative promotion.

---

## Output Contract

Return to main agent (concise — full detail lives in the saved report):

1. **Top 3 actionable signals** with direction (LONG/SHORT/AVOID) + one-sentence rationale each
2. Path to full saved report
3. If `scan:tg`: confirmation of TG send with message_id, OR the message text + note that env vars weren't configured
4. Critical anomalies: new coin trending, extreme funding rate, bot farm coordination

## Disclaimer

This tool finds patterns. It is **not financial advice**. Trading decisions and risk management are entirely the user's responsibility. Past pattern correlations do not predict future moves.
