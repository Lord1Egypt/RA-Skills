# Crypto Supply Dilution Tracker

A small, dependency-free Python tool that flags crypto tokens with
high future supply dilution risk, using CoinGecko's free public API.

## Why

Market cap alone hides a lot. Two tokens can have the same market cap
today, but if one has already released 95% of its total supply and
the other has only released 20%, the second one has far more future
sell pressure baked in as the rest of its supply unlocks or gets
mined. This tool surfaces that gap in seconds.

## Install / requirements

Python 3.8+, standard library only (`urllib`, `json`, `argparse`). No
pip installs, no API key, no signup.

## Quick start

```bash
python3 scripts/dilution_tracker.py bitcoin ethereum solana
```

Scan the top 25 coins by market cap instead of naming them:

```bash
python3 scripts/dilution_tracker.py --top 25
```

Get machine-readable output:

```bash
python3 scripts/dilution_tracker.py --ids bitcoin,ethereum --json
```

## How the score works

```
dilution_score = (eventual_supply - circulating_supply) / circulating_supply
```

`eventual_supply` is the coin's `max_supply` if it has one, otherwise
its `total_supply`. A score of 0 means fully diluted (no more supply
coming); a score of 1.0 means the amount of supply still to be
released equals what's already circulating (100% more dilution ahead).

| Score range | Label |
|---|---|
| 0 | FULLY DILUTED |
| 0 – 0.25 | LOW DILUTION |
| 0.25 – 1.0 | MODERATE DILUTION |
| ≥ 1.0 | HIGH DILUTION RISK |
| no supply cap of any kind reported | UNCAPPED |

## Limitations

CoinGecko's free tier has rate limits (roughly 10-30 calls/minute
depending on load) — this tool makes one call per invocation
regardless of how many coins you list, so normal usage won't hit it.
It cannot see project-specific vesting cliffs; it only reflects
supply numbers CoinGecko publishes.
