---
name: b402-private-defi
version: 0.4.2
description: >
  Private DeFi for AI agents. Shield tokens into a Railgun ZK privacy pool, swap privately,
  lend into Morpho vaults for yield, and bridge cross-chain via LI.FI — all gasless and
  untraceable. Supports Base, Arbitrum, BSC.
author: b402ai
homepage: https://github.com/b402-ai/b402-sdk
metadata:
  openclaw:
    requires:
      env: [WORKER_PRIVATE_KEY]
      bins: [node, npx]
    primaryEnv: WORKER_PRIVATE_KEY
    install:
      - kind: node
        package: b402-mcp
        bins: [b402-mcp]
    emoji: "\U0001F510"
    homepage: https://github.com/b402-ai/b402-sdk
---

# b402 — Private DeFi for AI Agents

**Shield. Swap. Lend. Bridge. All private. All gasless.**

b402 wraps Railgun's ZK privacy pool with an agent-friendly SDK and MCP server.
On-chain observers see "RelayAdapt called a DEX" — not your wallet, not your strategy.

## Install

```bash
npx b402-mcp@latest --claude
```

This generates a wallet at `~/.b402/wallet.json`, patches your Claude Desktop config, and registers the MCP server. Fund the wallet with USDC on Base to start.

## Tools

| Tool | What it does |
|---|---|
| `check_pool_balance` | Show shielded balances, wallet state, vault positions |
| `shield_usdc` | Move USDC into the Railgun privacy pool (gasless) |
| `private_swap` | Swap tokens inside the pool via ZK proof (USDC↔WETH, etc.) |
| `lend_privately` | Deposit into Morpho vault from pool (~4-8% APY) |
| `redeem_privately` | Withdraw from Morpho vault back to pool |
| `cross_chain_privately` | Private cross-chain transfer or swap via LI.FI (Base→Arb, etc.) |
| `get_swap_quote` | Preview swap rates without executing |
| `run_strategy` | Multi-step: swap + lend + reserve in one call |

## Example prompts

- "Check my privacy pool balance"
- "Shield 5 USDC into the pool"
- "Swap 2 USDC to WETH privately"
- "Privately send 1 USDC to 0xABC... on Arbitrum"
- "Private cross-chain swap: 1 USDC from pool to ARB on Arbitrum, to 0xABC..."
- "Lend 10 USDC in the steakhouse vault"
- "Run a yield strategy: 30% WETH, 50% lend, 20% reserve"

## How it works

```
Agent prompt → MCP tool call → b402-sdk
  → Railgun ZK proof (client-side, 10-30s)
  → RelayAdapt atomic tx (unshield → DeFi op → reshield)
  → On-chain: only RelayAdapt visible. No wallet linked.
```

Cross-chain: LI.FI routes through ~30 bridges + ~20 DEXes. Source and destination are unlinkable.

## Supported chains

| Chain | ID | Privacy pool | Cross-chain |
|---|---|---|---|
| Base | 8453 | Yes (0% fee) | Source + dest |
| Arbitrum | 42161 | Yes (0% fee) | Dest only (v1) |
| BSC | 56 | Yes (0% fee) | Dest only (v1) |

## SDK usage (for builders)

```typescript
import { B402 } from '@b402ai/sdk'

const b402 = new B402({ privateKey: process.env.WORKER_PRIVATE_KEY! })

// Shield into privacy pool (gasless)
await b402.shieldFromEOA({ token: 'USDC', amount: '10' })

// Private swap inside pool
await b402.privateSwap({ from: 'USDC', to: 'WETH', amount: '5' })

// Private cross-chain (LI.FI routing)
await b402.privateCrossChain({
  toChain: 'arbitrum',
  fromToken: 'USDC',
  toToken: 'ARB',
  amount: '1',
  destinationAddress: '0x...',
})

// Private lend (Morpho vaults, 4-8% APY)
await b402.privateLend({ amount: '10', vault: 'steakhouse' })
```

## Links

- SDK: [npmjs.com/package/@b402ai/sdk](https://npmjs.com/package/@b402ai/sdk)
- MCP: [npmjs.com/package/b402-mcp](https://npmjs.com/package/b402-mcp)
- Starter: [github.com/b402-ai/b402-starter](https://github.com/b402-ai/b402-starter)
- Agent template: [github.com/b402-ai/b402-agent-starter](https://github.com/b402-ai/b402-agent-starter)
