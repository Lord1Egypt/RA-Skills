---
name: crypto-signals-automation
description: Build and operate a crypto signal trading automation using RapidAPI cryptexAI Buy & Sell Signals as signal source and dYdX v4 for execution. Use when setting up end-to-end signal ingestion, API subscription/key configuration, dYdX credential/bootstrap (API key + passphrase + signing material), cron execution, TP/SL handling, retries, cleanup, and Telegram notifications.
---

# Crypto Signals Automation

Use this skill to create a full pipeline: RapidAPI signals -> normalized signal objects -> dYdX v4 order execution.

## Workflow

1. Collect setup inputs first:
   - RapidAPI plan + key (`X-RapidAPI-Key`)
   - dYdX wallet address + mnemonic file path + subaccount
   - risk settings (max leverage, margin per trade, max open positions, close-after-hours)
   - TP/SL mode (reduce-only conditional orders)
   - alert channels (Telegram chat IDs)
2. Validate RapidAPI connectivity with `scripts/rapidapi_fetch.py`.
3. Generate env template with `scripts/bootstrap_env.py`.
4. Wire runtime script/cron that:
   - fetches symbols/signals,
   - filters fresh active signals,
   - opens positions with retries,
   - places TP/SL reduce-only conditional orders,
   - closes stale positions,
   - cleans orphan reduce-only orders,
   - sends Telegram notifications for open/close with PnL.
5. Test with one symbol in controlled mode before enabling full symbol set.

## RapidAPI source

- API: `cryptexAI - Buy & Sell Signals`
- Base host header: `cryptexai-buy-sell-signals.p.rapidapi.com`
- Endpoints:
  - `GET /getSymbols`
  - `GET /getSignalsForSymbol?symbol=...`

Use the most recent `active=true` signal per symbol. Deduplicate by signal `id`.

## dYdX execution rules

- Use dYdX v4.
- Open position with market semantics.
- Set TP/SL immediately after open as reduce-only conditional orders:
  - TP type: take-profit-market
  - SL type: stop-market / stop-limit equivalent in client
- Retry failed order submissions up to total 3 attempts.
- Keep signal->order client_id mapping in state and only cancel matching reduce-only orders on cleanup.

## Security

- Never commit real API keys/secrets.
- Store secrets in `.env` with strict file permissions (`chmod 600`).
- Treat mnemonic/passphrase as secrets.
- If a token was exposed in chat/history, rotate it.

## References

- API details: `references/rapidapi-cryptexai.md`
- Setup checklist: `references/setup-checklist.md`
