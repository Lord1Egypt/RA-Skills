---
name: cross-exchange-arb-scanner
description: Scans live public spot tickers across Coinbase, Kraken, Bitstamp, Gemini, and OKX (no API key required) to detect cross-exchange crypto arbitrage opportunities, price discrepancies, and crossed markets for BTC, ETH, SOL, and other listed tokens. Use this when the user asks about crypto arbitrage, cross exchange arbitrage, cex arbitrage scanner, price spread between exchanges, buy low sell high across crypto exchanges, spot arbitrage bot, exchange price discrepancy, best bid ask across venues, or wants to check if an arbitrage opportunity currently exists between major spot exchanges. Reports spread in basis points and which venue to buy/sell on, but does not account for withdrawal time, network fees, or trading fees, so results are gross spreads only.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
---

# Cross-Exchange Arbitrage Scanner

Pulls live public bid/ask quotes from five spot exchanges (Coinbase, Kraken,
Bitstamp, Gemini, OKX) with zero API keys required, then flags any symbol
where the best bid on one exchange exceeds the best ask on another — a
crossed market, which is the raw signal for cross-exchange arbitrage.

## When to use this

- The user wants to know if there's a live arbitrage opportunity between
  major crypto spot exchanges right now.
- The user is comparing prices for a coin across venues before placing an
  order.
- The user wants a quick, keyless way to monitor spread/dislocation between
  exchanges for a watchlist of symbols.

## How to run it

```bash
python3 scripts/arb_scanner.py BTC ETH SOL
python3 scripts/arb_scanner.py --min-spread-bps 15 BTC ETH
python3 scripts/arb_scanner.py --json BTC
```

- `symbols`: one or more base symbols (e.g. `BTC`, `ETH`, `SOL`). All quotes
  are fetched in USD terms.
- `--min-spread-bps`: only surface arbitrage opportunities at or above this
  threshold (basis points). Useful for filtering noise below realistic fee
  costs.
- `--json`: emit machine-readable output instead of the formatted report.

## Important limitations (be upfront with the user about these)

- **Gross spread only.** The reported spread does not subtract trading fees,
  withdrawal fees, or network transfer time. A move from exchange A to B
  can take minutes and eat the entire edge. Treat any result under ~20-30
  bps as likely unprofitable after real-world costs.
- **Top-of-book only, not depth.** The scanner compares the best bid/ask,
  not the size available at that price. A large order will walk the book
  and the realized price will be worse than quoted.
- **Binance is excluded** — its public REST API blocks many cloud/server IP
  ranges (451-style geo/infra restriction), so it can't be reliably polled
  from a hosted environment.
- Not every exchange lists every symbol; those are skipped silently and
  noted in the per-symbol quote table.
- This is a point-in-time scanner, not a persistent bot. For continuous
  monitoring, wrap it in a cron/automation loop and add your own execution
  logic — this skill only detects and reports, it does not place trades.

See `references/notes.md` for exchange-specific quirks and `README.md` for
a plain-language overview.
