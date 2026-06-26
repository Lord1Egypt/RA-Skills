# ButterSwap 🔄

Execute cross-chain token swaps via ButterSwap with best-route
aggregation. Supports EVM chains (Ethereum, BSC, Base, Arbitrum, Polygon, etc.), Solana,TRON, and Bitcoin. Use when someone wants to swap tokens across different chains and you want to find the optimal route with lowest fees and fastest execution

## Features

- 🔄 **Cross-chain Aggregation** - Optimal swap routing across multiple blockchain liquidity sources
- ⛓️ **Multi-chain Support** - EVM + non-EVM chains
- 🧾 **Quotes + Transaction Data** - Quotes, swap, and approve transaction payloads

## Use Cases

- Cross-chain token swaps
- Bridge tokens across networks
- Get optimal swap routes
- Build cross-chain swap transactions

## Quick Start

### 1. Get Supported Chains

```bash
curl "https://bs-router-v3.chainservice.io/supportedChainInfo"
```

### 2. Find Token Information

```bash
curl "https://bs-router-v3.chainservice.io/findToken?address=0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
```

### 3. Get Swap Route

```bash
curl "https://bs-router-v3.chainservice.io/route?fromChainId=1&toChainId=56&amount=100&tokenInAddress=0xdAC17F958D2ee523a2206206994597C13D831ec7&tokenOutAddress=0x55d398326f99059fF775485246999027B3197955&type=exactIn&slippage=100&entrance=Butter%2B"
```

### 4. Get Swap Transaction

```bash
curl "https://bs-router-v3.chainservice.io/swap?hash=xxx&slippage=100&from=0x123...&receiver=0x456..."
```

## Common Chain IDs

| Chain     | Chain ID |
| --------- | -------- |
| Ethereum  | 1        |
| BSC       | 56       |
| Polygon   | 137      |
| Arbitrum  | 42161    |
| Optimism  | 10       |
| Base      | 8453     |
| Avalanche | 43114    |
| Solana    | 7560     |
| ...       | ...      |

## API Response Format

```json
{
  "errno": 0,
  "message": "success",
  "data": [{ ... }]
}
```

| errno | Meaning                |
| ----- | ---------------------- |
| 0     | Success                |
| 2000  | Parameter error        |
| 2003  | No Route Found         |
| 2004  | Insufficient Liquidity |
| ...   | ...                    |

## Documentation

- [Butter API Docs](https://docs.butternetwork.io/butter-swap-integration/integration-guide)

## License

MIT
