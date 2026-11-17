---
name: defi-stablecoin-yield-scanner
description: Scan live stablecoin yields across every major DeFi protocol and chain — Ethereum, Base, Arbitrum, Optimism, Polygon, Avalanche, and more — using the free DeFiLlama pools API (no API key required). Built for crypto and DeFi users hunting the best USDC, USDT, DAI, and other stablecoin APY without directional trading risk. Filters by minimum TVL to screen out low-liquidity rug risk, filters by APY range to catch unsustainable reward-emission traps, and can scope results to a single chain. Useful for passive income, yield farming, treasury management, and whale-style capital allocation across DeFi protocols like Aave, Pendle, Curve, and Morpho. Complements trading and options skills by covering the non-directional yield side of crypto.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
allowed-tools: Bash
---

# DeFi Stablecoin Yield Scanner

Pulls live pool data from the free DeFiLlama yields API and ranks stablecoin-only pools (USDC, USDT, DAI, sUSDe, crvUSD, and 15+ other pegged assets) by APY, with TVL and impermanent-loss risk shown alongside so you can screen out thin or unsustainable pools before allocating capital.

## When to use

- User wants the best current stablecoin yield across DeFi without directional/price risk
- Comparing yield opportunities across chains (Ethereum vs Base vs Arbitrum vs Avalanche, etc.)
- Screening for TVL floor to avoid low-liquidity or rug-prone pools
- Building or refreshing a passive-income / treasury allocation plan
- Sanity-checking whether an advertised APY is mostly base yield or reward emissions (which can vanish)

## Commands

```bash
python3 scripts/scan_yields.py                              # Top 15 stablecoin pools, TVL >= $1M
python3 scripts/scan_yields.py --min-tvl 10000000 --top 10   # Higher liquidity floor, fewer results
python3 scripts/scan_yields.py --chain Base                  # Scope to one chain
python3 scripts/scan_yields.py --min-apy 8 --max-apy 40      # Filter out noise and outliers/broken pools
python3 scripts/scan_yields.py --json                        # Raw JSON (includes apy_base vs apy_reward split)
```

## Output

A ranked table: project, chain, pool symbol, APY %, TVL in USD, and impermanent-loss risk flag. The `--json` mode additionally splits `apy_base` (organic yield) from `apy_reward` (token emissions), which is the key number to check before parking real capital — emission-heavy APY tends to decay fast as reward tokens get sold.

## Notes

- Data source: https://yields.llama.fi (DeFiLlama), refreshed continuously, no API key or rate-limit issues for reasonable use.
- This is a read-only scanner. It does not execute trades, approve contracts, or move funds — always verify a pool's contract and audit history independently before depositing.
- Not financial advice.
