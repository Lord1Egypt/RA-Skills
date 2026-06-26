---
name: debank
description: Query blockchain wallet data via DeBank API — balances, DeFi positions, tokens, NFTs, transaction history, gas prices, and token approvals. Use when the user asks about wallet balances, portfolio, DeFi positions, token prices, NFT holdings, transaction history, or gas prices on any EVM chain.
allowed-tools: Bash, Read
argument-hint: [command] [args...]
---

# DeBank CLI Skill

This skill uses [debank-cli](https://github.com/lolieatapple/debank-cli) to query blockchain data via the [DeBank Pro API](https://cloud.debank.com/).

**Skill repo**: https://github.com/lolieatapple/debank-skill
**CLI repo**: https://github.com/lolieatapple/debank-cli

## Prerequisites

Ensure `debank-cli` is installed globally:

```
!`which debank 2>/dev/null || echo "NOT_INSTALLED"`
```

If NOT_INSTALLED, install it:

```bash
npm install -g debank-cli
```

Then check if the API key is configured:

```
!`debank config show 2>&1`
```

If no API key is configured, ask the user for their DeBank Pro API key (obtain at https://cloud.debank.com/) and run:

```bash
debank config set-key <THE_KEY>
```

## Available Commands

### Wallet Queries

| Command | Description |
|---|---|
| `debank user balance <address>` | Total USD balance across all chains |
| `debank user tokens <address> [chain_id] [--all]` | Token balances (optionally filter by chain, `--all` includes dust) |
| `debank user protocols <address> [chain_id]` | DeFi protocol positions with full detail (supply, borrow, rewards) |
| `debank user nfts <address> [chain_id]` | NFT holdings |
| `debank user history <address> [chain_id] [count]` | Transaction history (max 20 per page) |
| `debank user approvals <address> <chain_id>` | Token approval/allowance list |
| `debank user chains <address>` | Chains where this address has activity |

### Token Queries

| Command | Description |
|---|---|
| `debank token info <chain_id> <token_id>` | Token details (name, symbol, decimals, price) |
| `debank token price <chain_id> <token_id> [YYYY-MM-DD]` | Current or historical price |
| `debank token holders <chain_id> <token_id> [limit]` | Top holders (default 20) |

### Chain & Gas

| Command | Description |
|---|---|
| `debank chain list` | All supported chains |
| `debank chain info <chain_id>` | Chain details |
| `debank gas <chain_id>` | Gas prices (slow/normal/fast) |

### Config & Account

| Command | Description |
|---|---|
| `debank config set-key <key>` | Save API key to `~/.debank-cli/config.json` |
| `debank config show` | Show current API key source and masked value |
| `debank config remove-key` | Remove saved API key |
| `debank account units` | Check remaining API units and usage |

## Common Chain IDs

`eth`, `bsc`, `matic`, `arb`, `op`, `base`, `avax`, `ftm`, `xdai`, `cro`, `linea`, `scroll`, `zksync`

## Native Token Addresses

For native tokens (ETH, BNB, etc.), use: `0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee`

## Handling the Request

If the user provides `$ARGUMENTS`, parse them and run the appropriate `debank` command directly.

Otherwise, determine the best command based on the user's natural language request:

- "What's in this wallet?" / "Show me the portfolio" → `debank user balance` + `debank user tokens` + `debank user protocols`
- "DeFi positions" / "protocol positions" → `debank user protocols`
- "Token balances" → `debank user tokens`
- "NFTs" → `debank user nfts`
- "Transaction history" → `debank user history`
- "Token price" / "How much is X?" → `debank token price`
- "Gas price" → `debank gas`
- "Approvals" / "allowances" → `debank user approvals`

For a comprehensive portfolio overview, run balance, tokens, and protocols in sequence to give a full picture.

Present the results clearly. When showing financial data, highlight the most significant positions and totals.
