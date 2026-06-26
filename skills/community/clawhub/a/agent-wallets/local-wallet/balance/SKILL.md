---
name: agent-wallet-local-balance
description: Check native or token contract balances for an address using viem. Use when the user asks for wallet balance, native coin balance, ERC-20/token balance, or balance verification for an address.
---

# Check Address Balance

## Runtime Requirements

- Runtime: Node.js 18+
- Required package: `viem`
- Required network input: `RPC_URL`

## Required Secrets / Inputs

- Required: `address`, `RPC_URL`, `chain`
- Optional: `tokenAddress`, `decimals`, `symbol`
- No signer secret is required for read-only balance checks

## Required Inputs

- `address`
- `rpcUrl`
- `chain` (for example `mainnet`, `sepolia`, or a custom chain object)
- optional for token balance:
  - `tokenAddress` (contract address)
  - optional `decimals` and `symbol` (if known)

## Workflow

1. Validate address with `isAddress`.
2. Create a `publicClient`.
3. If no `tokenAddress` is provided, check native balance:
   - call `publicClient.getBalance({ address })`
   - convert with `formatEther`
4. If `tokenAddress` is provided, check contract token balance:
   - validate `tokenAddress` with `isAddress`
   - call `publicClient.readContract` with ERC-20 `balanceOf`
   - optionally read `decimals`/`symbol`, then format with `formatUnits`
5. Return raw and formatted values for the selected mode.
6. If token metadata calls fail, return raw token amount and note missing metadata.

## Viem Example (Native)

```ts
import { createPublicClient, http, isAddress, formatEther } from 'viem'
import { sepolia } from 'viem/chains'

const address = '0xabc...'
if (!isAddress(address)) throw new Error('Invalid address')

const publicClient = createPublicClient({
  chain: sepolia,
  transport: http(process.env.RPC_URL!),
})

const wei = await publicClient.getBalance({ address })
const eth = formatEther(wei)

console.log({ address, wei: wei.toString(), eth })
```

## Viem Example (Contract Token / ERC-20)

```ts
import { createPublicClient, http, isAddress, formatUnits } from 'viem'
import { sepolia } from 'viem/chains'

const erc20Abi = [
  {
    type: 'function',
    name: 'balanceOf',
    stateMutability: 'view',
    inputs: [{ name: 'owner', type: 'address' }],
    outputs: [{ name: '', type: 'uint256' }],
  },
  {
    type: 'function',
    name: 'decimals',
    stateMutability: 'view',
    inputs: [],
    outputs: [{ name: '', type: 'uint8' }],
  },
] as const

const address = '0xabc...'
const tokenAddress = '0xdef...'
if (!isAddress(address) || !isAddress(tokenAddress)) throw new Error('Invalid address')

const publicClient = createPublicClient({
  chain: sepolia,
  transport: http(process.env.RPC_URL!),
})

const raw = await publicClient.readContract({
  address: tokenAddress,
  abi: erc20Abi,
  functionName: 'balanceOf',
  args: [address],
})

const decimals = await publicClient.readContract({
  address: tokenAddress,
  abi: erc20Abi,
  functionName: 'decimals',
})

const formatted = formatUnits(raw, decimals)
console.log({ address, tokenAddress, raw: raw.toString(), formatted })
```

## Response Template

- Address: `<address>`
- Chain: `<chain>`
- Mode: `native` or `token`
- Native balance (wei): `<wei>` (when mode is native)
- Native balance (formatted): `<formatted>` (when mode is native)
- Token contract: `<tokenAddress>` (when mode is token)
- Token balance (raw): `<raw>` (when mode is token)
- Token balance (formatted): `<formatted>` (when mode is token)
- Status: `success` | `failed`
- Next step: `<verify token decimals|switch RPC|recheck address>`

## Standard Response Contract

- `action`: `balance`
- `chain`: chain id/name used
- `address`: queried wallet address
- `txHash`: `null`
- `status`: `success` | `failed`
- `next_step`: one clear follow-up action

## Guardrails

- Validate address before querying.
- Validate `tokenAddress` when token mode is requested.
- Use read-only RPC for balance checks when possible.
- Never expose secret material while performing balance checks.

## Failure Handling

- Invalid address or token contract address -> stop and request corrected input.
- RPC/network timeout -> retry once, then request alternate RPC endpoint.
- Token contract missing `decimals` -> return raw amount and optionally format with user-supplied decimals.
- Contract call revert/proxy edge case -> return native balance fallback plus contract read error details.
