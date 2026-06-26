---
name: defi-research
version: 1.0.1
description: Research any token, check DEX liquidity, and get live gas prices. Built for flash loan traders and DeFi agents.
tags: defi, crypto, tokens, blockchain, trading
---

# DeFi Research API

Research tokens, check DEX liquidity, and get gas prices. Built for DeFi traders and flash loan agents.

## Payment Options

**Option A — Stripe Credits:** $10 = 100 credits at /buy. Send api_key with each request.

**Option B — Pay-per-call with USDC:** No account needed. Send exact USDC on Base to 0xC9D03C8Af4Bd51e0aDc9fc885AB227cbe6B649F5, then retry with tx_hash.

## Endpoints

### Token Price
Cost: 1 credit or $0.05 USDC. Returns current USD price, 24h change, and market cap.

POST /api/defi/price
{"api_key": "your_key", "token": "ethereum"}

Or pay with crypto:
POST /api/crypto/price
{"token": "ethereum"}
→ Returns 402 with payment details. Pay and retry with:
POST /api/crypto/price
{"token": "ethereum", "tx_hash": "0x..."}

### Deep Token Research
Cost: 3 credits or $0.15 USDC. Full research: price, rank, description, categories, links.

POST /api/defi/research
{"api_key": "your_key", "token": "bitcoin"}

Or pay with crypto:
POST /api/crypto/research
{"token": "bitcoin"}
→ 402 → pay → retry with tx_hash

### DEX Liquidity Check
Cost: 2 credits or $0.10 USDC. Find which DEX has the best liquidity.

POST /api/defi/liquidity
{"api_key": "your_key", "token": "USDC"}

Or pay with crypto:
POST /api/crypto/liquidity
{"token": "USDC"}

### Gas Prices (free)
Current Ethereum gas prices (slow/average/fast).

GET /api/defi/gas

## Requirements

Works with any web-connected OpenClaw agent with crypto wallet support.
