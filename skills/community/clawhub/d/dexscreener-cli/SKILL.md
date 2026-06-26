---
name: dexscreener
description: Query DexScreener API for token prices, market data, trending pools, and memecoin categories. Automatically installs @kilincarslan/dexscreener-cli if not present. Use for trading research, token discovery, liquidity analysis, and market trend monitoring via 13 CLI commands that return structured JSON data.
---

# DexScreener Skill

Query token and market data from DexScreener API. This skill automatically installs and manages the DexScreener CLI tool.

## Auto-Installation

The skill automatically installs `@kilincarslan/dexscreener-cli` if not found:

```bash
which dexscreener || npm install -g @kilincarslan-enterprises/dexscreener-cli
```

## Usage Pattern

When user asks for DexScreener data:

1. **Check/Install:** Ensure CLI is available
2. **Execute:** Run appropriate dexscreener command
3. **Parse:** Process JSON output for the user

## Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `dexscreener search <query>` | Search tokens by symbol/address | `dexscreener search SOL` |
| `dexscreener token <chain>_<addr>` | Token price, mcap, liquidity | `dexscreener token base_0x...` |
| `dexscreener pair <chain>_<addr>` | Pool/pair details | `dexscreener pair base_0x...` |
| `dexscreener token-pairs <chain>_<addr>` | All pairs for token | `dexscreener token-pairs solana_...` |
| `dexscreener pools` | Trending pools | `dexscreener pools` |
| `dexscreener profiles` | Boosted tokens | `dexscreener profiles --type top` |
| `dexscreener recent-updates` | Updated profiles | `dexscreener recent-updates` |
| `dexscreener takeovers` | Community takeovers | `dexscreener takeovers` |
| `dexscreener ads` | Latest ads | `dexscreener ads` |
| `dexscreener orders <chain>_<addr>` | Order book | `dexscreener orders base_0x...` |
| `dexscreener txs <chain>_<pair>` | Transactions | `dexscreener txs base_0x...` |
| `dexscreener metas` | Memecoin trends | `dexscreener metas` |
| `dexscreener meta <slug>` | Category details | `dexscreener meta ai` |

## Output Format

- **JSON** (default) — parse with `jq` or JSON.parse()
- **Table** — human readable (`--format table` or `-f table`)

## Chain Format

`chainId_tokenAddress` — lowercase only:
- `base_0x311935Cd80B76769bF2ecC9D8Ab7635b2139cf82`
- `solana_So11111111111111111111111111111111111111112`
- `ethereum_0x...`

## Common Patterns

### Get token price
```bash
dexscreener token base_0x... | jq -r '.priceUsd'
```

### Search and extract
```bash
dexscreener search SOL | jq '.[0] | {symbol: .baseToken.symbol, price: .priceUsd}'
```

### Find top volume pool
```bash
dexscreener pools | jq 'max_by(.volume.h24) | {pair: .baseToken.symbol, vol24h: .volume.h24}'
```

### Get trending metas
```bash
dexscreener metas | jq '.[].name'
```

## Error Handling

- Exit code 0 = success
- Exit code non-0 = error (check stderr)
- Rate limit: 60 req/min (handled automatically)

## Dependencies

- Node.js 18+
- npm (for global install)

## Repository

https://github.com/Kilincarslan-Enterprises/dexscreener-cli

## NPM Package

https://www.npmjs.com/package/@kilincarslan-enterprises/dexscreener-cli

## License

MIT — Free to use, modify, and distribute