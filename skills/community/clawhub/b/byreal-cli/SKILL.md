---
name: byreal-cli
description: "Byreal DEX (Solana) data & analytics CLI: query pools, tokens, TVL, APR, k-line charts, farmer rankings, launchpad projects, and DeFi position stats. Use when user mentions Byreal, LP analytics, liquidity data, pool stats, or Solana DEX queries."
metadata:
  openclaw:
    homepage: https://github.com/byreal-git/byreal-cli
    requires:
      bins:
        - byreal-cli
    install:
      - kind: node
        package: "@byreal-io/byreal-cli"
        global: true
---

# Byreal DEX Analytics

## Get Full Documentation

Always run these commands first to get complete, up-to-date documentation:

```bash
# Complete documentation (commands, parameters, workflows, constraints)
byreal-cli skill

# Structured capability discovery (all capabilities with params)
byreal-cli catalog list

# Detailed parameter info for a specific capability
byreal-cli catalog show <capability-id>
```

## Installation

```bash
# Check if already installed
which byreal-cli && byreal-cli --version

# Install
npm install -g @byreal-io/byreal-cli
```

## Check for Updates

```bash
byreal-cli update check
```

If an update is available:

```bash
byreal-cli update install
```

## Credentials & Permissions

- Most commands are **read-only** and require no wallet
- Write commands require wallet setup via `byreal-cli setup` (interactive, handled by the CLI itself)
- AI agents should **never** ask users to paste private keys in chat; always direct them to `byreal-cli setup`

## Hard Constraints

1. **`-o json` only for parsing** — when showing results to the user, **omit it** and let the CLI's built-in tables/charts render directly. Never fetch JSON then re-draw charts yourself.
2. **Never truncate on-chain data** — always display the FULL string for: transaction signatures (txid), mint addresses, pool addresses, NFT addresses, wallet addresses. Never use `xxx...yyy` abbreviation.
3. **Preview first** with `--dry-run`, then `--confirm`
4. **Large amounts (>$1000)** require explicit confirmation
5. **High slippage (>200 bps)** must warn user
