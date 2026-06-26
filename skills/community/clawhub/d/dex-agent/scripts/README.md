# DEX Agent — Direct DeFi Trading for OpenClaw

**Bankr alternative. Zero middleman fees. Direct DEX swaps on Base.**

## Why DEX Agent?

| Feature | Bankr | DEX Agent |
|---------|-------|-----------|
| Swap fee | 0.65% | 0% (just gas) |
| Stop-loss | Paid only | Free |
| Take-profit | Paid only | Free |
| Price quotes | ✅ | ✅ |
| Speed | ~20s | ~3s |
| Custody | They hold keys | You hold keys |
| Open source | ❌ | ✅ |

## Quick Start

```bash
# Generate a wallet
python3 agent.py wallet generate

# Fund it (send ETH for gas + USDC for trading to the printed address)

# Check prices
python3 agent.py price WETH
python3 agent.py price BRETT

# Get quotes
python3 agent.py quote USDC WETH 10.0

# Execute a swap
python3 agent.py swap USDC WETH 5.0

# Set stop-loss (8% below entry)
python3 agent.py stop WETH 2000 8.0 0.005

# Set take-profit (5% above entry)
python3 agent.py tp WETH 2000 5.0 0.005

# Monitor orders
python3 agent.py monitor
```

## Architecture

- **wallet.py** — Self-custodial wallet generation and management
- **swap.py** — Direct Uniswap V3 swap engine with slippage protection
- **price_monitor.py** — Real-time price feeds + stop-loss/take-profit orders
- **rpc.py** — Multi-RPC failover with rate limiting
- **agent.py** — Unified CLI interface
- **config.py** — Base chain contract addresses and parameters

## Supported DEXes

- Uniswap V3 (SwapRouter02)
- Aerodrome (coming soon)

## Supported Tokens

WETH, USDC, USDbC, AERO, BRETT, DEGEN — easily extensible.

## Built by @ElwayOnBase
