---
name: agent-wallet-local
description: Route local wallet tasks to generation/import, balance checks, or transaction-send docs. Use when the user asks to create/import a local wallet, check address balance, or send a transaction from a local wallet.
---

# Local Wallet Router

## Purpose

Map local wallet task types to the correct skill documentation.

## Runtime Requirements

- Runtime: Node.js 18+
- Required package: `viem`
- Required network input: `RPC_URL` for chain access

## Required Secrets / Inputs

- `RPC_URL` for all chain reads/writes
- `SEED_PHRASE` only for mnemonic import/sign flows
- `PRIVATE_KEY` only for private key import/sign flows
- Ask before reading env secrets

## Task Type -> Doc Location

- `generate` (create/import/recover wallet) -> [generate/SKILL.md](generate/SKILL.md)
- `balance` (check native balance for an address) -> [balance/SKILL.md](balance/SKILL.md)
- `send` (send transaction with existing wallet) -> [send/SKILL.md](send/SKILL.md)

## Routing Steps

1. Identify user intent:
   - wallet creation/import/recovery -> `generate`
   - address/native coin balance query -> `balance`
   - transaction transfer/broadcast -> `send`
2. Route to the mapped skill doc.
3. If intent is unclear, ask:
   - "Do you want to generate/import a wallet, check balance, or send a transaction?"

## Safety Notes

- Never expose seed phrases or private keys in plaintext.
- Confirm secure secret storage is used before completing generate/send flows.
- Default to read-only mode unless user explicitly requests a send/broadcast.
- Default to testnet when chain is unspecified and disclose that choice.

## Standard Response Contract

- `action`: `generate` | `import` | `balance` | `send`
- `chain`: chain id/name used
- `address`: active wallet or queried address
- `txHash`: transaction hash when available, else `null`
- `status`: `success` | `failed` | `needs_confirmation`
- `next_step`: one clear follow-up action
