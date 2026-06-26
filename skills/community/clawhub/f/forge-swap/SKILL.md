---
name: forge
description: Cross-chain swap routing via THORChain. Get quotes and build swap transactions across 44+ assets (BTC, ETH, RUNE, AVAX, USDC and more). Non-custodial — returns vault address and memo, user's wallet executes. 0.5% affiliate fee to forgemb on every routed swap.
version: 0.1.0
author: MoreBetter Studios
homepage: https://morebetterstudios.com
repository: https://github.com/morebetterclaw/forge
api: https://forge-api-production-50de.up.railway.app
mcp: https://forge-api-production-50de.up.railway.app/mcp
tags:
  - crypto
  - defi
  - thorchain
  - swap
  - cross-chain
  - bitcoin
  - ethereum
  - rune
---

# FORGE — Cross-Chain Swap Agent

Non-custodial cross-chain swaps powered by THORChain. Routes quotes across 44+ assets via the THORNode API directly. Every swap embeds a 0.5% affiliate fee to `forgemb` — protocol-native, trustless, settled in RUNE.

## Live API

```
Base:      https://forge-api-production-50de.up.railway.app
MCP:       https://forge-api-production-50de.up.railway.app/mcp
Discovery: https://forge-api-production-50de.up.railway.app/.well-known/mcp.json
```

## MCP Tools (Claude Desktop / Cursor / any MCP client)

```json
{
  "mcpServers": {
    "forge": {
      "url": "https://forge-api-production-50de.up.railway.app/mcp",
      "transport": "streamable-http"
    }
  }
}
```

**Tools:** `forge_quote` · `forge_execute` · `forge_assets` · `forge_status`

## REST API

```bash
# Get a quote
curl -X POST https://forge-api-production-50de.up.railway.app/swap/quote \
  -H "Content-Type: application/json" \
  -d '{"fromAsset":"ETH.ETH","toAsset":"BTC.BTC","amount":"0.1"}'

# Build swap transaction (returns vault address + memo — no funds sent)
curl -X POST https://forge-api-production-50de.up.railway.app/swap/execute \
  -H "Content-Type: application/json" \
  -d '{"fromAsset":"ETH.ETH","toAsset":"THOR.RUNE","amount":"0.05","destinationAddress":"thor1..."}'

# List supported assets
curl https://forge-api-production-50de.up.railway.app/swap/assets
```

## How It Works

1. Call `/swap/execute` with from/to asset and destination address
2. FORGE returns a **vault deposit address** and **THORChain memo**
3. User's wallet sends funds to vault address with memo as calldata
4. THORChain protocol routes the swap — FORGE never holds funds
5. `forgemb` earns 0.5% affiliate fee embedded in the memo, settled natively

## Asset Format

Assets use `CHAIN.TICKER` format:
- `ETH.ETH` — Ethereum native
- `BTC.BTC` — Bitcoin
- `THOR.RUNE` — THORChain native
- `AVAX.AVAX` — Avalanche native
- `ETH.USDC-0xA0b86...` — ERC-20 tokens include contract address

## Environment Variables (self-hosted)

```bash
FEE_RECIPIENT_ADDRESS=forgemb   # THORName or thor1... address for affiliate fees
SWAP_FEE_BPS=50                 # 50 = 0.5%
PORT=3000
ALLOWED_ORIGINS=*
```

## Revenue Model

Every swap routed through FORGE earns 0.5% to `forgemb` (THORChain name for `thor1yfrfgjgnzkjqqgv02yxn3j3kv50pe0rnhvs8zw`). Fees are embedded in the THORChain memo and settled by the protocol — no invoicing, no off-chain reconciliation.
