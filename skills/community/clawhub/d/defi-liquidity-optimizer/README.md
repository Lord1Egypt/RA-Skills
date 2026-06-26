# DeFi Liquidity Optimizer Skill

Automated liquidity provision analysis and optimization for concentrated liquidity market makers (CLMM) across Solana (Meteora, Raydium) and Ethereum (Uniswap V4).

## Features

- **Pool Comparison** - Compare APR, TVL, and fee efficiency across protocols
- **Impermanent Loss Calculator** - Estimate IL for various price scenarios
- **Rebalancing Recommendations** - Detect out-of-range positions
- **Risk Scoring** - TVL-based safety scores for pool selection
- **Python 3.9+ Compatible** - Zero external dependencies

## Usage

```bash
# Compare pools
python scripts/liquidity_optimizer.py compare

# Show rankings
python scripts/liquidity_optimizer.py rank

# Calculate IL for price change
python scripts/liquidity_optimizer.py il 1.5
```

## Use Cases

- Find best APR across DeFi protocols for liquidity provision
- Calculate impermanent loss risk for proposed positions
- Monitor active LP positions and get rebalancing alerts
- Compare fee efficiency between pools
- Generate risk-adjusted yield recommendations