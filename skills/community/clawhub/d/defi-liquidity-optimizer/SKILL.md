---
name: defi-liquidity-optimizer
description: |
  Automated liquidity provision optimizer for CLMM DEXs on Solana and Ethereum.
  Analyzes pools on Meteora, Raydium, and Uniswap V4 to compare APR yields, calculate
  impermanent loss risk across price scenarios, score pool safety by TVL, and
  generate rebalancing recommendations for out-of-range positions.

  Commands:
  - liquidity_optimizer.py compare   Full pool comparison report
  - liquidity_optimizer.py rank     APR rankings only
  - liquidity_optimizer.py il 1.5   Calculate IL for 1.5x price change

  Python 3.9+, zero external dependencies. Uses built-in math for IL calculation.
  In production, connect to Hummingbot Gateway or pool APIs for live data.

  Pool analysis includes TVL score (safety), fee efficiency, 24h volume, and APR.
  IL scenarios show impact at ±10%, ±25%, ±50%, ±100% price changes.
  Rebalancing alerts trigger when current price exits configured tick range.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
allowed-tools: Bash, Read
---

# DeFi Liquidity Optimizer

Analyzes concentrated liquidity pools across Solana and Ethereum to find optimal LP positions and monitor existing positions for rebalancing needs.

## Pool Analysis Features

- **APR Comparison** - Ranks pools by annual percentage yield
- **TVL Safety Scores** - Higher TVL = lower IL risk and more stable fees
- **Fee Efficiency** - Fees earned relative to trading volume
- **Impermanent Loss Calculator** - Shows impact at multiple price scenarios
- **Rebalancing Alerts** - Detects when positions fall out of range

## Usage

```bash
# Full comparison report
python scripts/liquidity_optimizer.py compare

# APR rankings only
python scripts/liquidity_optimizer.py rank

# IL calculation for specific price change
python scripts/liquidity_optimizer.py il 1.5   # 1.5x = 50% increase
python scripts/liquidity_optimizer.py il 0.75  # 0.75x = 25% decrease
```

## Understanding the Output

The comparison report shows each pool with:
- APR and daily fee earnings on a $1000 investment
- TVL-based safety score (1-5 stars)
- Fee efficiency percentage
- IL scenarios for different price changes

## Production Integration

For live pool data, connect to:
- Meteora DLMM API for Solana pools
- Raydium API for Solana pools
- Hummingbot Gateway for Ethereum Uniswap V4

The current script uses mock data structure that maps to real API responses.