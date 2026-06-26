# Supported Chains

## Chain Matrix

| Chain | ID | Data API | DeFi API | WebSocket | DEX Protocols |
|-------|----|----------|----------|-----------|---------------|
| Solana | `sol` | Yes | Yes | Yes | Jupiter, Raydium, Orca |
| BSC | `bsc` | Yes | Yes | Yes | PancakeSwap, Kyberswap |
| Ethereum | `eth` | Yes | Yes | Yes | Uniswap, Kyberswap |
| Polygon | `polygon` | — | Bridge only | — | — |
| Arbitrum | `arbitrum` | — | Bridge only | — | — |

## Native Token Addresses

| Chain | Native Token | Address | USDC Address |
|-------|-------------|---------|--------------|
| sol | SOL | `So11111111111111111111111111111111111111112` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| bsc | BNB | `0x0000000000000000000000000000000000000000` | `0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d` |
| eth | ETH | `0x0000000000000000000000000000000000000000` | `0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eB48` |

## Block Explorers

| Chain | Explorer | URL Pattern |
|-------|----------|-------------|
| sol | Solscan | `https://solscan.io/tx/{hash}` |
| bsc | BscScan | `https://bscscan.com/tx/{hash}` |
| eth | Etherscan | `https://etherscan.io/tx/{hash}` |

## Address Formats

| Chain Type | Format | Example |
|-----------|--------|---------|
| Solana | Base58, 32-44 chars | `So11111111111111111111111111111111111111112` |
| EVM (bsc/eth) | `0x` + 40 hex chars | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
