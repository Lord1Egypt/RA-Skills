---
name: chainstream-graphql
description: >-
  Execute flexible GraphQL queries against ChainStream's on-chain data warehouse (27 cubes in 3 chain groups: EVM, Solana, Trading).
  Use when user needs custom analytics beyond standard REST/MCP — cross-cube JOINs, custom aggregations, complex WHERE filters,
  time-series analysis, or SQL-level flexibility on blockchain data. Supports x402/MPP auto-payment.
  Keywords: GraphQL, query, cube, DEXTrades, DEXTradeByTokens, Pairs, aggregation, join, on-chain analytics, custom query.
---

# ChainStream GraphQL

Flexible GraphQL interface to ChainStream's on-chain data warehouse. 27 cubes organized in 3 chain groups (EVM / Solana / Trading), covering DEX trades, token-centric trade analysis, trading pairs, transfers, blocks, transactions, prediction markets, and more — across Solana, Ethereum, BSC, and Polygon.

- **Endpoint**: `https://graphql.chainstream.io/graphql` (routed through APISIX gateway)
- **CLI**: `npx @chainstream-io/cli graphql`
- **Auth**: API Key via `X-API-KEY` header
- **Payment**: x402 (USDC on Base/Solana) or MPP (USDC.e on Tempo) — auto-handled by CLI

## When to Use GraphQL vs chainstream-data

| Scenario | Use | Why |
|----------|-----|-----|
| Standard token search, market trending, wallet profile | `chainstream-data` (REST/MCP) | Pre-built endpoints, simpler |
| Cross-cube JOIN (trades + instructions, trades + transfers) | **GraphQL** | joinXxx support |
| Custom aggregation (count, sum, avg with groupBy) | **GraphQL** | Metrics + dimension grouping |
| Complex filters (multi-condition WHERE, nested, OR via `any`) | **GraphQL** | Full filter operator support |
| Time-series data with custom resolution | **GraphQL** | Time interval bucketing + dimension aggregation |
| Prediction market data (PolyMarket) | **GraphQL** | PredictionTrades/Managements/Settlements cubes (Polygon) |
| Data not exposed by REST API | **GraphQL** | Direct access to all 27 cubes |

## Integration Path

**Before anything else (CLI path), ensure user is authenticated:**
1. `npx @chainstream-io/cli config auth` — check login status
2. If NOT logged in → `npx @chainstream-io/cli login` (creates EVM + Solana wallet, auto-grants **nano trial plan: 50K CU free, 30 days** — no purchase needed)
3. `npx @chainstream-io/cli plan status` — verify subscription is active

**New users get a free trial on login (50K CU).** For details on trial plans and upgrade options, see [`shared/authentication.md`](../shared/authentication.md#agent-bootstrap-checklist).

1. **Has API Key?**
   → YES → Use CLI directly: `npx @chainstream-io/cli graphql query --query '...'`
   → NO → Ensure logged in (see above), then CLI auto-handles on first 402

2. **First time / unsure about schema?**
   → Run `npx @chainstream-io/cli graphql schema --summary` to discover available cubes
   → Run `npx @chainstream-io/cli graphql schema --type DEXTrades` to drill into a specific cube

3. **Need full schema reference for complex query construction?**
   → Run `npx @chainstream-io/cli graphql schema --full` for complete field list + rules

## Getting an API Key

GraphQL goes through ChainStream's unified APISIX gateway — **same API Key and subscription quota as the REST API**.

- **Dashboard users**: [app.chainstream.io](https://app.chainstream.io) → API Keys
- **AI Agents (x402)**: CLI auto-purchases on first 402 — USDC on Base or Solana → API Key auto-saved to `~/.config/chainstream/config.json`
- **AI Agents (MPP)**: `tempo request "https://api.chainstream.io/mpp/purchase?plan=<PLAN>"` → API Key auto-returned
- **CLI auto-payment**: No pre-purchase needed. First `graphql query` that triggers 402 → interactive plan selection → payment → auto-retry

```bash
# Option A: Set existing API Key
npx @chainstream-io/cli config set --key apiKey --value <your-api-key>

# Option B: Create wallet for x402 auto-payment
npx @chainstream-io/cli login

# Option C: Check pricing first
npx @chainstream-io/cli wallet pricing
```

## Endpoint Selector

| Intent | CLI Command |
|--------|-------------|
| List all cubes + descriptions | `npx @chainstream-io/cli graphql schema --summary` |
| Explore one cube's fields | `npx @chainstream-io/cli graphql schema --type <CubeName>` |
| Full schema reference | `npx @chainstream-io/cli graphql schema --full` |
| Force-refresh cached schema | `npx @chainstream-io/cli graphql schema --summary --refresh` |
| Execute inline query | `npx @chainstream-io/cli graphql query --query '<graphql>'` |
| Execute query from file | `npx @chainstream-io/cli graphql query --file ./query.graphql` |
| Execute with variables | `npx @chainstream-io/cli graphql query --query '...' --var '{"key":"value"}'` |
| Machine-readable output | Append `--json` to any command |

## AI Workflow

### Step 1: Discover Schema (first time or when unsure)

```bash
npx @chainstream-io/cli graphql schema --summary
```

This returns a compact list of all 27 cubes organized by chain group (EVM/Solana/Trading) with descriptions and top-level fields. If you need details on a specific cube:

```bash
npx @chainstream-io/cli graphql schema --type DEXTrades
```

### Step 2: Construct and Execute Query

**MANDATORY — READ** [references/schema-guide.md](references/schema-guide.md) before constructing your first query.

Based on schema knowledge + user intent, construct a GraphQL query and execute:

```bash
npx @chainstream-io/cli graphql query --query 'query {
  Solana {
    DEXTrades(limit: {count: 25}, orderBy: {descending: Block_Time}) {
      Block { Time }
      Trade { Buy { Currency { MintAddress } Amount PriceInUSD } Sell { Currency { MintAddress } Amount } Dex { ProtocolName } }
    }
  }
}' --json
```

If the user has no subscription, use the non-interactive purchase flow: `plan status --json` → `wallet pricing --json` (present plans to user) → `plan purchase --plan <USER_CHOSEN> --json` (signs x402 payment, returns API Key). See [x402-payment.md](../shared/x402-payment.md) for details.

### Step 3: Analyze Results

- Parse JSON output
- Identify data patterns (time series, ranking, distribution, comparison)
- Provide insights in natural language
- If visualization is needed, choose appropriate chart type based on data shape

## Query Construction Quick Reference

The schema uses **chain group wrappers** as the top-level entry point:

```graphql
# Solana (no network arg needed)
query {
  Solana {
    CubeName(limit: {count: N}, orderBy: {descending: Field}, where: {...}) {
      FieldGroup { SubField }
      joinXxx { ... }
      count
    }
  }
}

# EVM (network required: eth | bsc | polygon)
query {
  EVM(network: eth) {
    CubeName(limit: {count: N}, orderBy: {descending: Field}, where: {...}) {
      FieldGroup { SubField }
    }
  }
}

# Trading (cross-chain pre-aggregated, no network arg)
query {
  Trading {
    Pairs(tokenAddress: {is: "..."}, limit: {count: 24}) {
      TimeMinute
      Price { Open High Low Close }
    }
  }
}
```

- **Chain group wrapper**: Top-level required. `Solana`, `EVM(network: ...)`, or `Trading`.
- **network**: Only on `EVM` wrapper. Values: `eth`, `bsc`, `polygon`.
- **limit**: `{count: N, offset: M}`. Default 25.
- **orderBy**: `{descending: Field}` or `{ascending: Field}`. For computed fields: `{descendingByField: "field_name"}`.
- **where**: `{Group: {Field: {operator: value}}}`. OR conditions: `any: [{...}, {...}]`.
- **DateTime format**: `"YYYY-MM-DD HH:MM:SS"` — NO `T`, NO `Z`. Critical for ClickHouse.
- **DateTimeFilter**: `since`, `till`, `after`, `before` — NEVER `gt`/`lt`.
- **joinXxx**: LEFT JOIN to related cubes. Always prefer over multiple queries.
- **dataset**: Optional wrapper arg — `realtime`, `archive`, or `combined` (default).
- **aggregates**: Optional wrapper arg — `yes`, `no`, or `only`.

## Chain Groups and Cubes

| Chain Group | Wrapper | Cubes |
|------------|---------|-------|
| **Solana** | `Solana { ... }` | DEXTrades, DEXTradeByTokens, Transfers, BalanceUpdates, Blocks, Transactions, DEXPools, Instructions, InstructionBalanceUpdates, Rewards, DEXOrders, TokenSupplyUpdates |
| **EVM** | `EVM(network: eth\|bsc\|polygon) { ... }` | DEXTrades, DEXTradeByTokens, Transfers, BalanceUpdates, Blocks, Transactions, DEXPoolEvents, Events, Calls, MinerRewards, DEXPoolSlippages, TokenHolders, TransactionBalances, Uncles, PredictionTrades*, PredictionManagements*, PredictionSettlements* |
| **Trading** | `Trading { ... }` | Pairs, Tokens, Currencies, Trades |

*Prediction cubes only available on `polygon` network.

## NEVER Do

- NEVER use flat query format (`CubeName(network: sol)` without chain group wrapper) — always wrap in `Solana { ... }`, `EVM(network: ...) { ... }`, or `Trading { ... }`
- NEVER guess field names without checking schema first — run `graphql schema --summary` or `--type`
- NEVER use ISO 8601 datetime format (`2026-03-31T00:00:00Z`) — ClickHouse requires `"2026-03-31 00:00:00"`
- NEVER use `gt`/`lt` on DateTime fields — use `since`/`after`/`before`/`till`
- NEVER split related data into multiple queries when joinXxx can combine them
- NEVER auto-select a payment plan — always let the user choose

## Error Recovery

| Error | Meaning | Recovery |
|-------|---------|----------|
| 401 / "Not authenticated" | Not logged in or no API Key | First `config auth` → `login` if not logged in (auto-grants nano trial 50K CU) → retry. If still failing: `config set --key apiKey --value <key>` |
| 402 | No active subscription | First `config auth` → `login` if needed (trial may suffice) → `plan status`. If no subscription or quota exhausted: `wallet pricing` then `plan purchase`. **MANDATORY — READ** [`shared/x402-payment.md`](../shared/x402-payment.md) for manual purchase flow |
| "GraphQL error: ..." | Invalid query syntax or non-existent field | Check field names against `graphql schema --type <cube>` |
| 429 | Rate limit | Wait 1s, exponential backoff |
| 5xx | Server error | Retry once after 2s |

On 401/402, follow this sequence:
1. **Check login**: `npx @chainstream-io/cli config auth` — if not logged in, run `login` (creates wallet + auto-grants nano trial with 50K CU free). After login, retry the failed command — it will likely succeed now
2. **Check subscription**: `npx @chainstream-io/cli plan status` — if `active: true` with remaining quota, retry
3. **If logged in but no subscription**: ask the user "Do you have a ChainStream API Key?" — if yes, `config set --key apiKey --value <key>` and retry; if no, load [`shared/x402-payment.md`](../shared/x402-payment.md) for the purchase flow. GraphQL shares the same API Key / subscription pool as the REST API — no separate purchase needed.

## Skill Map

| Reference | Content | When to Load |
|-----------|---------|--------------|
| [schema-guide.md](references/schema-guide.md) | Query syntax, filter operators, joinXxx rules, advanced patterns, common mistakes | Before constructing any query |
| [query-patterns.md](references/query-patterns.md) | 20+ ready-to-use query templates by scenario | When building queries for common use cases |
| [x402-payment.md](../shared/x402-payment.md) | x402 and MPP payment protocols, plan purchase flow | On 402 errors or when user needs subscription |
| [authentication.md](../shared/authentication.md) | API Key setup, wallet auth, MCP config | On auth errors |

## Related Skills

- [chainstream-data](../chainstream-data/) — Standard REST/MCP queries for common analytics (token search, market trending, wallet profile). Use when pre-built endpoints suffice.
- [chainstream-defi](../chainstream-defi/) — DeFi execution: swap, bridge, create token, sign transactions. Use when analysis leads to action.
