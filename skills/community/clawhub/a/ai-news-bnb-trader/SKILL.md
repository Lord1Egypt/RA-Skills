---
name: ai-news-bnb-trader
description: TypeScript (Node.js 20+) AI news-driven BNB strategy trading bot for BSC. Use when user wants event/news sentiment signals, strict risk controls, and automated WBNB<->stablecoin swaps with dry-run safety, panic mode, status, and approval revoke tooling.
---

# AI News BNB Trader

Run an event-driven BSC trading bot using news sentiment + risk gates.

## Safety first

- Default `DRY_RUN=true`.
- Never print private key/seed in logs.
- Only whitelist assets (`WBNB`, `USDT`/`BUSD`/`USDC`).
- Panic mode immediately disables trading.

## Commands

```bash
npm run start -- start
npm run start -- status
npm run start -- panic
npm run start -- revoke-approvals
npm run key:encrypt -- --out ./secrets/key.json
```

## News modes

- Poll REST via `NEWS_API_URL` every `NEWS_POLL_SECONDS`
- Optional WebSocket via `NEWS_WS_URL`

Both modes dedupe on `news.id` and log failures with exponential backoff.

## Signal models

- `RuleSignalModel` (default): keyword rules with explainable reasons
- `OpenAISignalModel` (optional): enabled when `OPENAI_API_KEY` is set; timeout + fallback to rules

## Strategy

- Buy WBNB with stablecoin if `sentiment * impact >= BUY_THRESHOLD` and confidence >= `MIN_CONF`
- Sell WBNB to stablecoin if `sentiment * impact <= -SELL_THRESHOLD` and confidence >= `MIN_CONF`
- Enforce all risk gates before execution

## Risk controls

- Max order notional / max position pct / daily trade cap
- Daily loss cap (MTM approximation)
- TP/SL from avg entry
- Cooldown between trades
- Slippage cap from quote
- Consecutive failures -> SAFE_MODE

## Notes

- Prefer private RPC (`PRIVATE_RPC_URL`) when provided.
- For production: validate token/DEX addresses and add deeper MEV defenses.
