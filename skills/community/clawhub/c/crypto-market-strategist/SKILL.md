---
name: crypto-market-strategist
description: Analyze one BTC or ETH derivatives setup using current public Deribit, Hyperliquid, and Polymarket data. Use for read-only strategy research, volatility, options skew, funding, basis, support and resistance, prediction-market context, or regime classification. Never execute trades or claim certainty.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "📊"
---

# Crypto Market Strategist

Analyze exactly one asset, BTC or ETH. Ask which asset if the user names
neither. Start every delivered analysis with `Not investment advice.`

## First use

The skill uses public, keyless endpoints and never connects to an exchange
account. Before installing the Python dependency, explain the command and ask
for confirmation:

```bash
python3 -m pip install -r <skill-directory>/requirements.txt
```

## Complete analysis

After the user selects BTC or ETH, run:

```bash
python3 <skill-directory>/scripts/cli_analyze.py BTC
```

Replace `BTC` with `ETH` when requested. The command saves complete source
observations locally and prints fitted evidence plus all deterministic strategy
rankings as JSON.

Use the returned `score` only as setup fit, never as a win rate or expected
return. Review source availability and timestamps, volatility-surface fit
warnings, implied versus realized volatility, futures basis, funding, trend,
price levels, prediction-market rules, and agreement between independent
sources.

Choose one best-fit strategy and show:

- data timestamp and any unavailable sources;
- market regime and regime confidence;
- material volatility, skew, carry, trend, and level evidence;
- selected strategy with its unchanged setup-fit score;
- entry conditions, invalidation, alternatives, and reassessment trigger;
- evidence identifiers from the JSON.

Do not invent an exact option instrument, expiry, strike, size, leverage,
probability of profit, payoff ratio, or expected return. Never place orders,
request API credentials, or imply a profit guarantee.
