# Cross-Exchange Arbitrage Scanner

A keyless Python script that checks live public prices for a crypto symbol
across five major spot exchanges (Coinbase, Kraken, Bitstamp, Gemini, OKX)
and tells you whether there's currently a "crossed market" — meaning the
best bid on one exchange is higher than the best ask on another, the raw
condition for a cross-exchange arbitrage trade.

## Why this exists

Most arbitrage-scanner skills on ClawHub focus on funding-rate arbitrage
(perp vs. perp basis) or single-exchange strategy. There wasn't a simple,
no-API-key tool that just answers "is there a live spot price gap between
major exchanges right now, and how big is it in basis points?" This fills
that gap.

## Quick start

```bash
cd scripts
python3 arb_scanner.py BTC ETH SOL
```

Example output:
```
=== BTC ===
  bitstamp    bid=64739.8800     ask=64739.8900
  coinbase    bid=64734.9600     ask=64734.9700
  gemini      bid=64742.5000     ask=64742.5100
  kraken      bid=64730.8000     ask=64730.9000
  okx         bid=64786.6000     ask=64786.7000
  >> ARB: buy BTC on kraken @ 64730.9000, sell on okx @ 64786.6000 = 8.6 bps gross (before fees/withdrawal)
```

## What it does NOT do

- Does not place trades — detection/reporting only.
- Does not account for trading fees, withdrawal fees, or transfer time.
- Does not check order book depth — only top-of-book bid/ask.

For a persistent monitor, schedule this script on an interval and pipe
`--json` output into your own alerting/execution logic.
