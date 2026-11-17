---
name: crypto-signals-router
description: >
  Routes to the appropriate agent in the crypto-signals-plugin team.
  Trigger when the user asks about crypto trade signals, market analysis,
  price data, crypto news sentiment, Telegram channel publishing, x402 wallet
  management, signal performance, or anything related to running an automated
  crypto signals operation. Lean toward delegation — if crypto signals, market
  data fetching, news analysis, x402 payments for APIs, or Telegram channel
  management is any part of the task, route it to the appropriate agent below.
---

# Crypto Signals Team — 24/7 Operations Router

This plugin runs continuously 24 hours a day, 7 days a week on **OpenClaw** or **Hermes Agent**. The signals cycle runs every 30 minutes. The watchdog runs every 5 minutes. A weekly performance summary publishes every Monday at 09:00 UTC.

---

## Agent Map

| Task | Agent | Schedule / Trigger |
|------|-------|--------------------|
| Sign x402 payment / manage wallet spend | `wallet-keeper` | On-demand (called by market-scout/news-sentinel) |
| Fetch price data / OHLCV / on-chain metrics | `market-scout` | Every cycle (parallel with news-sentinel) |
| Fetch news / sentiment / regulatory events | `news-sentinel` | Every cycle (parallel with market-scout) |
| Generate a trade signal | `signal-forge` | Every cycle (after both data agents complete) |
| Publish to Telegram / format signal message | `channel-captain` | Every cycle + Monday summary |
| System health / auto-recovery | `watchdog` | Every **5 minutes**, 24/7 |

---

## When to route to each agent

| User says / context | Route to |
|---|---|
| "Sign this x402 payment" / "How much have we spent today?" | `wallet-keeper` |
| "Get BTC price" / "Fetch market data" / "Get OHLCV for ETH" | `market-scout` |
| "What's the latest crypto news?" / "Score this news item" | `news-sentinel` |
| "Generate a signal" / "What should I trade?" / "Analyze the market" | `signal-forge` |
| "Post to Telegram" / "Format the signal" / "Publish the signal" | `channel-captain` |
| "Check system health" / "Is the bot running?" / "Any errors?" | `watchdog` |
| "Run signals" / "Run the full cycle" / "Check for signals now" | All agents via `scripts/run-cycle.sh` |
| Simple price question (one-liner, no signal needed) | Handle in main thread |

---

## Full Cycle Orchestration (every 30 min)

```
scripts/run-cycle.sh
│
├── [PARALLEL] market-scout   → ~/.crypto-signals/market-snapshot.json
│   └── wallet-keeper (on 402 challenge)
│
├── [PARALLEL] news-sentinel  → ~/.crypto-signals/news-briefing.json
│   └── wallet-keeper (on 402 challenge)
│
├── signal-forge              → ~/.crypto-signals/trade-signal.json
│   (receives both outputs above)
│
└── channel-captain           → publishes to Telegram
    └── wallet-keeper (for x402 premium subscription gating)
```

Watchdog runs independently every 5 minutes:
```
scripts/watchdog.sh
├── Check heartbeat age (threshold: HEARTBEAT_TIMEOUT_MINUTES=35)
├── Check error log spike (alert if ≥3 errors in 5min window)
├── Check Telegram bot connectivity
├── Check x402scan reachability
└── Check today's spend vs DAILY_SPEND_CAP_USDC
    └── Auto-pause + alert if cap reached
```

---

## Runtime Support

### OpenClaw
Plugin is linked to `~/.openclaw/plugins/crypto-signals-plugin`. Scheduling is done via **system cron**:
```cron
*/30 * * * *  ~/.gemini/config/plugins/crypto-signals-plugin/scripts/run-cycle.sh
*/5  * * * *  ~/.gemini/config/plugins/crypto-signals-plugin/scripts/watchdog.sh
0 9  * * 1    ~/.gemini/config/plugins/crypto-signals-plugin/scripts/run-cycle.sh weekly-summary
```

### Hermes Agent
Plugin is linked to `~/.hermes/skills/crypto-signals-plugin`. Scheduling is done via **Hermes built-in scheduler**:
```bash
hermes schedule add --name crypto-signals-cycle  --cron "*/30 * * * *" --skill crypto-signals-plugin/crypto-signals-router
hermes schedule add --name crypto-signals-watchdog --cron "*/5 * * * *" --skill crypto-signals-plugin/watchdog
hermes schedule add --name crypto-signals-weekly   --cron "0 9 * * 1"  --skill crypto-signals-plugin/channel-captain
```

### Persistent Linux Service (optional, either runtime)
```bash
# Install systemd timer for watchdog (more reliable than cron)
sudo cp ~/.gemini/config/plugins/crypto-signals-plugin/config/crypto-signals-watchdog.{service,timer} /etc/systemd/system/
sudo systemctl enable --now crypto-signals-watchdog.timer
```

---

## Required Environment Variables

| Variable | Required | Description |
|---|---|---|
| `WALLET_PRIVATE_KEY` | ✅ | EVM private key (Base network) for x402 payments |
| `TELEGRAM_BOT_TOKEN` | ✅ | Telegram bot token for publishing |
| `TELEGRAM_CHANNEL_ID` | ✅ | Channel ID (e.g., `@mycryptosignals`) |
| `OPERATOR_TELEGRAM_CHAT_ID` | ✅ | Your personal chat ID for watchdog alerts |
| `WATCHLIST_TOKENS` | ✅ | Comma-separated tokens (e.g., `BTC,ETH,SOL`) |
| `CHANNEL_WALLET_ADDRESS` | ✅ | USDC address for premium subscription revenue |
| `MAX_SESSION_SPEND_USDC` | Optional | Default: `5.0` |
| `MAX_SINGLE_PAYMENT_USDC` | Optional | Default: `0.50` |
| `DAILY_SPEND_CAP_USDC` | Optional | Default: `10.0` |
| `PREMIUM_SIGNAL_PRICE_USDC` | Optional | Default: `0.50` |
| `MIN_WALLET_BALANCE_USDC` | Optional | Default: `1.0` |
| `MAX_DATA_AGE_SECONDS` | Optional | Default: `120` |
| `HEARTBEAT_TIMEOUT_MINUTES` | Optional | Default: `35` |

---

## Quick Start

```bash
# 1. Install the plugin
bash ~/.gemini/config/plugins/crypto-signals-plugin/scripts/install.sh

# 2. Fill in your credentials
nano ~/.gemini/config/plugins/crypto-signals-plugin/.env

# 3. Test the first cycle manually
bash ~/.gemini/config/plugins/crypto-signals-plugin/scripts/run-cycle.sh

# 4. Check logs
tail -f ~/.crypto-signals/cron.log

# 5. The cron / hermes scheduler will now run it automatically 24/7
```

---

## State & Logs (all in `~/.crypto-signals/`)

| File | Description |
|---|---|
| `heartbeat` | Touched on every successful cycle completion |
| `error.log` | All ERROR and CRITICAL log entries |
| `cron.log` | stdout/stderr from run-cycle.sh |
| `watchdog.log` | stdout/stderr from watchdog.sh |
| `spend-log.jsonl` | Every x402 payment: timestamp, seller, amount, URL |
| `signal-log.jsonl` | Every signal published: ID, channel, message ID, outcome |
| `last-cycle.json` | Metadata from the most recent cycle |
| `market-snapshot.json` | Latest raw market data |
| `news-briefing.json` | Latest raw news data |
| `trade-signal.json` | Latest signal output from signal-forge |
| `spend-paused` | Flag file — if present, cycles are paused. Delete to resume |
| `cycle.lock` | flock file — prevents concurrent cycles |
