---


name: freqtrade-us-setup
description: "Complete setup guide for running Freqtrade (cryptocurrency trading bot) legally in the United States. Use when setting up Freqtrade for the first time, choosing a US-compatible exchange, configuring API keys securely, or troubleshooting US-specific exchange issues. Covers Kraken setup, Docker configuration, API key security, and dry-run testing. Trigger phrases: freqtrade US, US exchanges freqtrade, freqtrade legal US, freqtrade Kraken setup, freqtrade docker config."
metadata: {"clawdbot":{"emoji":"\ud83d\udcc8","requires":{"bins":["docker"]},"os":["linux","darwin","win32"],"version":"1.0.5"}}
---



# Freqtrade US Setup Guide

> **⚠️ Security First:** This guide emphasizes legal, secure setup for US users. Never use VPNs to bypass exchange geo-restrictions — it violates ToS, risks fund freezes, and may be illegal.

## 1-Minute Intro

## Before You Run: Pin, Protect, and Dry-Run

This skill sets up a bot that will hold real exchange credentials. Three
things must be true before the bot runs.

**1. Pin the version.** Do not clone and run an unpinned default branch — that
branch can change under you, and it will receive your trading credentials.

```bash
# Clone Freqtrade at an exact release tag, and verify what you are about to run
git clone --branch 2024.11 --depth 1 https://github.com/freqtrade/freqtrade.git
cd freqtrade
git rev-parse HEAD   # record the exact commit you reviewed
```

Pin the Docker image to a digest as well, not a floating tag:

```yaml
image: freqtradeorg/freqtrade:2024.11@sha256:<reviewed-digest>
```

Never clone the default branch without a `--branch` tag. The default branch can
change under you, and it will receive your trading credentials. The Quick Start
below uses the same pinned clone as this section — there is no unpinned path.

**2. Protect the credentials.** Do not put real API key values in
`docker-compose.yml` or in a config file that could be committed.

```yaml
# WRONG - real key values inline in a tracked file
environment:
  - FREQTRADE__EXCHANGE__KEY=REAL_KEY_HERE
  - FREQTRADE__EXCHANGE__SECRET=REAL_SECRET_HERE

# RIGHT - reference variables, values supplied from an untracked env file
environment:
  - FREQTRADE__EXCHANGE__KEY=${EXCHANGE_KEY}
  - FREQTRADE__EXCHANGE__SECRET=${EXCHANGE_SECRET}
```

Keep the values in a `.env` file that is gitignored (and verify `.env` is
actually ignored before adding it), or in a secrets manager. Use a
**read-only key with withdrawal permission disabled** until you have a reason
to do otherwise.

**Disabled withdrawals do not protect you from trading losses.** A key without
withdrawal permission can still place, modify, and cancel real orders against
your balance. Treat the key as full account access to your trading balance, and
keep `dry_run: true` until you have deliberately decided to go live. See
[Kraken's API key security guidance](https://support.kraken.com/articles/api-key-security).

**3. Start in dry-run.** Run `dry_run: true` first and confirm the bot behaves
correctly before it can place a real order.

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
# Clone Freqtrade at a pinned release tag (same pin as the safety section above)
git clone --branch 2024.11 --depth 1 https://github.com/freqtrade/freqtrade.git
cd freqtrade
git rev-parse HEAD   # record the exact commit you reviewed

# Create config (interactive wizard)
docker-compose run --rm freqtrade new-config --config /freqtrade/user_data/config.json

# When prompted:
# - Exchange: kraken
# - Stake currency: USDT (or USD)
# - Dry-run: yes (always start paper trading!)
```

### Step 3: Secure Your Keys

Freqtrade uses a specific double-underscore env var pattern (`FREQTRADE__SECTION__KEY`) that overrides config values at runtime. Create a `.env` file in your Freqtrade directory. This file holds the real values and must stay untracked:

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

**Make sure `.env` is actually delivered into the container.** A `.env` file
next to `docker-compose.yml` is read by Compose for variable substitution, but
`FREQTRADE__*` variables are only visible inside the container if they are
passed through in `environment:`. Reference them rather than hardcoding values:

```yaml
services:
  freqtrade:
    environment:
      - FREQTRADE__EXCHANGE__KEY=${FREQTRADE__EXCHANGE__KEY}
      - FREQTRADE__EXCHANGE__SECRET=${FREQTRADE__EXCHANGE__SECRET}
```

The values live in the untracked `.env`; the compose file holds only references.

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
