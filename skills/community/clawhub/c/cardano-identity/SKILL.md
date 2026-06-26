---
name: cardano-identity
description: "Resolve and list ADAHandles for the connected Cardano wallet."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
  openclaw:
    emoji: "🪪"
    requires:
      env: [SEED_PHRASE]
    install:
      - kind: node
        package: "@indigoprotocol/cardano-mcp"
---

# Cardano Identity — ADAHandles

Resolve and list ADAHandles for the connected Cardano wallet.

## Prerequisites

- `@indigoprotocol/cardano-mcp` server running

## MCP Tools

- `get_adahandles` — Retrieve all ADAHandles owned by the connected wallet

## When to use

Use this skill when the user asks about:

- Their ADAHandle or $handle
- Human-readable wallet identifiers
- Handle-to-address resolution

## Data interpretation

- ADAHandles are Cardano native tokens under a specific policy ID.
- Each handle maps to a wallet address (e.g. `$alice` resolves to `addr1...`).
- Handles are returned as plain strings without the `$` prefix.
