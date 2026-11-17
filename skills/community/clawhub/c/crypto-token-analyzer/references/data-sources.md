# Data Sources & Endpoints

## DexScreener (primary market data)

`https://api.dexscreener.com`

``` 
GET /latest/dex/tokens/{tokenAddress}
```
```bash
curl -s "https://api.dexscreener.com/latest/dex/tokens/0x..."
```

```
GET /token-pairs/v1/{chainId}/{tokenAddress}
```
ethereum, bsc, solana, base, arbitrum, polygon, avalanche

```
GET /latest/dex/pairs/{chainId}/{pairAddress}
```
```
GET /latest/dex/search?q={query}
```

- `pairs[].priceUsd`
- `pairs[].priceChange.m5` / `h1` / `h6` / `h24`
- `pairs[].volume.h24` (also m5/h1/h6)
- `pairs[].liquidity.usd`
- `pairs[].fdv` / `marketCap`
- `pairs[].txns.h24.buys` / `sells`
- `pairs[].pairCreatedAt` (unix ms)
- `pairs[].labels`
- `pairs[].info` (imageUrl, websites, socials)
- `pairs[].boosts.active`

Prefer the pair with highest `liquidity.usd` on the requested chain.

Web fallback (for charts / visual K-line):
- `https://dexscreener.com/{chain}/{tokenAddress}`
- `https://www.geckoterminal.com/{chain}/tokens/{tokenAddress}`

## GoPlus Token Security

```
GET //api.gopluslabs.io/api/v1/token_security/{chain_id}?contract_addresses={address}
```
No key required for public free tier (rate limited).

### GoPlus chain_id mapping

| Chain | chain_id |
|-------|----------|
| ethereum | 1 |
| bsc | 56 |
| polygon | 137 |
| arbitrum | 42161 |
| avalanche | 43114 |
| base | 8453 |
| optimism | 10 |
| fantom | 250 |

Solana support is limited / different — fall back to other tools or note the gap.

## Block Explorers (supplement)

- https://etherscan.io/token/{address}
- https://bscscan.com/token/{address}
- https://basescan.org/token/{address}
- https://arbiscan.io/token/{address}
- https://polygonscan.com/token/{address}
- https://snowtrace.io/token/{address}
- https://solscan.io/token/{address}
- https://birdeye.so/token/{address}?chain=solana

Use browser tools or open_page when you need holder distribution, contract source verification status, or recent large transfers.