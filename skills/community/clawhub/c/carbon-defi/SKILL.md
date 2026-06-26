---
name: carbon-defi
description: >
  Use this skill when the user wants to create or manage on-chain maker trading
  strategies on Carbon DeFi. Triggers include: "place a limit order", "create a
  recurring strategy", "buy ETH at a specific price", "set up a DCA strategy",
  "manage my Carbon strategies", "pause/resume/reprice a strategy", "deposit or
  withdraw from a strategy", "full range liquidity", "provide liquidity and earn fees",
  or any mention of Carbon DeFi, maker orders, or on-chain automated trading strategies
  on Ethereum, Sei, Celo, TAC, or COTI.
allowed-tools: Bash(curl *)
---

# Carbon DeFi — On-Chain Maker Trading via MCP

Carbon DeFi is a fully on-chain maker trading protocol. Users set prices upfront — strategies execute automatically with zero gas on fills. No bots, no agent needs to stay online after placing a strategy.

## Connect to the MCP Server

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "carbon-defi": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.carbondefi.xyz/mcp"]
    }
  }
}
```

Restart Claude Desktop after saving. Alternatively, call tools directly via REST:

```bash
curl -X POST https://mcp.carbondefi.xyz/tools/get_strategies \
  -H "Content-Type: application/json" \
  -d '{"owner": "0xYourAddress", "chain": "ethereum"}'
```

## Core Concepts

**Maker-first.** Every strategy is a maker order — you set the price, the market comes to you.

**Unsigned transactions.** All write operations return an unsigned transaction (`to`, `data`, `value`). The user must sign and broadcast it. Never assume a transaction has been submitted.

**Base and quote tokens.**
- `base_token` — the token being bought or sold (e.g. ETH)
- `quote_token` — the pricing token (e.g. USDC)
- All prices are expressed as: **quote per 1 base** (e.g. 2000 USDC per ETH)

**Budgets.**
- `buy_budget` — always in quote token (e.g. USDC to spend buying ETH)
- `sell_budget` — always in base token (e.g. ETH to sell)

**Native ETH.** Use address `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`. Never WETH. ETH never requires approval.

**Supported chains.** `ethereum`, `sei`, `celo`, `tac`, `coti`

## Strategy Types

| User intent | Tool to use |
|---|---|
| "buy at exactly X" / "sell at exactly X" | `carbon_create_limit_order` |
| "scale in as price drops" / "DCA into" | `carbon_create_range_order` (buy) |
| "scale out as price rises" / "sell gradually" | `carbon_create_range_order` (sell) |
| "buy low sell high forever" / "recurring" / "grid" | `carbon_create_recurring_strategy` |
| "provide liquidity" / "earn fees" / "concentrated" | `carbon_create_concentrated_strategy` |
| "full range liquidity" / "widest range" | `carbon_create_full_range_strategy` |

A range order executes gradually as price moves through the range — correct for "scale in" or "DCA". Do not split into multiple orders.

## All 25 Tools

### Explore
- `carbon_get_strategies` — all active strategies for a wallet. **Always call first.**
- `carbon_get_strategy` — single strategy by ID — type, status, prices, budgets, trade count
- `carbon_get_activity` — trade and event history for a wallet or strategy
- `carbon_explore_pair` — top strategies for a token pair, ranked by trade count
- `carbon_simulate_strategy` — backtest against real historical prices before going on-chain
- `carbon_resolve_token` — fuzzy token symbol/name → on-chain address ("dollar" finds USDC/USDT/DAI)
- `carbon_find_opportunities` — discount buys or premium sells vs market price
- `carbon_get_protocol_stats` — TVL, volume, fees history
- `carbon_get_price_history` — OHLC price data for any token pair

### Trade (swap against Carbon liquidity)
- `carbon_get_trade_quote` — swap quote: expected output, rate, strategies used. Always call before execute.
- `carbon_execute_trade` — unsigned swap transaction. Requires `trade_actions` from `get_trade_quote`.

### Create
- `carbon_create_limit_order` — one-time buy or sell at exact price
- `carbon_create_range_order` — gradual execution across a price range
- `carbon_create_recurring_strategy` — looping buy+sell, repeats forever, zero gas on fills
- `carbon_create_concentrated_strategy` — two-sided liquidity with a defined spread
- `carbon_create_full_range_strategy` — two-sided liquidity up to 1000x from market price

### Manage
- `carbon_reprice_strategy` — update price ranges only
- `carbon_edit_strategy` — update prices and budgets in one transaction
- `carbon_deposit_budget` — add funds without interrupting the strategy
- `carbon_withdraw_budget` — remove funds without closing the strategy
- `carbon_pause_strategy` — pause orders, funds stay, resume anytime
- `carbon_resume_strategy` — reactivate a paused strategy
- `carbon_delete_strategy` — permanently close and return all funds

### Help & Knowledge
- `carbon_help` — detailed guidance on any tool or full overview
- `carbon_learn` — protocol concepts: fees, security, marginal price, overlapping liquidity, contracts, SDK, API, and more

## Behavior Rules

1. Always call `carbon_get_strategies` first to check existing positions
2. Never invent a market price — always ask the user. Never reuse a price from earlier in the conversation.
3. Present a strategy proposal and wait for explicit user approval before building a transaction
4. Always show the full unsigned transaction (`to`, `data`, `value`) after creation
5. Check the `warnings` array in every response — if allowance warning exists, show approval steps before the transaction
6. When market price is inside a buy range, ask: full range or below market only?
   - Full range: omit `buy_price_marginal`
   - Below market only: set `buy_price_marginal` to current market price
7. Overlapping buy/sell ranges: warn but allow — ask user to confirm intent
8. Buy price above market: warn and offer to adjust
9. Sell price below market: warn and offer to adjust
10. For pause: show current prices first, confirm before pausing
11. For resume: restore prices only — funds already in strategy, never ask for budgets
12. For reprice: call once with all four prices — fill missing side from current strategy state
13. For delete: always confirm with user — irreversible

## Token Allowances

Before any strategy depositing ERC-20 tokens, check if the Carbon DeFi controller has sufficient allowance. If not, the user must send an approval transaction first.

> Note: USDT on Ethereum requires setting allowance to 0 before increasing.

## Transaction Verification

All write operations return unsigned transactions. To independently verify calldata before signing:
- Spec: https://docs.carbondefi.xyz/developer-guides/carbon-defi-transaction-encoding
- Covers: contract addresses per chain, function selectors, price encoding, budget encoding, verification checklist

## Batch API

Run multiple tools in parallel as a single request (counts against rate limit once):

```bash
curl -X POST https://mcp.carbondefi.xyz/batch \
  -H "Content-Type: application/json" \
  -d '[
    {"tool": "get_strategies", "params": {"owner": "0x...", "chain": "ethereum"}},
    {"tool": "get_protocol_stats", "params": {"chain": "ethereum"}}
  ]'
```

## Rate Limits

- 30 requests/min per IP, burst of 10
- Use `/batch` for parallel calls — counts as 1 request
- REST endpoints (`/tools/:toolName`) are faster than MCP proxy

## Links

- App: https://app.carbondefi.xyz
- Docs: https://docs.carbondefi.xyz
- AI Agents & MCP: https://docs.carbondefi.xyz/ai-agents-and-mcp-integration
- MCP endpoint: https://mcp.carbondefi.xyz/mcp
- OpenAPI spec: https://mcp.carbondefi.xyz/openapi.json
- Litepaper: https://carbondefi.xyz/litepaper
