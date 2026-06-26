---
name: freqtrade-us-setup
description: "Complete setup guide for running Freqtrade (cryptocurrency trading bot) legally in the United States. Use when setting up Freqtrade for the first time, choosing a US-compatible exchange, configuring API keys securely, or troubleshooting US-specific exchange issues. Covers Kraken setup, Docker configuration, API key security, and dry-run testing. Trigger phrases: freqtrade US, US exchanges freqtrade, freqtrade legal US, freqtrade Kraken setup, freqtrade docker config."
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["docker"]},"os":["linux","darwin","win32"]}}
---

# Freqtrade US Setup Guide

> **⚠️ Security First:** This guide emphasizes legal, secure setup for US users. Never use VPNs to bypass exchange geo-restrictions — it violates ToS, risks fund freezes, and may be illegal.

## 1-Minute Intro

Freqtrade (the Python bot) is legal in the US. The catch: many exchanges block US traders. **Use Kraken** — it's stable, US-compliant, and officially supported.

## Quick Start

### Step 1: Generate Kraken API Keys

1. Log into Kraken → Settings → API
2. Create a new key with these permissions **exactly**:
   - ✅ **Funds: Query**
   - ✅ **Orders: Query open orders & trades**
   - ✅ **Orders: Query closed orders & trades**
   - ✅ **Orders: Create & modify orders**
   - ✅ **Orders: Cancel & close orders**
   - ❌ **NEVER enable Withdraw** (critical security risk)

### Step 2: Docker Setup

```bash
# Clone Freqtrade
git clone https://github.com/freqtrade/freqtrade.git
cd freqtrade

# Create config (interactive wizard)
docker-compose run --rm freqtrade new-config --config /freqtrade/user_data/config.json

# When prompted:
# - Exchange: kraken
# - Stake currency: USDT (or USD)
# - Dry-run: yes (always start paper trading!)
```

### Step 3: Secure Your Keys

Freqtrade uses a specific double-underscore env var pattern (`FREQTRADE__SECTION__KEY`) that overrides config values at runtime. Create a `.env` file in your Freqtrade directory:

```bash
# Kraken API (required)
FREQTRADE__EXCHANGE__KEY=your-kraken-api-key
FREQTRADE__EXCHANGE__SECRET=your-kraken-secret

# Web UI (optional)
FREQTRADE__API_SERVER__USERNAME=your-username
FREQTRADE__API_SERVER__PASSWORD=your-password
FREQTRADE__API_SERVER__JWT__SECRET__KEY=your-jwt-secret
FREQTRADE__API_SERVER__WS__TOKEN=your-ws-token

# Telegram (optional — leave empty if not using)
# Note: Multi-bot Telegram setup via env vars is unverified.
# If you hit issues, consult Freqtrade docs for your specific setup.
# Never hardcode sensitive tokens in files that could be committed to git.
FREQTRADE__TELEGRAM__TOKEN=
FREQTRADE__TELEGRAM__CHAT_ID=
```

**Add to `.gitignore` immediately:**

```bash
echo ".env" >> .gitignore
```

In `user_data/config.json`, leave the exchange key and secret as **empty strings** — Freqtrade will populate them from the env vars automatically:

```json
{
  "exchange": {
    "name": "kraken",
    "key": "",
    "secret": "",
    "ccxt_config": {},
    "ccxt_async_config": {}
  },
  "stake_currency": "USDT",
  "dry_run": true,
  "max_open_trades": 3
}
```

### Step 4: Validate & Test

```bash
# Download historical data
docker-compose run --rm freqtrade download-data \
  --pairs BTC/USDT ETH/USDT \
  --timeframe 5m \
  --timerange 20240101-

# Run dry-run for 1-2 weeks before going live
docker-compose up
```

## Before Going Live

1. **Dry-run minimum:** 1-2 weeks of paper trading
2. **Backtest:** Verify your strategy works historically
3. **Start small:** Go live with a conservative stake amount
4. **Monitor:** Watch closely for first 24-48 hours

## When to Read References

- **exchange-comparison.md** → Comparing Kraken, Binance.US, Coinbase
- **security-checklist.md** → API key management, fund protection, common mistakes

---

**Disclaimer:** Freqtrade is open-source, experimental software. Trading involves financial risk. This guide is provided as-is with no guarantees. Use at your own risk.

**Questions?** See references/ or check Freqtrade's official docs at https://www.freqtrade.io
