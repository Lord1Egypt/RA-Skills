---
name: derek-bitcoin-intel
description: The only Bitcoin intelligence agent that pays for its own data with sats. Serves live price, Fear & Greed, mempool fees, ETF flows, on-chain metrics, and prediction market odds — all over Lightning (L402). No API keys, no subscriptions, no middlemen. Open source, VirusTotal clean, built by a real operator running mainnet Lightning.
---

# Derek Bitcoin Intelligence API

Bitcoin market intelligence that pays for itself — delivered over Lightning.

## What This Is

Derek is an autonomous Bitcoin intelligence agent. He monitors markets, curates non-obvious news, tracks on-chain activity, and serves it all as a paid API over the L402 protocol.

No API keys. No subscriptions. No accounts. Just sats for signal.

## What Makes This Different

Derek doesn't just wrap free APIs. He runs his own Lightning node and pays for premium data sources with micropayments — then distills that into intelligence you can query on demand. The L402 protocol means your agent pays a Lightning invoice and gets data back. One round trip. Done.

Built by a real operator running mainnet Lightning. Open source. VirusTotal clean.

## What You Get

### /api/health — Free
Service status, available endpoints, and pricing. Hit this first.

### /api/market-brief — 100 sats
Updated every 1-4 hours. Returns:
- Current BTC price and 24h change
- Fear & Greed index
- Mempool fee rates
- ETF flow data
- On-chain metrics (SOPR, MVRV Z-Score, exchange flows)
- Prediction market odds on Bitcoin-material events
- Curated news coverage — non-obvious Bitcoin stories, not recycled headlines
- Breaking alert state

### /api/latest-alert — 50 sats
Updated every 15 minutes. Returns the most recent breaking alert — triggered by significant price moves (>5%) or major events (exchange hacks, regulatory shifts, ETF decisions).

## Requirements

- `lnget` installed ([github.com/lightninglabs/lnget](https://github.com/lightninglabs/lnget))
- A configured Lightning node (LND) with a funded channel
- Tor access for reaching the .onion endpoint

## Usage

```bash
# Check service status (free)
lnget http://jnfaphddbeubdgpsbrw4d2z6wjew57djdzyrzkbt2ta7bi3wfzmfsfyd.onion/api/health

# Get market brief (100 sats)
lnget -q http://jnfaphddbeubdgpsbrw4d2z6wjew57djdzyrzkbt2ta7bi3wfzmfsfyd.onion/api/market-brief

# Get latest alert (50 sats)
lnget -q http://jnfaphddbeubdgpsbrw4d2z6wjew57djdzyrzkbt2ta7bi3wfzmfsfyd.onion/api/latest-alert
```

## Pricing

| Endpoint | Cost | Update Frequency |
|----------|------|-----------------|
| /api/health | Free | Real-time |
| /api/market-brief | 100 sats | Every 1-4 hours |
| /api/latest-alert | 50 sats | Every 15 minutes |

## About

Derek is an autonomous Bitcoin intelligence agent built on LND, Aperture (L402 reverse proxy), and a Tor hidden service. He runs 24/7, monitors markets and on-chain activity, and serves curated analysis to any agent that can pay a Lightning invoice. Built for the agent economy — where machines pay machines for signal.
