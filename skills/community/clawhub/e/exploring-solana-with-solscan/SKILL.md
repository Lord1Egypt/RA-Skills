---
name: solscan-data
description: >
  Use this skill to query Solana blockchain data via the Solscan Pro API.
  Triggers: look up wallet address, check token price, analyze NFT collection,
  inspect transaction, explore DeFi activities, get account metadata/label/tags,
  fetch block info, monitor API usage, search token by keyword.
version: 2.0.0
license: MIT
---

# Solscan Pro Skill

Empowers AI agents to retrieve professional-grade Solana on-chain data across
accounts, tokens, NFTs, transactions, blocks, markets, and programs.

## When to Use This Skill

- User asks about a Solana wallet address, balance, portfolio, or stake
- User wants token price, holders, markets, or trending tokens
- User needs to inspect a transaction signature or decode instructions
- User asks about NFT collections, items, or recent NFT activity
- User wants DeFi activity, transfer history, or reward exports
- User wants to analyze a program's on-chain statistics, transaction metrics, or user activity
- User needs to check popular DeFi platforms or view API usage

## Authentication

All requests require an API key in the HTTP header:

```http
token: <YOUR_SOLSCAN_API_KEY>
```

Base URL: `https://pro-api.solscan.io/v2.0`

---

## Tools

### Tool 1 — Direct API CLI (Precise Data)

**Use when**: you need exact, structured on-chain data for a specific address,
signature, block, or mint.

**Syntax**: `python3 scripts/solscan.py <resource> <action> [--param value]`

### Tool 2 — MCP Natural Language Tools

**Use when**: answering general exploratory questions or when the user does not
provide a specific address.

Available MCP tools:
- `search_transaction_by_signature` — look up a transaction by its signature
- `get_account_balance` — retrieve SOL balance for a wallet
- `get_token_metadata` — get name, symbol, decimals for a token mint

---

## API Reference

### Account

| Action | Key Params | Returns |
|---|---|---|
| `account detail` | `--address` | Lamports, owner, executable flag |
| `account data-decoded` | `--address` | Decoded account data |
| `account metadata` | `--address` | Label, icon, tags, domain, funder |
| `account metadata-multi` | `--addresses` | Batch metadata (comma-separated) |
| `account transfer` | `--address [filters...]` | SPL + SOL transfer history (supports activity-type, token, flow, time range filters) |
| `account defi` | `--address [filters...]` | DeFi protocol interactions (activity-type, from, platform, source, token, time range) |
| `account balance-change` | `--address [filters...]` | Historical balance changes (token, flow, amount, time range, remove-spam) |
| `account transactions` | `--address [--before] [--limit]` | Recent transactions list (cursor-based pagination) |
| `account portfolio` | `--address [--exclude-low-score-tokens]` | Token holdings with USD value |
| `account tokens` | `--address --type [--page] [--page-size] [--hide-zero]` | Associated token/NFT accounts (page-size: 10/20/30/40) |
| `account stake` | `--address [--page] [--page-size] [--sort-by] [--sort-order]` | Active stake accounts (page-size: 10/20/30/40) |
| `account reward-export` | `--address [--time-from] [--time-to]` | Staking reward history CSV (max 5000 items, max 1 req/min) |
| `account transfer-export` | `--address [filters...]` | Transfer history CSV (max 5000 items, max 1 req/min) |
| `account leaderboard` | `[--sort-by] [--sort-order] [--page] [--page-size]` | Top accounts by activity |
| `account defi-export` | `--address [filters...]` | DeFi activity CSV (max 5000 items, max 1 req/min) |

**`account metadata` response fields:**
> `account_address`, `account_label`, `account_icon`, `account_tags`, `account_type`, `account_domain`, `funded_by`, `tx_hash`, `block_time`

**`account transfer` filter options:**
> - `--activity-type`: Transfer type filter (comma-separated). Options: ACTIVITY_SPL_TRANSFER, ACTIVITY_SPL_BURN, ACTIVITY_SPL_MINT, ACTIVITY_SPL_CREATE_ACCOUNT, ACTIVITY_SPL_CLOSE_ACCOUNT, ACTIVITY_SPL_TOKEN_WITHDRAW_STAKE, ACTIVITY_SPL_TOKEN_SPLIT_STAKE, ACTIVITY_SPL_TOKEN_MERGE_STAKE, ACTIVITY_SPL_VOTE_WITHDRAW, ACTIVITY_SPL_SET_OWNER_AUTHORITY
> - `--token-account`: Filter transfers for a specific token account in the wallet
> - `--from`: Filter by source address(es) (max 5, comma-separated)
> - `--exclude-from`: Exclude transfers from address(es) (max 5, comma-separated)
> - `--to`: Filter by recipient address(es) (max 5, comma-separated)
> - `--exclude-to`: Exclude transfers to address(es) (max 5, comma-separated)
> - `--token`: Filter by token address(es) (max 5, comma-separated). Use `So11111111111111111111111111111111111111111` for native SOL
> - `--amount`: Amount range filter (min max)
> - `--value`: USD value range filter (min max)
> - `--from-time`, `--to-time`: Unix timestamp range filter
> - `--exclude-amount-zero`: Exclude transfers with zero amount (boolean)
> - `--flow`: Transfer direction: in|out
> - `--page-size`: 10, 20, 30, 40, 60, 100 (default: 10)
> - `--sort-order`: Sort order: asc|desc (default: desc)
>
> **Deprecated parameters**: `sort_by`, `block_time` (use `from_time`/`to_time` instead)

**`account defi` filter options:**
> - `--activity-type`: Activity type filter (comma-separated). Options: ACTIVITY_TOKEN_SWAP, ACTIVITY_AGG_TOKEN_SWAP, ACTIVITY_TOKEN_ADD_LIQ, ACTIVITY_TOKEN_REMOVE_LIQ, ACTIVITY_POOL_CREATE, ACTIVITY_SPL_TOKEN_STAKE, ACTIVITY_LST_STAKE, ACTIVITY_SPL_TOKEN_UNSTAKE, ACTIVITY_LST_UNSTAKE, ACTIVITY_TOKEN_DEPOSIT_VAULT, ACTIVITY_TOKEN_WITHDRAW_VAULT, ACTIVITY_SPL_INIT_MINT, ACTIVITY_ORDERBOOK_ORDER_PLACE, ACTIVITY_BORROWING, ACTIVITY_REPAY_BORROWING, ACTIVITY_LIQUIDATE_BORROWING, ACTIVITY_BRIDGE_ORDER_IN, ACTIVITY_BRIDGE_ORDER_OUT
> - `--from`: Filter activities from a specific address
> - `--platform`: Filter by platform address(es) (comma-separated, max 5)
> - `--source`: Filter by source address(es) (comma-separated, max 5)
> - `--token`: Filter by token address
> - `--from-time`, `--to-time`: Unix timestamp range filter
> - `--page-size`: 10, 20, 30, 40, 60, 100 (default: 10)
> - `--sort-by`: Sort field (default: block_time, options: block_time)
> - `--sort-order`: Sort order: asc|desc (default: desc)
>
> **Deprecated parameters**: `block_time` (use `from_time`/`to_time` instead)

**`account balance-change` filter options:**
> - `--token-account`: Filter by specific token account
> - `--token`: Filter by token address
> - `--amount`: Amount range (min max)
> - `--flow`: in|out
> - `--remove-spam`: true|false
> - `--from-time`, `--to-time`: Unix timestamp range
> - `--page-size`: 10, 20, 30, 40, 60, 100 (default: 10)
> - `--sort-by`: Sort field (default: block_time, options: block_time)
> - `--sort-order`: Sort order: asc|desc (default: desc)
>
> **Deprecated parameters**: `block_time` (use `from_time`/`to_time` instead)

**`account transactions` pagination:**
> - Uses cursor-based pagination with `--before` (transaction signature)
> - `--limit`: 10, 20, 30, 40 (default: 10)
> - No page/page_size parameters

**`account stake` options:**
> - `--sort-by`: active_stake|delegated_stake (default: active_stake)
> - `--sort-order`: asc|desc
> - `--page-size`: 10, 20, 30, 40 (default: 10)

**`account reward-export` parameters:**
> - `--time-from`: Start time (Unix timestamp in seconds, default: 1 month before time-to)
> - `--time-to`: End time (Unix timestamp in seconds, default: current time)

**`account transfer-export` filter options:**
> - `--activity-type`: Transfer type filter (comma-separated). Options: ACTIVITY_SPL_TRANSFER, ACTIVITY_SPL_BURN, ACTIVITY_SPL_MINT, ACTIVITY_SPL_CREATE_ACCOUNT, ACTIVITY_SPL_CLOSE_ACCOUNT, ACTIVITY_SPL_TOKEN_WITHDRAW_STAKE, ACTIVITY_SPL_TOKEN_SPLIT_STAKE, ACTIVITY_SPL_TOKEN_MERGE_STAKE, ACTIVITY_SPL_VOTE_WITHDRAW, ACTIVITY_SPL_SET_OWNER_AUTHORITY
> - `--token-account`: Filter by specific token account address
> - `--from`: Filter from address
> - `--to`: Filter to address
> - `--token`: Filter by token address (use `So11111111111111111111111111111111111111111` for native SOL)
> - `--amount`: Amount range (min max)
> - `--from-time`, `--to-time`: Unix timestamp range
> - `--exclude-amount-zero`: Exclude zero amount transfers
> - `--flow`: Transfer direction: in|out
>
> **Deprecated parameters**: `block_time` (use `from_time`/`to_time` instead)

**`account leaderboard` options:**
> - `--sort-by`: sol_values|stake_values|token_values|total_values (default: total_values)
> - `--sort-order`: asc|desc
> - `--page-size`: 10, 20, 30, 40, 60, 100 (default: 10)

**`account defi-export` filter options:**
> - `--activity-type`: Activity type filter (comma-separated). Options: ACTIVITY_TOKEN_SWAP, ACTIVITY_AGG_TOKEN_SWAP, ACTIVITY_TOKEN_ADD_LIQ, ACTIVITY_TOKEN_REMOVE_LIQ, ACTIVITY_POOL_CREATE, ACTIVITY_SPL_TOKEN_STAKE, ACTIVITY_LST_STAKE, ACTIVITY_SPL_TOKEN_UNSTAKE, ACTIVITY_LST_UNSTAKE, ACTIVITY_TOKEN_DEPOSIT_VAULT, ACTIVITY_TOKEN_WITHDRAW_VAULT, ACTIVITY_SPL_INIT_MINT, ACTIVITY_ORDERBOOK_ORDER_PLACE, ACTIVITY_BORROWING, ACTIVITY_REPAY_BORROWING, ACTIVITY_LIQUIDATE_BORROWING, ACTIVITY_BRIDGE_ORDER_IN, ACTIVITY_BRIDGE_ORDER_OUT
> - `--from`: Filter activities from a specific address
> - `--platform`: Filter by platform address(es) (comma-separated, max 5)
> - `--source`: Filter by source address(es) (comma-separated, max 5)
> - `--token`: Filter by token address
> - `--from-time`, `--to-time`: Unix timestamp range
> - `--sort-by`: Sort field (default: block_time, options: block_time)
> - `--sort-order`: Sort order: asc|desc (default: desc)
>
> **Deprecated parameters**: `block_time` (use `from_time`/`to_time` instead)

### Token

| Action | Key Params | Returns |
|---|---|---|
| `token meta` | `--address` | Name, symbol, decimals, supply |
| `token meta-multi` | `--addresses` | Batch metadata |
| `token price` ⚠️ | `--address [--from-time] [--to-time]` | **DEPRECATED** - Single token price history (use `token price-history` instead) |
| `token price-multi` ⚠️ | `--addresses [--from-time] [--to-time]` | **DEPRECATED** - Batch price history (use `token price-history` instead) |
| `token price-latest` | `--addresses` | Latest price of multiple tokens (max 50, comma-separated) |
| `token price-history` | `--addresses [--from-time] [--to-time]` | Historical price of multiple tokens (max 50, comma-separated; time: YYYYMMDD) |
| `token holders` | `--address [--page] [--page-size] [--from-amount] [--to-amount]` | Top holder list with amounts (page-size: 10/20/30/40) |
| `token markets` | `--token [--sort-by] [--program] [--page] [--page-size]` | DEX markets: 1 token for all markets, 2 tokens for pair search |
| `token transfers` | `--address [filters...]` | Transfer history |
| `token defi` | `--address [filters...]` | DeFi activity |
| `token defi-export` | `--address [filters...]` | DeFi activity CSV |
| `token historical` | `--address [--range]` | Historical data (price, volume, holder, trader,...) for a token (range: 7 or 30 days, default: 7) |
| `token search` | `--keyword [--search-mode] [--search-by] [--sort-by] [--sort-order] [--page] [--page-size]` | Search tokens by keyword/address/name/symbol |
| `token trending` | `[--limit]` | Currently trending tokens |
| `token list` | `[--page] [--page-size] [--sort-by] [--sort-order]` | Full token list (sort: holder|market_cap|created_time) |
| `token top` | — | Top tokens by market cap |
| `token latest` | `[--platform-id] [--page] [--page-size]` | Newly listed tokens (page-size: 10/20/30/40/60/100) |

**`token price` parameters** ⚠️ DEPRECATED:
> - `--address`: Token address (required)
> - `--from-time`: Start time in YYYYMMDD format (optional)
> - `--to-time`: End time in YYYYMMDD format (optional)

**`token price-multi` parameters** ⚠️ DEPRECATED:
> - `--addresses`: Token addresses, comma-separated (max 50, required)
> - `--from-time`: Start time in YYYYMMDD format (optional)
> - `--to-time`: End time in YYYYMMDD format (optional)

**`token price-latest` parameters:**
> - `--addresses`: Token addresses, comma-separated (max 50, required)

**`token price-history` parameters:**
> - `--addresses`: Token addresses, comma-separated (max 50, required)
> - `--from-time`: Start time in YYYYMMDD format (optional)
> - `--to-time`: End time in YYYYMMDD format (optional)

**`token holders` parameters:**
> - `--address`: Token address (required)
> - `--from-amount`: Minimum token holding amount (string format, optional)
> - `--to-amount`: Maximum token holding amount (string format, optional)
> - `--page`: Page number (default: 1)
> - `--page-size`: 10, 20, 30, 40 (default: 10)

**`token markets` parameters:**
> - `--token`: Token address(es) - REQUIRED (1 token for all markets, 2 tokens for pair search, comma-separated)
> - `--sort-by`: Sort field: volume|trade|tvl|trader
> - `--program`: Filter by DEX program(s) (comma-separated, max 5)
> - `--page`: Page number (default: 1)
> - `--page-size`: 10, 20, 30, 40, 60, 100 (default: 10)

**`token transfers` filter options:**
> - `--activity-type`: Transfer type filter (comma-separated). Options: ACTIVITY_SPL_TRANSFER, ACTIVITY_SPL_BURN, ACTIVITY_SPL_MINT, ACTIVITY_SPL_CREATE_ACCOUNT, ACTIVITY_SPL_CLOSE_ACCOUNT, etc.
> - `--from`: Filter from address(es) (max 5, comma-separated)
> - `--exclude-from`: Exclude from address(es) (max 5, comma-separated)
> - `--to`: Filter to address(es) (max 5, comma-separated)
> - `--exclude-to`: Exclude to address(es) (max 5, comma-separated)
> - `--amount`: Amount range (min max)
> - `--value`: USD value range (min max)
> - `--exclude-amount-zero`: Exclude zero amount transfers (boolean flag)
> - `--page-size`: 10, 20, 30, 40, 60, 100 (default: 10)
> - `--sort-by`: block_time (default: block_time)
> - `--sort-order`: asc|desc (default: desc)

**`token defi` filter options:**
> - `--activity-type`: Activity type filter (comma-separated). Options: ACTIVITY_TOKEN_SWAP, ACTIVITY_AGG_TOKEN_SWAP, ACTIVITY_TOKEN_ADD_LIQ, ACTIVITY_TOKEN_REMOVE_LIQ, ACTIVITY_POOL_CREATE, etc.
> - `--from`: Filter activities from a specific address
> - `--platform`: Filter by platform address(es) (comma-separated, max 5)
> - `--source`: Filter by source address(es) (comma-separated, max 5)
> - `--token`: Filter by token address
> - `--from-time`, `--to-time`: Unix timestamp range filter
> - `--page-size`: 10, 20, 30, 40, 60, 100 (default: 10)
> - `--sort-by`: block_time (default: block_time)
> - `--sort-order`: asc|desc (default: desc)

**`token defi-export` filter options:**
> - `--activity-type`: Activity type filter (comma-separated): ACTIVITY_TOKEN_SWAP, ACTIVITY_AGG_TOKEN_SWAP, etc.
> - `--from`: Filter activities from a specific address
> - `--platform`: Filter by platform address(es) (comma-separated, max 5)
> - `--source`: Filter by source address(es) (comma-separated, max 5)
> - `--token`: Filter by token address
> - `--from-time`, `--to-time`: Unix timestamp range filter
> - `--sort-by`: block_time (default: block_time)
> - `--sort-order`: asc|desc (default: desc)

**`token historical` parameters:**
> - `--address`: Token address (required)
> - `--range`: 7 or 30 days (default: 7)

**`token search` parameters:**
> - `--keyword`: Search term (required)
> - `--search-by`: combination|address|name|symbol (default: combination)
> - `--search-mode`: exact|fuzzy (default: exact)
> - `--exclude-unverified-token`: Exclude unverified tokens (boolean flag)
> - `--sort-by`: reputation|market_cap|volume_24h (default: reputation)
> - `--sort-order`: asc|desc (default: desc)
> - `--page`, `--page-size`: 10, 20, 30, 40 (default: 10)

**`token latest` platforms:**
> - `--platform-id`: jupiter, lifinity, meteora, orca, raydium, phoenix, sanctum, kamino, pumpfun, openbook, apepro, stabble, jupiterdca, jupiter_limit_order, solfi, zerofi, letsbonkfun_launchpad, raydium_launchlab, believe_launchpad, moonshot_launchpad, jup_studio_launchpad, bags_launchpad

### Transaction

| Action | Key Params | Returns |
|---|---|---|
| `transaction detail` | `--tx` | Full tx details (token and sol balance changes, IDL data, defi or transfer activities of each instructions) |
| `transaction detail-multi` | `--txs` | Batch tx details (max 50 transactions) |
| `transaction last` | `[--limit] [--filter]` | Most recent transactions |
| `transaction actions` | `--tx` | Human-readable decoded actions (transfers, swap activities, nft activities...) |
| `transaction actions-multi` | `--txs` | Batch decoded actions (max 50 transactions) |
| `transaction fees` | — | Network fees statistics (no parameters) |

**`transaction last` parameters:**
> - `--limit`: Number of transactions to return (10, 20, 30, 40, 60, 100, default: 10)
> - `--filter`: Filter type (exceptVote, all, default: exceptVote)

**`transaction detail` parameters:**
> - `--tx`: Transaction signature (required, length: 30-100 characters)

**`transaction detail-multi` parameters:**
> - `--txs`: Transaction signatures, comma-separated (required, max 50, each 30-100 characters)

**`transaction actions` parameters:**
> - `--tx`: Transaction signature (required, length: 30-100 characters)

**`transaction actions-multi` parameters:**
> - `--txs`: Transaction signatures, comma-separated (required, max 50, each 30-100 characters)

### NFT

| Action | Key Params | Returns |
|---|---|---|
| `nft news` | `--filter [--page] [--page-size]` | Latest NFT activity feed (filter: created_time, page-size: 12/24/36) |
| `nft activities` | `[filters...]` | NFT activities (all filters optional: from, to, source, activity-type, token, collection, currency-token, price, from-time, to-time) |
| `nft collections` | `[--range] [--sort-by] [--sort-order] [--collection] [--page] [--page-size]` | Top NFT collections (range: 1/7/30 days, sort: items/floor_price/volumes) |
| `nft items` | `--collection [--sort-by] [--page] [--page-size]` | Items inside a collection (sort: last_trade/listing_price, page-size: 12/24/36) |

**`nft activities` parameters** (all optional):
> - `--from`, `--to`: Filter by address
> - `--source`: Filter by source address(es) (comma-separated, max 5)
> - `--activity-type`: Type of activity (comma-separated). Options: ACTIVITY_NFT_SOLD, ACTIVITY_NFT_LISTING, ACTIVITY_NFT_BIDDING, ACTIVITY_NFT_CANCEL_BID, ACTIVITY_NFT_CANCEL_LIST, ACTIVITY_NFT_REJECT_BID, ACTIVITY_NFT_UPDATE_PRICE, ACTIVITY_NFT_LIST_AUCTION
> - `--token`: Token address
> - `--collection`: Collection address
> - `--currency-token`: Currency token address
> - `--price`: Price range filter (min max, requires currency_token parameter)
> - `--from-time`, `--to-time`: Unix timestamp range
> - `--page-size`: 10, 20, 30, 40, 60, 100 (default: 10)
> - `--block-time` ⚠️ **DEPRECATED**: Use `--from-time`/`--to-time` instead

**`nft collections` parameters** (all optional):
> - `--range`: Days range (1, 7, 30, default: 1)
> - `--sort-by`: Sort field (items, floor_price, volumes, default: volumes)
> - `--sort-order`: Sort order (asc, desc, default: desc)
> - `--collection`: Filter by collection ID
> - `--page`: Page number (default: 1)
> - `--page-size`: 10, 20, 30, 40 (default: 10)

**`nft items` parameters**:
> - `--collection`: Collection address (required)
> - `--sort-by`: Sort field (last_trade, listing_price, default: last_trade)
> - `--page`: Page number (default: 1)
> - `--page-size`: 12, 24, 36 (default: 12)

### Block

| Action | Key Params | Returns |
|---|---|---|
| `block last` | `[--limit]` | Get the list of the latest blocks |
| `block detail` | `--block` | Get the details of a block |
| `block transactions` | `--block [--page] [--page-size] [--exclude-vote] [--program]` | Get the list of transactions of a block |

**`block last` parameters:**
> - `--limit`: Number of blocks to return (10, 20, 30, 40, 60, 100, default: 10)

**`block detail` parameters:**
> - `--block`: The slot index of a block (required, minimum: 0)

**`block transactions` parameters:**
> - `--block`: The slot index of a block (required, minimum: 0)
> - `--page`: Page number for pagination (default: 1)
> - `--page-size`: Number of items per page (10, 20, 30, 40, 60, 100, default: 10)
> - `--exclude-vote`: Excludes vote transactions from the results (boolean flag, default: false)
> - `--program`: The program used to filter transactions that interact with it (optional, string)

### Market

| Action | Key Params | Returns |
|---|---|---|
| `market list` | `[--page] [--page-size] [--program] [--token-address] [--sort-by] [--sort-order]` | All trading pools/markets (sort: created_time\|volumes_24h\|trades_24h) |
| `market info` | `--address` | Get market/pool details by address |
| `market volume` | `--address [--time]` | Get historical market data and volume |

**`market list` parameters:**
> - `--page`: Page number (default: 1)
> - `--page-size`: Number of items per page (10, 20, 30, 40, 60, 100, default: 10)
> - `--program`: Program owner address (optional)
> - `--token-address`: Token address involved in market (optional)
> - `--sort-by`: Sort field (created_time, volumes_24h, trades_24h, default: volumes_24h)
> - `--sort-order`: Sort order (asc, desc, default: desc)

**`market info` parameters:**
> - `--address`: Market ID/address (required, minimum length: 30 characters)

**`market volume` parameters:**
> - `--address`: Market ID/address (required, minimum length: 30 characters)
> - `--time`: Filter data by time range in YYYYMMDD format. Pass start and end date to filter by time range (e.g., `--time 20240701 20240715`). Accepts 1-2 values (optional)

### Program

| Action | Key Params | Returns |
|---|---|---|
| `program list` | `[--sort-by] [--sort-order] [--page] [--page-size]` | Programs active in last 90 days (sort: num_txs\|num_txs_success\|interaction_volume\|success_rate\|active_users_24h) |
| `program popular-platforms` | — | Popular DeFi platforms |
| `program analytics` | `--address --range` | Program-level analytics for any Solana program (range: 7 or 30 days, required) |

**`program list` parameters:**
> - `--sort-by`: Sort field (num_txs, num_txs_success, interaction_volume, success_rate, active_users_24h, default: num_txs)
> - `--sort-order`: Sort order (asc, desc)
> - `--page`: Page number (default: 1)
> - `--page-size`: 10, 20, 30, 40 (default: 10)

**`program analytics` parameters:**
> - `--address`: Program address on Solana blockchain (required, minimum: 30 characters)
> - `--range`: Analytics time range in days (7 or 30, required)

### Monitor

| Action | Key Params | Returns |
|---|---|---|
| `monitor usage` | — | Your API key usage & rate limits |

---

## Error Handling

| HTTP Code | Meaning | Agent Action |
|---|---|---|
| `400` | Bad request / invalid address | Validate address format, retry |
| `401` | Authentication failed | Check `token` header is set correctly |
| `429` | Rate limit exceeded | Wait and retry with backoff |
| `500` | Internal server error | Retry once; report if persistent |

All error responses include `success: false`, `code`, and `message` fields.

---

## Example Workflows

### Wallet Research Workflow
- [ ] Step 1: `account metadata --address <ADDR>` → confirm label and type
- [ ] Step 2: `account portfolio --address <ADDR>` → get token holdings
- [ ] Step 3: `account transfer --address <ADDR>` → review recent activity
- [ ] Step 4: `account defi --address <ADDR>` → check protocol interactions

### Token Analysis Workflow
- [ ] Step 1: `token meta --address <MINT>` → confirm token identity
- [ ] Step 2: `token price --address <MINT>` → get current price
- [ ] Step 3: `token holders --address <MINT>` → check concentration risk
- [ ] Step 4: `token markets --token <MINT>` → find best liquidity pools

---

## Evaluations

| Query | Expected Behavior |
|---|---|
| "What tokens does wallet `ABC123` hold?" | Calls `account portfolio --address ABC123`, returns token list with USD values |
| "What is the current price of BONK?" | Calls `token meta` to resolve mint, then `token price`, returns USD price |
| "Decode transaction `XYZ...`" | Calls `transaction actions --signature XYZ`, returns human-readable action list |
| "Is this a known wallet?" | Calls `account metadata --address`, returns label/tags/domain if available |

---

*Resources: [Solscan Pro API Docs](https://pro-api.solscan.io/pro-api-docs/v2.0), [Solscan Pro API FAQs](https://pro-api.solscan.io/pro-api-docs/v2.0/faq.md)*
