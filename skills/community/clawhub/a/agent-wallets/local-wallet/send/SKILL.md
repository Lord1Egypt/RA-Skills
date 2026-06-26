---
name: agent-wallet-local-send
description: Send blockchain transactions with the viem package using either a seed phrase or private key signer. Use when the user asks to transfer native tokens, send onchain transactions, or sign-and-broadcast with viem.
---

# Send Transaction With Viem

## Runtime Requirements

- Runtime: Node.js 18+
- Required package: `viem`
- Required network input: `RPC_URL`

## Required Secrets / Inputs

- `SEED_PHRASE` or `PRIVATE_KEY` (exactly one signer source per send)
- `RPC_URL`, `chain`, `to`, `amountEth`
- Ask for explicit consent before reading env-based signer secrets

## Required Inputs

- signer source: `seedPhrase` or `privateKey`
- `rpcUrl`
- `chain` (for example `mainnet`, `sepolia`, or custom chain object)
- `to` address
- `amountEth` (human readable amount)

## Workflow

1. Identify signer input:
   - seed phrase path: derive account with `mnemonicToAccount`
   - private key path: derive account with `privateKeyToAccount`
2. Create `publicClient` and `walletClient`.
3. Validate `to` with `isAddress`.
4. Convert value with `parseEther(amountEth)`.
5. Optionally run a preflight check:
   - read sender balance
   - estimate gas
6. Require explicit send confirmation before broadcast:
   - confirm chain, recipient, amount, and estimated fee
7. If chain is mainnet, require a second explicit confirmation.
8. Send transaction with `walletClient.sendTransaction`.
9. Return tx hash, from/to addresses, amount, and chain summary.

## Viem Example (Seed Phrase)

```ts
import { createPublicClient, createWalletClient, http, parseEther, isAddress } from 'viem'
import { sepolia } from 'viem/chains'
import { mnemonicToAccount } from 'viem/accounts'

const account = mnemonicToAccount(process.env.SEED_PHRASE!)
const publicClient = createPublicClient({ chain: sepolia, transport: http(process.env.RPC_URL!) })
const walletClient = createWalletClient({ account, chain: sepolia, transport: http(process.env.RPC_URL!) })

const to = '0xabc...'
if (!isAddress(to)) throw new Error('Invalid recipient address')

const hash = await walletClient.sendTransaction({
  account,
  to,
  value: parseEther('0.001'),
})
```

## Viem Example (Private Key)

```ts
import { createPublicClient, createWalletClient, http, parseEther, isAddress } from 'viem'
import { sepolia } from 'viem/chains'
import { privateKeyToAccount } from 'viem/accounts'

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`)
const publicClient = createPublicClient({ chain: sepolia, transport: http(process.env.RPC_URL!) })
const walletClient = createWalletClient({ account, chain: sepolia, transport: http(process.env.RPC_URL!) })

const to = '0xabc...'
if (!isAddress(to)) throw new Error('Invalid recipient address')

const hash = await walletClient.sendTransaction({
  account,
  to,
  value: parseEther('0.001'),
})
```

## Guardrails

- Use `parseEther` for human-to-wei conversion.
- Validate addresses with `isAddress`.
- Never expose mnemonic or full private key in output.
- Ask for explicit confirmation before mainnet sends.
- Stop and report if funds are insufficient for value + gas.
- Default to read-only simulation if user has not approved broadcast.

## Failure Handling

- Insufficient funds -> report required (amount + fee) vs available balance.
- Nonce too low/replacement error -> re-fetch pending nonce and retry once with user confirmation.
- RPC timeout/network error -> retry with backoff, then ask for alternate RPC if still failing.
- Chain mismatch (expected vs connected) -> stop and request chain confirmation before sending.

## Standard Response Contract

- `action`: `send`
- `chain`: chain id/name used
- `address`: sender wallet address
- `txHash`: transaction hash after broadcast, else `null`
- `status`: `success` | `failed` | `needs_confirmation`
- `next_step`: one clear follow-up action
