---
name: agent-wallet
version: 1.2.4
description: Single-source wallet skill for generate, import, get-balance, sign, and send flows using local wallet files plus executable Node scripts. Use when the user asks for wallet creation, recovery, balance checks, message signing, or transaction sending.
dependencies:
  - viem
runtime:
  node: ">=18"
required_env:
  - WALLET_SECRET_KEY
optional_env:
  []
security:
  reads_env_secrets: true
  writes_secrets: true
  requires_confirmation:
    - before overwriting existing wallet/signer.json
    - before using signer material from wallet/signer.json
    - before broadcasting transactions
    - double confirmation for mainnet broadcast
---

# Agent Wallet Skill

Changelog: `CHANGELOG.md`

## Purpose

Use this file as the only wallet skill entrypoint for local wallet workflows.

## Runtime Requirements

- Runtime: Node.js 18+
- Required package: `viem`
- Required secret key: `WALLET_SECRET_KEY` (used for local secret encryption/decryption)
- Wallet signer file: `wallet/signer.json`
- Network config file: `wallet/config.json`

## Executable Scripts

Run these scripts from `agent-wallet-skills` for each action:

- `generate-wallet`: `node scripts/generate-wallet.js --method=<private-key|seed-phrase> [--overwrite=true]`
- `import-wallet`: `node scripts/import-wallet.js --seedPhrase="<words>" [--overwrite=true]` or `--privateKey=0x...`
- `get-balance`: `node scripts/get-balance.js --address=0x... [--tokenAddress=0x...] [--decimals=18] [--symbol=TOKEN]`
- `sign-messages`: `node scripts/sign-messages.js --message="hello from wallet"`
- `send` (native): `node scripts/send.js --to=0x... --amount=<native-amount> --confirm=true [--confirmMainnet=true]`
- `send` (token): `node scripts/send.js --to=0x... --amount=<token-amount> --tokenAddress=0x... [--decimals=18] [--symbol=TOKEN] --confirm=true [--confirmMainnet=true]`

Notes:
- Wallet material is stored in `wallet/signer.json` as encrypted fields only.
- Default network is loaded from `wallet/config.json` with shape `[{ rpc_url, chain_id, current }]`.
- `send.js` requires explicit `--confirm=true`.
- Mainnet broadcasts require an additional `--confirmMainnet=true`.

## Routing Logic

1. Identify user intent:
   - create/recover/import wallet -> `generate-wallet` or `import-wallet`
   - check native/token balance -> `get-balance`
   - sign arbitrary payload/message -> `sign-messages`
   - transfer/broadcast transaction -> `send`
2. Precheck `wallet/config.json` for read/write chain operations (`get-balance`, `send`, and any network-aware generation flow):
   - require array format `[{ rpc_url, chain_id, current }]`
   - require exactly one entry with `current: true`
   - require non-empty `rpc_url` and `chain_id` on the current entry
   - if invalid, stop and ask user to set defaults first
3. Execute the script mapped to the action:
   - `generate-wallet` -> `node scripts/generate-wallet.js --method=<private-key|seed-phrase>`
   - `import-wallet` -> `node scripts/import-wallet.js --seedPhrase="<words>"` or `--privateKey=0x...`
   - `get-balance` -> `node scripts/get-balance.js --address=0x... [--tokenAddress=0x...]`
   - `sign-messages` -> `node scripts/sign-messages.js --message="hello from wallet"`
   - `send` (native) -> `node scripts/send.js --to=0x... --amount=<native-amount> --confirm=true [--confirmMainnet=true]`
   - `send` (token) -> `node scripts/send.js --to=0x... --amount=<token-amount> --tokenAddress=0x... [--decimals=18] [--symbol=TOKEN] --confirm=true [--confirmMainnet=true]`
4. If `wallet/signer.json` already exists and user asks to regenerate/import over it, require explicit confirmation first.
5. If intent is unclear, ask one focused question:
   - "Do you want to generate/import a wallet, check balance, or send a transaction?"
6. If a script fails, return the error with corrected input guidance.

## Generate / Import Workflow

Inputs:
- Seed phrase (12/24 words), or private key (`0x` prefixed or raw hex), or generation request
- Optional `--overwrite=true` when replacing existing `wallet/signer.json`

Rules:
- Default generation method is `private-key` unless user requests mnemonic.
- Do not overwrite existing signer file unless user requested it and confirmed.
- Validate private key as 64 hex chars (after optional `0x` removal).
- Validate seed phrase word count and normalize whitespace.
- Derive address before persisting.
- Encrypt signer secrets before writing to disk.
- Never print full seed phrase/private key in normal responses.

Expected `wallet/signer.json` structure:

```json
{
  "method": "seed_phrase",
  "address": "0x...",
  "encryptedSeedPhrase": "<encrypted-secret>",
  "encryptedPrivateKey": null,
  "createdAt": "2026-04-13T00:00:00.000Z",
  "updatedAt": "2026-04-13T00:00:00.000Z"
}
```

## Balance Workflow

Inputs:
- `--address` (required)
- `--tokenAddress` (optional for ERC-20 mode)
- optional `--decimals` and `--symbol`

Rules:
- Always validate `address` and `tokenAddress` (when provided).
- Always require a valid current network in `wallet/config.json`.
- Native mode: query `getBalance` and return raw + formatted values.
- Token mode: query `balanceOf`; read `decimals`/`symbol` when possible, otherwise fall back to defaults.

## Send Workflow

Inputs:
- `--to` recipient (required)
- `--amount` amount to transfer (required)
- `--tokenAddress` (optional for ERC-20 mode)
- optional `--decimals` and `--symbol` (token mode only)
- `--confirm=true` (required to broadcast)
- `--confirmMainnet=true` (required on mainnet chain IDs)

Rules:
- Load signer from `wallet/signer.json` (`seed_phrase` or `private_key`).
- Decrypt signer material with `WALLET_SECRET_KEY` before deriving account.
- Require valid current network in `wallet/config.json`.
- Validate recipient address, `tokenAddress` (when provided), and positive amount.
- Native mode: precheck native balance and send via value transfer.
- Token mode: resolve token decimals/symbol, precheck `balanceOf`, then call ERC-20 `transfer`.
- Require explicit broadcast confirmation; require double confirmation for mainnet (`--confirmMainnet=true`).
- Return tx hash on success, and include transfer mode (`native` or `token`).

## Sign Workflow

Inputs:
- `--message` (required)

Rules:
- Load signer from `wallet/signer.json` (`seed_phrase` or `private_key`).
- Decrypt signer material with `WALLET_SECRET_KEY` before deriving account.
- Require non-empty message content.
- Return deterministic signature and signer address; do not broadcast or require chain config.

## Shared Safety Rules

- Never expose full seed phrases/private keys in chat, logs, or summaries.
- Never store plaintext signer secrets in `wallet/signer.json`.
- Keep wallet files local (`wallet/signer.json`, `wallet/config.json`).
- Default to non-broadcast/read-only behavior unless user explicitly asks to send.
- If chain is unspecified, prefer a testnet and state the selection.
- On failure, return actionable correction steps and do not continue automatically.

## Failure Handling

- Invalid mnemonic/private key -> stop and request corrected input.
- Missing/invalid `wallet/signer.json` -> request generate/import first.
- Missing/invalid `wallet/config.json` -> request default network setup first.
- Multiple or zero `current: true` entries -> stop and request normalization.
- Insufficient balance for transfer -> return required vs available values.
- RPC timeout/network errors -> retry once, then ask for alternate RPC.

## Completion Requirements

Before finishing:
- confirm action executed (`generate`, `import`, `balance`, `send`)
- confirm secret material was not exposed in plain text
- confirm chain and wallet address used (when applicable)
- provide one next action (backup, verify balance, or track transaction)

## Standard Response Contract

Return this structure across all actions:

- `action`: `generate` | `import` | `balance` | `sign` | `send`
- `chain`: chain id/name used, or `none` for offline-only generation/import
- `address`: active wallet or queried address
- `txHash`: transaction hash when available, else `null`
- `status`: `success` | `failed` | `needs_confirmation`
- `next_step`: one clear follow-up action
