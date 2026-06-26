# binance-square — Claude skill (ClawHub)

Trading signal agent built around **Binance Square (币安广场)**. Scrapes the platform's internal feed API (gets ~200 posts per scan vs ~3 from naive WebFetch), drills coin hashtag pages, detects bot-pushed narratives via two-layer classification, cross-references on-chain data (OI / funding / liquidation), and produces directional signals (LONG / SHORT / AVOID).

## Install

```bash
clawhub install binance-square            # (after publishing)
cd ~/.claude/skills/binance-square && npm install
```

## Use (in Claude Code)

```
/binance-square                          # default: scan main feed + drill top 3 coins
/binance-square scan:tg                  # scan + push report to Telegram DM
/binance-square coin:RAVE                # deep-drill #RAVE hashtag (~200 posts)
/binance-square read:https://...         # read a single article
/binance-square read:RAVE 爆仓           # search Square for keyword
```

## Configure (env vars)

| Var | Required for | Notes |
|-----|--------------|-------|
| `COINGLASS_BASE` | On-chain confirmation step | Your Coinglass API base URL or proxy |
| `TG_BOT_TOKEN` | `scan:tg` mode | From [@BotFather](https://t.me/BotFather) |
| `TG_CHAT_ID` | `scan:tg` mode | From [@userinfobot](https://t.me/userinfobot) |
| `CHROME_PATH` | Optional | Override Chrome binary (auto-detected by default) |

Without `COINGLASS_BASE`, the skill skips on-chain checks and falls back to Square sentiment + price action only.
Without `TG_*`, `scan:tg` returns the message text in the response instead of pushing.

## What makes this work

1. **API interception, not DOM scraping** — Puppeteer captures the internal `/bapi/composite/v9/.../feed-recommend/list` responses while scrolling. Each scroll yields ~20 fresh posts with full structured data (coin mentions, engagement, author verification).

2. **Two-layer bot detection**:
   - Layer 1: default `Square-Creator-xxx` username pattern
   - Layer 2: behavioral — high post count + low average views = bot, even with a custom display name (catches sophisticated farms)

3. **Sentiment scoring with bilingual crypto keywords** (做多/做空/抄底/爆仓/long/short/...), counting only non-bot posts to avoid contamination.

4. **Direction matrix** combining liquidation ratio (strongest), funding extremes, OI/price relationship, and Square sentiment — each weighted by signal strength.

5. **Drill mode** — the main feed is moderated (almost no obvious bots), but coin hashtag pages have 30-70% bot density. Drilling reveals coordinated bot rings posting across multiple coins simultaneously.

## Architecture

```
/binance-square <args>
        │
        ▼
  scrape-square.mjs       (Puppeteer + API interception, ~200+ posts)
        │
        ▼
  Coinglass curl × 3      (OI / funding / liquidation per coin)
        │
        ▼
  Direction matrix         (LONG / SHORT / AVOID / WATCH)
        │
        ├─→ Save signal-*.md report
        │
        └─→ (optional) send-telegram.mjs  → DM
```

## Limitations

- Binance Square API is undocumented; payload structure may change. If the scraper breaks, inspect the API call signatures with browser DevTools.
- Coinglass Hobbyist plan restricts `oi-summary`. Per-coin queries work fine.
- Sentiment keyword list is finite — extend in `scrape-square.mjs` for better coverage.
- Bot detection is heuristic. Possible false positives for high-frequency legitimate KOLs.
- Skill is most useful for Chinese-speaking crypto traders since Binance Square is Chinese-dominant.

## Disclaimer

This is a research / pattern-finding tool. **Not financial advice.** Trading decisions and risk management are entirely the user's responsibility.

## License

MIT-0
