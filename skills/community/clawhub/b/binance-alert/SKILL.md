---
name: binance-alert
description: Binance smart alert system. Monitors price/change alerts, new listings, Alpha airdrop opportunities, and HODLer announcements via Telegram. No Binance API Key required.
homepage: https://github.com/cnwpdb/binance-alert-skill
metadata: {"clawdbot":{"requires":{"bins":["python3"],"env":["TG_BOT_TOKEN","TG_CHAT_ID"]}}}
---

# BinanceAlert

Monitors Binance market events and pushes real-time alerts via Telegram.

## Required Environment Variables

| Variable | Description |
|----------|-------------|
| `TG_BOT_TOKEN` | Telegram Bot Token (from @BotFather) |
| `TG_CHAT_ID` | Telegram target Chat ID |

The script reads these from `/data/freqtrade/user_data/.secrets.env` automatically, or from system environment variables directly.

## Price Alert

```bash
python3 {baseDir}/scripts/binance_alert.py price <SYMBOL> <target_price> [above|below]
```

Example: alert when BTC breaks $100,000
```bash
python3 {baseDir}/scripts/binance_alert.py price BTCUSDT 100000 above
```

## Change Alert (24h %)

```bash
python3 {baseDir}/scripts/binance_alert.py change <SYMBOL> <threshold_pct>
```

Example: alert when ETH moves more than 8% in 24h
```bash
python3 {baseDir}/scripts/binance_alert.py change ETHUSDT 8
```

## New Listing Monitor

```bash
python3 {baseDir}/scripts/binance_alert.py listing
```

## Alpha Airdrop Scanner

```bash
python3 {baseDir}/scripts/binance_alert.py alpha
```

Scans Binance Web3 Alpha tokens, scores by KYC holders, alpha points multiplier, and market cap.

## Announcement Monitor (HODLer Airdrops)

```bash
python3 {baseDir}/scripts/binance_alert.py announcement
```

## Run All Checks (for cron/timer)

```bash
python3 {baseDir}/scripts/binance_alert.py run
```

## Status

```bash
python3 {baseDir}/scripts/binance_alert.py status
```

## Notes

- Requires `TG_BOT_TOKEN` and `TG_CHAT_ID` (read from `.secrets.env` or system env)
- State persisted to `/data/freqtrade/user_data/binance_alert_state.json`
- Price/change alerts auto-mark as triggered after firing, no duplicate pushes
- New listing monitor initializes baseline on first run, no push
- Recommended: run via systemd timer every 5 minutes using the `run` command