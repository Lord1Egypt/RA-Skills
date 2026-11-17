# DEX Batch Distribution

Batch-distribute ERC-20 tokens or ETH to up to 200 recipients in a single transaction through DEX hook integrations, powered by Spraay Protocol.

## What this does

Spraay is **push-based** distribution. Instead of recipients claiming rewards from a farm or merkle tree, the sender chooses recipients off-chain and delivers to all of them in one transaction. No claim step, no unclaimed dust.

This skill covers the `@spraay/dex-adapters` npm package, which provides adapters for batch distribution through four DEX ecosystems — plus a generic adapter for direct Spraay calls on any supported chain.

## Install

```sh
npm install @spraay/dex-adapters viem
```

## Supported adapters

| Adapter | Import path | Chains | Hook contract |
|---|---|---|---|
| Generic (direct Spraay) | `@spraay/dex-adapters/generic` | Base, BNB Chain | N/A — calls Spraay contract directly |
| Uniswap V4 | `@spraay/dex-adapters/uniswap-v4` | Base, BNB Chain | `BatchDistributeHook` (CREATE2-mined, afterInitialize + afterDonate) |
| PancakeSwap Infinity | `@spraay/dex-adapters/pancakeswap` | BNB Chain | `BatchDistributeHook` (ICLHook) |
| SushiSwap | `@spraay/dex-adapters/sushiswap` | Base | Launchpad holder rewards |
| Balancer v3 | `@spraay/dex-adapters/balancer` | Base | `BatchDistributeHook` |

## How it works

Each DEX adapter wraps Spraay's on-chain batch functions (`sprayToken`, `sprayETH`, `sprayEqual`) as a composable hook inside that DEX's pool ecosystem. The hook doesn't intercept swaps or liquidity — it's a standalone utility that makes batch distribution available alongside a pool's existing incentive mechanisms.

**Cost**: 30 bps protocol fee. ~60% gas savings vs. 200 separate transfers.

**Recipient limit**: Up to 200 per transaction.

## Quick start — Generic (direct Spraay calls)

```ts
import { createPublicClient, createWalletClient, http, parseUnits } from 'viem'
import { base } from 'viem/chains'
import { distribute, estimateCost } from '@spraay/dex-adapters/generic'

const publicClient = createPublicClient({ chain: base, transport: http() })
const walletClient = createWalletClient({ chain: base, transport: http() })
const [account] = await walletClient.requestAddresses()

const recipients = ['0xAbc...', '0xDef...']
const amounts = [parseUnits('100', 6), parseUnits('250', 6)]
const USDC = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913' // USDC on Base

// Estimate cost (includes 30 bps fee)
const quote = await estimateCost({
  token: USDC, recipients, amounts,
  chain: base, publicClient, account
})

// Distribute — handles approval + simulation + send
const { hash, approvalHash } = await distribute({
  token: USDC, recipients, amounts,
  chain: base, walletClient, publicClient, account
})
```

## Uniswap V4 adapter

The V4 adapter deploys a `BatchDistributeHook` with CREATE2 address mining (V4 encodes hook permissions in the contract address). The hook uses `afterInitialize` (pool registration) and `afterDonate` callbacks.

```ts
import { base } from 'viem/chains'
import {
  deployHook,
  distribute,
  setOperator,
  UNISWAP_V4
} from '@spraay/dex-adapters/uniswap-v4'

// Deploy the hook (CREATE2-mined address with permission flags 0x1010)
const { address: hook } = await deployHook({
  chain: base,
  walletClient,
  publicClient,
  operator: account
})

// Distribute through the hook
await distribute({
  hook: hook!,
  token: USDC,
  recipients,
  amounts,
  chain: base,
  walletClient,
  publicClient
})
```

### Verified contract addresses

**Uniswap V4 PoolManager:**
- Base: `0x498581ff718922c3f8e6a244956af099b2652b2b`
- Ethereum: `0x000000000004444c5dc75cB358380D2e3dE08A90`
- Arbitrum: `0x360e68faccca8ca495c1b759fd9eee466db9fb32`
- BNB Chain: `0x28e2ea090877bf75740558f6bfb36a5ffee9e9df`

**Spraay contract:**
- Base: `0x1646452F98E36A3c9Cfc3eDD8868221E207B5eEC`
- BNB Chain: `0x3093a2953a4ecB125b82e6Fcd4fc0388cE5b32C1`

**BatchDistributeHook (Uniswap V4):**
- Base: [`0xB9c1aB7BD023C784c19B8e9F10CE9CDEd9fF9010`](https://basescan.org/address/0xB9c1aB7BD023C784c19B8e9F10CE9CDEd9fF9010#code) — verified, block 52791101

## PancakeSwap Infinity adapter

```ts
import { bsc } from 'viem/chains'
import {
  deployHook,
  distribute,
  encodeCLPoolParameters,
  getPoolId,
  PANCAKESWAP_INFINITY
} from '@spraay/dex-adapters/pancakeswap'

// Deploy hook
const { address: hook } = await deployHook({
  chain: bsc, walletClient, publicClient, operator: account
})

// Create pool with hook, then distribute
await distribute({
  hook: hook!,
  poolId,
  token: TOKEN,
  recipients,
  amounts,
  chain: bsc,
  walletClient,
  publicClient
})
```

## Push vs pull — when to use this

| | Pull (farms, donate, merkle) | Push (Spraay) |
|---|---|---|
| Who pays gas | Each recipient on claim | Sender, once per batch |
| Eligible recipients | On-chain positions/proofs | Any address |
| Allocation logic | On-chain | Off-chain, sender decides |
| Recipient action | Must claim | None |
| Best for | Open continuous incentives | Airdrops, holder rewards, revenue shares, targeted payouts |

The two models work together — a pool can run farms while the operator pushes one-off or targeted payouts through Spraay.

## Safety rules

- Always estimate cost before distributing (`estimateCost`)
- Approvals are bounded to exactly `amount + fee` — never infinite
- Verify recipient addresses off-chain before batching
- Test with dust amounts on mainnet before large distributions
- Private keys in environment variables only, never hardcoded

## Resources

- **SDK**: [npmjs.com/package/@spraay/dex-adapters](https://www.npmjs.com/package/@spraay/dex-adapters)
- **Uniswap V4 hook repo**: [github.com/plagtech/spraay-uniswap-v4-hook](https://github.com/plagtech/spraay-uniswap-v4-hook)
- **PancakeSwap hook repo**: [github.com/plagtech/spraay-pancakeswap-infinity-hook](https://github.com/plagtech/spraay-pancakeswap-infinity-hook)
- **Spraay Protocol**: [spraay.app](https://spraay.app)
- **Publisher**: Plagtech ([plagtech.net](https://plagtech.net))
