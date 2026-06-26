---
name: agent-wallet-local-generate
description: Generate or import wallet details using either a mnemonic seed phrase or private key. Use when the user asks for wallet creation, recovery, onboarding, or key-based wallet setup.
---

# Wallet (Seed Phrase or Private Key)

## Runtime Requirements

- Runtime: Node.js 18+
- Required package: `viem`
- Optional network input: `RPC_URL` (only needed when validating on-chain state)

## Required Secrets / Inputs

- `SEED_PHRASE` only for mnemonic import
- `PRIVATE_KEY` only for private key import
- For new wallet generation, do not pre-read env secrets
- Ask for explicit consent before reading env-based signer secrets

## Inputs

Accept one of:
- a seed phrase (usually 12 or 24 words)
- a hex private key (`0x` prefixed or raw hex)
- a request to generate a new wallet

## Workflow

1. Determine input type:
   - **Seed phrase flow** for mnemonic words
   - **Private key flow** for hex key material
   - if unclear, ask: "Use seed phrase or private key?"
2. If agent wallet is missing, run wallet creation flow with `viem` (section below).
3. For seed phrase flow:
   - normalize phrase input (trim, collapse spaces, lowercase when appropriate)
   - validate word count (12/24) and checksum if supported
   - derive wallet from mnemonic with default path unless user specifies one
4. For private key flow:
   - confirm import/derive operation
   - normalize key format
   - trim whitespace
   - remove wrapping quotes
   - accept both `0x` and non-`0x` formats
5. Validate private key shape when private key flow is used:
   - 64 hex chars after removing `0x`
   - only `[0-9a-fA-F]`
6. Derive wallet address/public key for the selected method.
7. Persist secret material with secure storage only (vault, key manager, encrypted env secret store).
8. Return wallet details safely:
   - show address/public key
   - never show full seed phrase or private key

## No Wallet Exists (Viem)

When the agent has no wallet configured, create one first, then continue with normal wallet/transaction flows.

### Option A: Generate a new seed phrase wallet

```ts
import { generateMnemonic, mnemonicToAccount } from 'viem/accounts'

const mnemonic = generateMnemonic()
const account = mnemonicToAccount(mnemonic)

// Store mnemonic in secure secret storage only.
// Persist account.address as the agent wallet address.
```

### Option B: Generate a new private key wallet

```ts
import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts'

const privateKey = generatePrivateKey()
const account = privateKeyToAccount(privateKey)

// Store privateKey in secure secret storage only.
// Persist account.address as the agent wallet address.
```

### Option C: Import existing wallet

- If user provides `seedPhrase`, derive with `mnemonicToAccount`.
- If user provides `privateKey`, derive with `privateKeyToAccount`.
- In both cases, persist only via secure secret storage and keep values masked in logs.

## Response Template

- Method: `seed phrase` or `private key`
- Action: `generated`, `imported`, or `derived`
- Address: `<derived-address>`
- Network/Path: `<network>` / `<derivation-path-if-used>`
- Secret status: `validated and hidden`
- Status: `success` | `failed` | `needs_confirmation`
- Next step: `<backup|fund wallet|run balance check>`

## Standard Response Contract

- `action`: `generate` | `import`
- `chain`: chain id/name used, or `none` if offline generation only
- `address`: derived wallet address
- `txHash`: `null`
- `status`: `success` | `failed` | `needs_confirmation`
- `next_step`: one clear follow-up action

## Failure Handling

- Invalid mnemonic checksum -> stop, request corrected phrase, do not derive.
- Invalid private key length/hex -> stop, request corrected key format.
- Secret store unavailable -> stop and ask user to configure secure storage first.
- Chain mismatch during validation -> report mismatch and request target chain confirmation.

## Guardrails

- Reject invalid seed phrase word counts with a corrective prompt.
- If mnemonic checksum fails, ask for correction or confirmation.
- If private key length/format is invalid, stop and request corrected input.
- Never store secret material in plaintext files unless explicitly requested.
- Recommend secure offline backup after successful wallet derivation.
- If no wallet existed, confirm the new wallet was created and linked to the agent profile.
- Never echo full secrets in terminal output or chat logs.
