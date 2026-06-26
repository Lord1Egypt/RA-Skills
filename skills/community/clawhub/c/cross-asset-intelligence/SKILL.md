---
name: cross-asset-intelligence
version: 1.0.2
description: "Cross-asset financial analysis API combining crypto and traditional markets. BTC vs S&P500/NASDAQ/Nikkei225/DAX correlation, cross-market risk score (0-100), crypto news impact analysis, macroeconomic environment report, token contract risk evaluation, daily market briefing. Pay-per-request with USDC micropayments via x402 on Base. No API key needed. Use when asked to 'check BTC correlation with stocks', 'what is the market risk level', 'is this token safe', 'crypto market analysis', 'macro outlook', 'morning market briefing', 'cross-asset analysis', 'BTC vs equities', 'risk score', 'token safety check', 'evaluate contract risk for address', 'daily market update', 'market sentiment', 'portfolio risk', 'VIX and crypto', 'correlation between bitcoin and stock market', 'financial analysis for trading', 'hedge fund briefing', 'institutional market report'. Bilingual: English and Japanese. Powered by Claude AI (Haiku/Sonnet/Opus). Data from CoinGecko, FRED, Twelve Data, RSS feeds. 4 pricing tiers: quick ($0.001, no AI, sub-second), insight ($0.03-0.15, Claude Haiku), analysis ($0.08-0.20, Claude Sonnet), pro ($0.80-1.00, Claude Opus institutional-grade)."
author: suga_crypto
license: MIT
tags:
  - crypto
  - finance
  - trading
  - market-analysis
  - risk
  - correlation
  - macro
  - token-safety
  - x402
  - micropayments
  - cross-asset
  - btc
  - defi
  - market-research
---

# Cross-Asset Intelligence API

AI-powered cross-market financial analysis. Crypto + traditional finance in one API.

## What This Skill Does

Connects your agent to 22 paid analysis endpoints spanning 6 domains:

1. **BTC-Equity Correlation** — Pearson correlation between BTC and stock indices
2. **Cross-Market Risk Score** — Composite 0-100 score from BTC volatility, VIX, bonds, macro
3. **Crypto News Impact** — Top 3 market-moving stories ranked by impact
4. **Macro Environment** — Fed rate, CPI, unemployment, GDP, yields with AI analysis
5. **Token Safety** — SAFE/CAUTION/DANGER verdict for any ERC-20 contract
6. **Daily Briefing** — All-in-one cross-asset market snapshot

## Payment

All endpoints use x402 micropayments (USDC on Base). Your agent's wallet pays automatically per request. No API key, no subscription, no signup.

| Tier | Price Range | AI Model | Speed |
|------|------------|----------|-------|
| quick | $0.001-0.002 | None (pure math) | <500ms |
| insight | $0.03-0.06 | Claude Haiku | <5s |
| analysis | $0.08-0.20 | Claude Sonnet | <10s |
| pro | $0.80-1.00 | Claude Opus | cached 2h |

## Setup

Your agent needs a funded wallet (USDC on Base). Set your wallet's private key as an environment variable:

- **Variable name:** `WALLET_SIGNING_KEY`
- **Format:** hex (32-byte private key)
- **Recommended:** Use a dedicated agent wallet with limited funds — not your main wallet

Store the value in `.env` (gitignored) or a secret manager. Never share or commit it.

## Usage

All endpoints are accessible via HTTP GET through Bankr x402 Cloud:

```
Base URL: https://x402.bankr.bot/0x98ee945dfa6bb8e9ed9f9b6ae56eb82bcc82f0aa/
```

### Quick examples

```bash
# BTC vs S&P500 correlation (30 days)
GET /correlation-quick?index=sp500&period_days=30

# Cross-market risk score
GET /risk-score-quick

# Token safety check
GET /token-safety-quick?chain=ethereum&address=0x...

# Daily market briefing
GET /daily-briefing-quick

# With AI analysis (Claude Sonnet)
GET /correlation-analysis?index=nasdaq&period_days=90&lang=ja
```

### Available endpoints

**Correlation:** `correlation-quick`, `correlation-insight`, `correlation-analysis`, `correlation-pro`
- Params: `index` (sp500/nasdaq/nikkei225/dax), `period_days` (7/14/30/90), `lang` (en/ja)

**Risk Score:** `risk-score-quick`, `risk-score-insight`, `risk-score-analysis`, `risk-score-pro`
- Params: `lang` (en/ja)

**Top News:** `top-news-insight`, `top-news-analysis`, `top-news-pro`
- Params: `lang` (en/ja)

**Macro Report:** `macro-report-insight`, `macro-report-analysis`, `macro-report-pro`
- Params: `lang` (en/ja)

**Token Safety:** `token-safety-quick`, `token-safety-insight`, `token-safety-analysis`, `token-safety-pro`
- Params: `chain` (ethereum/base/etc), `address` (contract address), `lang` (en/ja)

**Daily Briefing:** `daily-briefing-quick`, `daily-briefing-insight`, `daily-briefing-analysis`, `daily-briefing-pro`
- Params: `lang` (en/ja)

## Response Format

All responses include:
- Core analysis data (correlation coefficients, risk scores, news items, etc.)
- `upgrade_available` — links to higher-tier analysis with pricing
- `meta.data_sources` — transparency on where data comes from
- `meta.data_freshness` — timestamp of underlying data
- `disclaimer` — not financial advice

## Why This Over Raw Data APIs

- **Cross-asset analysis** — BTC vs stock indices, not just crypto or just stocks
- **AI judgment included** — not raw numbers, but interpreted analysis
- **4 pricing tiers** — from $0.001 machine-readable data to $0.80 institutional reports
- **x402 native** — no API key dance, just pay and get data
- **Bilingual** — English and Japanese output

## Differentiators

- Only x402 API offering crypto × traditional finance cross-asset AI analysis
- Historical data analysis capabilities expanding
- Claude Opus institutional-grade reports at pro tier
- Sub-second quick tier for automated monitoring and alerts

## Security & Privacy

This skill contains no executable code. It is a pure markdown description of an external API. All data processing happens server-side on secured infrastructure. No local files are read, written, or executed.
