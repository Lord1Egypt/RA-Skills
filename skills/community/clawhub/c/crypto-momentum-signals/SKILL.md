---
name: crypto-momentum-signals
description: "Quantitative momentum signals for any CoinGecko-listed coin in one pay-per-call request: SMA7/SMA25 trend, RSI-14 (Wilder), annualized volatility, 24h/7d/30d change, market cap rank. $0.0005 USDC on Base via x402. No subscription, no API key, no signup."
metadata: { "openclaw": { "emoji": "📈", "requires": { "bins": ["curl"] } } }
---

# Crypto Momentum Signals (x402, pay-per-request)

One-call quantitative momentum read for any CoinGecko coin (bitcoin,
ethereum, solana, arbitrum, dogwifcoin, ...). Use it when a user asks "is
this coin trending?", "what does RSI say?", or before any momentum-based
watchlist screen. Part of the One Dollar Quest agent experiment (public
worklog: https://github.com/perria080925-bot/one-dollar-quest).

## Endpoint

```
BASE = https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010
GET {BASE}/market-signal?coin=<coingecko-id>&vs=<usd|eur|mxn>
Price: $0.0005 USDC per request (x402 v2, EIP-3009, facilitator api.bankr.bot)
```

## Flow

1. `curl -i "{BASE}/market-signal?coin=ethereum&vs=usd"`
2. Expect **HTTP 402** with `X-PAYMENT-REQUIREMENTS` (scheme `exact`, USDC
   on Base `0x8335...2913`).
3. Pay with any x402 client (EIP-3009) and retry with `X-PAYMENT` header.
4. Response JSON: price, market cap + rank, 24h volume, change 24h/7d/30d,
   SMA7/SMA25 trend flag, RSI-14, annualized volatility, data sources +
   disclaimer.

## Signal reference

- **SMA7 vs SMA25**: short trend vs mid trend — `golden` (SMA7 above),
  `dead` (SMA7 below), or `flat`.
- **RSI-14** (Wilder smoothing): <30 oversold, >70 overbought, 45-55 range
  chop.
- **Annualized volatility**: realized vol from daily returns, for position
  sizing context.

## When to use

- Screening many coins for trend + momentum without a paid data feed.
- Adding a quantitative line ("RSI 62, golden trend, vol 45% ann.") to an
  agent's market commentary.
- Combined with `perp-market-regime` (derivatives side) and `evm-pair-scan`
  (on-chain liquidity) for a full pre-trade picture.

## Notes

- Reads public CoinGecko data with server-side quantitative computation; no
  wallet connection, no keys, no account.
- Heuristic analytics, not financial advice. Sources are cited in responses.
