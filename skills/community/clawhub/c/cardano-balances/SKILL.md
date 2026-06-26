---
name: cardano-balances
description: "Query wallet balances, addresses, and UTxOs on the Cardano blockchain."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
  openclaw:
    emoji: "💰"
    requires:
      env: [SEED_PHRASE]
    install:
      - kind: node
        package: "@indigoprotocol/cardano-mcp"
---

# Cardano Wallet Balances

Query wallet balances, addresses, and UTxOs on the Cardano blockchain.

## Prerequisites

- `@indigoprotocol/cardano-mcp` server running

## MCP Tools

- `get_balances` — Retrieve all balances and native assets for the connected wallet
- `get_addresses` — Retrieve all Cardano addresses for the connected wallet
- `get_utxos` — Retrieve all UTxOs for the connected wallet

## When to use

Use this skill when the user asks about:

- Wallet balances or ADA amount
- Native tokens or assets in their wallet
- Wallet addresses
- UTxO details or UTXO inspection

## Data interpretation

- Balances are returned in **lovelace** (1 ADA = 1,000,000 lovelace). Always convert to ADA for display.
- Native assets are identified by `policyId` + `nameHex`.
- The `name` field provides a human-readable label when available.
