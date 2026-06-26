---
name: agent-wallet
description: Route wallet workflows for agents that need to generate or import wallets using either a seed phrase or private key. Use when the user asks for wallet creation, import, recovery, or key-based onboarding.
---

# Agent Wallet Skills

## Purpose

Use this skill as the main entrypoint for wallet setup workflows.

## Runtime Requirements

- Runtime: Node.js 18+ (or equivalent TS/JS runtime)
- Required package: `viem`
- Network access: RPC endpoint for the target chain
- Secret storage: vault, key manager, or encrypted secret store

## Required Secrets / Inputs

- `RPC_URL` for chain reads/writes
- `SEED_PHRASE` only when user explicitly chooses mnemonic import/signing
- `PRIVATE_KEY` only when user explicitly chooses private key import/signing
- Agent must ask for confirmation before reading env-based secrets

## Wallet Type -> Skill Location Map

- Local wallet (generate/import with seed phrase or private key): [local-wallet/SKILL.md](local-wallet/SKILL.md)
- Check native/token balance (`viem`): [local-wallet/balance/SKILL.md](local-wallet/balance/SKILL.md)
- Send transaction with existing wallet (`viem`): [local-wallet/send/SKILL.md](local-wallet/send/SKILL.md)

## Routing Logic

1. Check if the agent already has a wallet configured:
   - if wallet exists, use existing wallet flow
   - if wallet does not exist, run wallet generation flow (step 2)
2. Wallet generation flow (no existing wallet):
   - ask preferred method: seed phrase or private key import
   - if user does not provide a method, default to generating a new seed phrase wallet
   - generate/import with `viem` account helpers in `local-wallet/SKILL.md`
   - derive address/public key and persist via the project's secure secret mechanism
3. Identify the wallet input type from the user request:
   - mnemonic / seed phrase words
   - hex private key string
   - request to generate a new wallet
4. Route by wallet type to the mapped location:
   - `seed phrase` -> `local-wallet/SKILL.md`
   - `private key` -> `local-wallet/SKILL.md`
   - `check balance` -> `local-wallet/balance/SKILL.md`
   - `send transaction` -> `local-wallet/send/SKILL.md`
5. If input type is unclear, ask one focused question:
   - "Do you want to use a seed phrase or a private key?"

## No Wallet Exists (Viem Flow)

When the agent has no wallet configured, create one with `viem` before continuing.

### Preferred default (generate new private key wallet)

```ts
import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts'

const privateKey = generatePrivateKey()
const account = privateKeyToAccount(privateKey)

// Persist privateKey via secure secret storage only (env vault, key manager, etc.)
// Use account.address as the agent wallet address.
```

### Optional seed phrase path

- If user explicitly asks for seed phrase-based setup, follow `local-wallet/SKILL.md` seed phrase flow.
- Derive the account/address and store secret material in secure secret storage.

### Required checks after generation

- Wallet address exists and is valid format for the target chain.
- Secret material is stored securely and never echoed in plaintext.
- Agent metadata references the new wallet address for future operations.

## Shared Safety Rules

- Never print full seed phrases or private keys in outputs, logs, or summaries.
- Mask secrets when showing examples (for example `ab12...9f`).
- Prefer offline generation/import steps where possible.
- Remind users to back up secrets in a secure location.
- Default to read-only actions until user explicitly asks to send/broadcast.
- If chain is not provided, default to a testnet and state that choice.
- Never broadcast immediately after simulation without explicit confirmation.

## Completion Requirements

Before finishing:
- confirm wallet address/public key was derived successfully
- confirm secret material was not exposed in plain text
- if wallet was missing, confirm a new wallet was created and stored securely
- provide next action (backup, test transaction, or network config)

## Standard Response Contract

Return this structure across all wallet skills:

- `action`: `generate` | `import` | `balance` | `send`
- `chain`: chain id/name used
- `address`: active wallet or queried address
- `txHash`: transaction hash when available, else `null`
- `status`: `success` | `failed` | `needs_confirmation`
- `next_step`: one clear follow-up action
