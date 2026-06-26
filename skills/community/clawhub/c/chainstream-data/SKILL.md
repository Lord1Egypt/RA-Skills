---
name: chainstream-data
description: "Query and analyze on-chain data via MCP (17 tools) and CLI across Solana, BSC, Ethereum. Use when user asks to search tokens, check token security or holders, track market trends or hot tokens, analyze wallet PnL or holdings, stream real-time trades, compare multiple tokens, or backtest trading strategies. Covers token analytics, market ranking, wallet profiling, and WebSocket streaming. Keywords: token, wallet, market, trending, PnL, holders, security, candles, WebSocket, on-chain data, MCP."
---

# ChainStream Data

On-chain data intelligence for AI agents. Access token analytics, market trends, wallet profiling, and compliance screening across Solana, BSC, and Ethereum.

- **MCP Server**: `https://mcp.chainstream.io/mcp` (streamable-http, 17 tools)
- **CLI**: `npx @chainstream-io/cli`
- **SDK**: `@chainstream-io/sdk`
- **Base URL**: `https://api.chainstream.io`

## Integration Path (check FIRST)

**Agent runtime decision tree — choose based on environment and operation type:**

1. **MCP tools registered?** (Cursor/Claude Desktop/VS Code already configured ChainStream MCP)
   → YES → Use MCP tools for data queries (`tokens_search`, `wallets_profile`, etc.)
   → NO → Use CLI for all operations (`npx @chainstream-io/cli ...`)

2. **Need DeFi operation?** (swap, create token, sign transaction)
   → YES → Must use CLI (MCP has no wallet signing capability)
   → NO → Continue with MCP (or CLI if MCP unavailable)

3. **MCP call failed?**
   → Fall back to CLI as backup

**Before anything else (CLI path), ensure user is authenticated:**
1. `npx @chainstream-io/cli config auth` — check login status
2. If NOT logged in → `npx @chainstream-io/cli login` (creates EVM + Solana wallet, auto-grants **nano trial plan: 50K CU free, 30 days** — no purchase needed)
3. If logged in → proceed to subscription check below

**New users get a free trial on login (50K CU).** For details on trial plans and upgrade options, see [`shared/authentication.md`](../shared/authentication.md#agent-bootstrap-checklist).

**Then check subscription:** `npx @chainstream-io/cli plan status`
- If `active: true` → proceed with data queries
- If no subscription → follow the purchase flow below (NEVER just run a data command hoping it "auto-purchases")

**Getting an API Key (required for all paths):**
- Dashboard users: [app.chainstream.io](https://app.chainstream.io) → API Keys
- x402 (USDC on Base/Solana): `npx @chainstream-io/cli plan purchase --plan <PLAN> --json` → x402 purchase (real USDC payment via EIP-3009 signature). Run `wallet pricing --json` first, present ALL plans, let user choose
- MPP (USDC.e on Tempo): `tempo request "https://api.chainstream.io/mpp/purchase?plan=<PLAN>"` → MPP payment → API Key auto-returned (fetch `/mpp/pricing` first, let user choose plan)

**⚠️ Purchase flow (x402)**:
0. `config auth` — ensure user is logged in. If not: `login` first (auto-grants nano trial — may be sufficient, check `plan status` before proceeding to purchase)
1. `plan status --json` — check if subscription already exists (login auto-grants nano trial, so new users likely already have one)
2. If `active: true` and quota sufficient → no purchase needed, proceed with data queries
3. If no subscription or quota exhausted: `wallet pricing --json` — present ALL plans, let user choose. **NEVER auto-select a plan.**
4. `wallet balance --chain base --json` (and/or `--chain sol`) — check where user has USDC
5. If USDC is on Solana: `config set --key walletChain --value sol` (default is `base`)
6. `plan purchase --plan <USER_CHOSEN> --json` — x402 purchase (real USDC payment). API Key auto-saved to config

**⚠️ Quota is CU, NOT call count**: Plan quota is measured in **Compute Units (CU)**, not API call count. Each API endpoint costs a different amount of CU per call (varies by endpoint complexity and response size). When presenting plans to the user, always use "CU" as the unit — NEVER say "calls" or "requests".

**Channel matrix:**

| Operation | MCP (when registered) | CLI | SDK |
|-----------|----------------------|-----|-----|
| Search tokens | `tokens_search` | `token search` | `client.token.search` |
| Analyze token | `tokens_analyze` | `token info` | `client.token.getToken` |
| Price history | `tokens_price_history` | `token candles` | `client.token.getCandles` |
| Wallet profile | `wallets_profile` | `wallet profile` | `client.wallet.*` |
| Market trending | `market_trending` | `market trending` | `client.ranking.*` |
| DEX quote | `dex_quote` | `dex route` | `client.dex.route` |
| DEX swap | _(no signing)_ | `dex swap` | `client.dex.swap` + sign |
| Create token | _(no signing)_ | `dex create` | `client.dex.createToken` |

## Prerequisites

### MCP path (recommended for data queries)

Add to your MCP client configuration (Cursor, Claude Desktop, VS Code):

```json
{
  "mcpServers": {
    "chainstream": {
      "url": "https://mcp.chainstream.io/mcp",
      "headers": { "X-API-KEY": "<your-api-key>" }
    }
  }
}
```

### CLI path

```bash
# Option A: Use API Key (recommended — works with all agent wallets)
npx @chainstream-io/cli config set --key apiKey --value <your-api-key>

# Option B: Create ChainStream Wallet (for DeFi + auto x402 payment)
npx @chainstream-io/cli login

# Option C: Import existing key (dev/testing)
npx @chainstream-io/cli wallet set-raw --chain base   # EVM (Base) key
npx @chainstream-io/cli wallet set-raw --chain sol     # Solana key
```

### SDK path

`npm install @chainstream-io/sdk` — see [`shared/authentication.md`](../shared/authentication.md) Path 2 for `WalletSigner` integration.

## Endpoint Selector

### Token

| Intent | CLI Command | MCP Tool | Reference |
|--------|-------------|----------|-----------|
| Search tokens | `npx @chainstream-io/cli token search --keyword X --chain sol` | `tokens_search` | [token-research.md](references/token-research.md) |
| Token detail | `npx @chainstream-io/cli token info --chain sol --address ADDR` | `tokens_analyze` | [token-research.md](references/token-research.md) |
| Security check | `npx @chainstream-io/cli token security --chain sol --address ADDR` | `tokens_analyze` | [token-research.md](references/token-research.md) |
| Top holders | `npx @chainstream-io/cli token holders --chain sol --address ADDR` | `tokens_analyze` | [token-research.md](references/token-research.md) |
| K-line / OHLCV | `npx @chainstream-io/cli token candles --chain sol --address ADDR --resolution 1h` | `tokens_price_history` | [token-research.md](references/token-research.md) |
| Liquidity pools | `npx @chainstream-io/cli token pools --chain sol --address ADDR` | `tokens_discover` | [token-research.md](references/token-research.md) |

### Market

| Intent | CLI Command | MCP Tool | Reference |
|--------|-------------|----------|-----------|
| Hot/trending tokens | `npx @chainstream-io/cli market trending --chain sol --duration 1h` | `market_trending` | [market-discovery.md](references/market-discovery.md) |
| New token listings | `npx @chainstream-io/cli market new --chain sol` | `market_trending` | [market-discovery.md](references/market-discovery.md) |
| Recent trades | `npx @chainstream-io/cli market trades --chain sol` | `trades_recent` | [market-discovery.md](references/market-discovery.md) |

### Wallet

| Intent | CLI Command | MCP Tool | Reference |
|--------|-------------|----------|-----------|
| Wallet profile (PnL + holdings) | `npx @chainstream-io/cli wallet profile --chain sol --address ADDR` | `wallets_profile` | [wallet-profiling.md](references/wallet-profiling.md) |
| PnL details | `npx @chainstream-io/cli wallet pnl --chain sol --address ADDR` | `wallets_profile` | [wallet-profiling.md](references/wallet-profiling.md) |
| Token balances | `npx @chainstream-io/cli wallet holdings --chain sol --address ADDR` | `wallets_profile` | [wallet-profiling.md](references/wallet-profiling.md) |
| Transfer history | `npx @chainstream-io/cli wallet activity --chain sol --address ADDR` | `wallets_activity` | [wallet-profiling.md](references/wallet-profiling.md) |
| Own wallet balance (base/sol) | `npx @chainstream-io/cli wallet balance --chain sol` | — | Supports `sol` and `base` (note: `base` is a payment chain, not a data chain) |

### Subscription

| Intent | CLI Command | MCP Tool | Reference |
|--------|-------------|----------|-----------|
| **Check current subscription** | `npx @chainstream-io/cli plan status` | — | [x402-payment.md](../shared/x402-payment.md) |
| Check subscription (explicit) | `npx @chainstream-io/cli plan status --chain evm --address ADDR` | — | [x402-payment.md](../shared/x402-payment.md) |
| View available plans | `npx @chainstream-io/cli wallet pricing` | — | [x402-payment.md](../shared/x402-payment.md) |
| **Purchase plan (non-interactive)** | `npx @chainstream-io/cli plan purchase --plan <NAME> --json` | — | [x402-payment.md](../shared/x402-payment.md) |
| Check subscription (API) | `curl "https://api.chainstream.io/x402/status?chain=evm&address=ADDR"` | — | [x402-payment.md](../shared/x402-payment.md) |

## Quickstart

```bash
npx @chainstream-io/cli login                                              # Auth (one-time)
npx @chainstream-io/cli token search --keyword PUMP --chain sol            # Search tokens
npx @chainstream-io/cli token info --chain sol --address <addr> --json     # Token detail (single-line JSON for piping)
```

All commands from the Endpoint Selector tables above work after `login`. Append `--json` for machine-readable output.

**Default limit**: All list queries (`token search`, `token holders`, `token candles`, `market trending`, `market new`, `market trades`, `wallet holdings`, `wallet activity`) default to **5 results**. Pass `--limit <n>` to override (e.g. `--limit 20`).

## AI Workflows

### Token Research Flow

```
npx @chainstream-io/cli token search → npx @chainstream-io/cli token info → npx @chainstream-io/cli token security
→ npx @chainstream-io/cli token holders → npx @chainstream-io/cli token candles
```

Before recommending any token, always run `token security` — ChainStream's risk model covers honeypot, rug pull, mint authority, freeze authority, and holder concentration.

### Market Discovery Flow

**MANDATORY - READ**: Before executing this workflow, load [`references/market-discovery.md`](references/market-discovery.md) for the multi-factor signal weight table and output format.

```
npx @chainstream-io/cli market trending (top 50)
→ AI multi-factor analysis (smart money, volume, momentum, safety)
→ npx @chainstream-io/cli token security (top 5 candidates)
→ Present results to user
→ If user wants to trade → load chainstream-defi skill
```

**Do NOT load** wallet-profiling.md for this workflow.

### Wallet Profiling Flow

**MANDATORY - READ**: Load [`references/wallet-profiling.md`](references/wallet-profiling.md) for PnL interpretation and behavior patterns.

```
npx @chainstream-io/cli wallet profile → npx @chainstream-io/cli wallet activity
→ npx @chainstream-io/cli token info (on top holdings)
→ Assess: win rate, concentration, holding behavior
```

## NEVER Do

- NEVER answer "what's the price of X" from training data — always make a live CLI/API call; crypto prices are stale within seconds
- NEVER skip `token security` before recommending a token — ChainStream's risk model covers honeypot, rug pull, and concentration signals that generic analysis misses
- NEVER pass `format: "detailed"` to MCP tools unless user explicitly requests it — returns 4-10x more tokens than default `concise`, wastes context window
- NEVER batch more than 50 addresses in `/multi` endpoints — API hard limit
- NEVER use public RPC or third-party data providers as substitutes — results differ and miss ChainStream-specific enrichments (security scores, smart money tags)
- NEVER omit `--limit` on list queries — CLI defaults to 5 results to prevent context overflow. If the user needs more, pass `--limit <n>` explicitly (e.g. `--limit 20`)
- NEVER run data commands (token/market/wallet) without ensuring user is logged in and has an active subscription — run `config auth` → `login` (if needed) → `plan status` first. New users get a free nano trial on login; only run `plan purchase` if the trial is exhausted or absent

## Error Recovery

| Error | Meaning | Recovery |
|-------|---------|----------|
| "Not authenticated" / 401 / 402 | Not logged in, no API Key, or no active subscription | Follow the 401/402 sequence below |
| 429 | Rate limit | Wait 1s, exponential backoff |
| 5xx | Server error | Retry once after 2s |

On 401/402, follow this exact sequence:
1. **Check login**: `npx @chainstream-io/cli config auth` — if not logged in, run `npx @chainstream-io/cli login` (creates wallet + auto-grants nano trial with 50K CU free). After login, retry the failed command — it will likely succeed now
2. **Check subscription**: `npx @chainstream-io/cli plan status` — if `active: true` with remaining quota, the issue is likely a transient auth error; retry
3. **If logged in but no subscription**: ask the user "Do you have a ChainStream API Key?" — if yes, `config set --key apiKey --value <key>` and retry; if no, run `npx @chainstream-io/cli wallet pricing`, **present ALL plans to the user**, let them choose, then load [`shared/x402-payment.md`](../shared/x402-payment.md) for the purchase flow. **NEVER auto-select a plan. NEVER try to pipe input to interactive CLI prompts.**

## Skill Map

| Reference | Content | When to Load |
|-----------|---------|--------------|
| [token-research.md](references/token-research.md) | 25+ token endpoints, batch queries, security field meanings | Token analysis tasks |
| [market-discovery.md](references/market-discovery.md) | Ranking/trade endpoints, multi-factor discovery workflow | Hot token discovery |
| [wallet-profiling.md](references/wallet-profiling.md) | 15+ wallet endpoints, PnL logic, behavior patterns | Wallet analysis |
| [websocket-streams.md](references/websocket-streams.md) | Channels, subscription format, heartbeat | Real-time streaming |

## Related Skills

- [chainstream-graphql](../chainstream-graphql/) — When standard REST/MCP endpoints aren't enough: custom GraphQL queries with cross-cube JOINs, aggregations, and complex filters on 27 on-chain cubes
- [chainstream-defi](../chainstream-defi/) — When analysis leads to action: swap, launchpad, transaction signing and broadcast
