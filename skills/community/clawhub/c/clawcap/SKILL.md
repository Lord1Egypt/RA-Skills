---
name: clawcap
description: Spending cap proxy for OpenClaw. Enforce hard daily and monthly limits across all your AI models (Claude, GPT, Gemini, and more) under one cap. Stop runaway token burn, detect heartbeat loops, and kill agents remotely via Telegram. One URL, one cap, all models tracked together.
version: 1.1.2
metadata:
  openclaw:
    requires:
      env:
        - CLAWCAP_TOKEN
      bins:
        - node
    primaryEnv: CLAWCAP_TOKEN
    emoji: "\U0001F6E1"
    homepage: https://clawcap.co
---

# ClawCap — Spending Cap for OpenClaw

Stop runaway API bills. ClawCap enforces hard spending caps across every model your agents use — Claude, GPT, Gemini, and more — under a single proxy URL.

## What It Does

- **Hard daily & monthly caps** — your agents stop when you hit your limit, not when your wallet is empty
- **All models, one cap** — Claude, GPT, Gemini, DeepSeek, Mistral, and more tracked together
- **Heartbeat detection** — catches agents stuck in polling loops burning tokens
- **Loop detection** — stops agents repeating the same failed request
- **Kill switch** — stop any agent instantly via Telegram or API
- **Real-time tracking** — see exactly what you're spending per model

## Setup (2 minutes)

### 1. Get Your Token

Sign up at [clawcap.co](https://clawcap.co) and grab your proxy token. Free tier works instantly — no credit card needed.

Set it as an environment variable:

```bash
export CLAWCAP_TOKEN="cc_live_your_token_here"
```

### 2. Run Setup

The setup script automatically patches your OpenClaw config to route all providers through ClawCap:

```bash
node skills/clawcap/scripts/setup.js
```

This will:
- Read your `~/.openclaw/openclaw.json`
- Point every provider's `baseUrl` to your ClawCap proxy URL
- Back up your original config to `~/.openclaw/openclaw.json.backup`

### 3. Done — You're Protected

Start OpenClaw normally. All requests now flow through ClawCap and your spending caps are enforced automatically.

Check your spend anytime:

```bash
curl https://clawcap.co/proxy/$CLAWCAP_TOKEN/status
```

## Manual Setup

If you prefer to configure manually, set every provider's `baseUrl` in `~/.openclaw/openclaw.json` to:

```
https://clawcap.co/proxy/YOUR_TOKEN
```

Your API keys stay the same — ClawCap only reads them to forward requests, never stores them.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAWCAP_TOKEN` | Your ClawCap proxy token (starts with `cc_live_`) |

## Plans

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | $5/day cap, kill switch, heartbeat detection |
| Solo | $5/mo | Custom caps, heartbeat+loop protection, Telegram alerts |
| Pro | $15/mo | Multi-agent tracking, per-model analytics, custom alert thresholds, weekly spend reports |

## Troubleshooting

**Agent not routing through ClawCap:** Check that `baseUrl` in your openclaw.json points to `https://clawcap.co/proxy/cc_live_...` — not the original API URL.

**429 errors:** You've hit your spending cap. Check `/status` to see current spend, or upgrade your plan for higher limits.

**Token not working:** Make sure you're using the full `cc_live_...` token from your setup page, not just the email.

## Links

- [ClawCap Website](https://clawcap.co)
- [Setup Page](https://clawcap.co/setup)
