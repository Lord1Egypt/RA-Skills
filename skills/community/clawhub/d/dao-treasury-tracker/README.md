# DAO Treasury Tracker

A small, dependency-free Python tool that scores DAO treasury
concentration risk using DeFiLlama's free public treasury API.

## Why

"$1B treasury" means very different things depending on what's in it.
A treasury that's 95% the DAO's own governance token is fragile — a
token crash wipes out real spending power. A treasury with a large
stablecoin/ETH allocation can actually fund grants, audits, and
operations through a bear market. This tool computes that split
directly from on-chain-sourced data instead of requiring manual
dashboard reading.

## Install / requirements

Python 3.8+, standard library only (`urllib`, `json`, `argparse`). No
pip installs, no API key, no signup.

## Quick start

```bash
python3 scripts/treasury_tracker.py uniswap lido aave ens gitcoin
```

Get machine-readable output for one protocol:

```bash
python3 scripts/treasury_tracker.py --json uniswap
```

Not sure of a protocol's slug? List some known slugs:

```bash
python3 scripts/treasury_tracker.py --list-protocols
```

## How the score works

DeFiLlama's `currentChainTvls` breaks a treasury into per-chain
non-token assets (e.g. `"Ethereum": 1704`) and a chain-agnostic
`"OwnTokens"` total for the project's own governance token holdings.
This tool sums the two to get total treasury value, then computes:

```
own_token_pct = own_token_usd / total_treasury_usd * 100
```

| own_token_pct | Label |
|---|---|
| < 40% | DIVERSIFIED |
| 40% – 70% | MODERATE CONCENTRATION |
| ≥ 70% | TOKEN-CONCENTRATED (high risk) |

## Limitations

Only covers protocols DeFiLlama tracks a treasury module for — many
smaller or newer DAOs aren't included and will show up as a skipped
error rather than a result. This is a balance-sheet snapshot, not a
runway or spending-rate projection.
