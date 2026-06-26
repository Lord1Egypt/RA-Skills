---
name: aiusd-core
version: 1.0.1
description: "AIUSD Core — structured trading tools and account management for AI agents. Use when user wants to buy/sell assets, check balances, stake, or manage positions."
homepage: https://aiusd.ai
license: MIT
compatibility: "Requires node >= 18"
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: ["node"]
---

# AIUSD Core

AIUSD Core is a unified trading toolkit that lets agents trade across venues, manage perpetual futures, access prediction markets, earn yield by staking, and manage funds — all through a single CLI.

## CLI entry point

All commands in this skill use `npx -y aiusd-core` as the CLI prefix. This works without any global installation — npx resolves the package from npm automatically.

If `aiusd-core` is already in PATH (via `npm install -g aiusd-core`), you may use `aiusd-core` directly instead.

**NEVER use `dist/cli.js` — it is a library module, not an entry point.**

## When to use this skill

Trigger this skill when the user wants to:

- **Trade** — buy, sell, or swap any asset across supported venues
- **Perpetual futures** — long, short, or close positions with leverage, TP/SL
- **Prediction markets** — trade on event outcomes, search markets, manage positions
- **Account & funds** — check balances, deposit, withdraw, stake AIUSD for yield
- **Market intelligence** — trending assets, price feeds, holder analysis
- **Automated trading** — monitor signals, set conditional execution rules

## Authentication

When a user wants to get started or is not yet logged in, present 2 options:

1. **Create new account** — set up a fresh wallet
2. **Browser login** — sign in with an existing account via browser

Map the user's choice to the corresponding CLI flag:
- **Create new account** → `npx -y aiusd-core login --new-wallet`. The CLI creates a wallet, authenticates, and prints a JSON `auth_event` with the wallet address.
- **Browser login** → two-step flow:
  1. Run `npx -y aiusd-core login --browser`. The CLI prints a JSON with `url` and `session_id`, then **exits immediately**. Send the `url` to the user — **NEVER fabricate or guess it**.
  2. After sending the URL, run `npx -y aiusd-core login --poll-session <session_id>`. This blocks until the user signs in, then saves the token and exits with "Login successful".
- **Restore from backup** → `npx -y aiusd-core login --restore <path>`. Only use when the user explicitly asks to restore from a mnemonic file.

| Command | Description |
|---------|------------|
| `npx -y aiusd-core login --new-wallet` | Create new wallet and authenticate |
| `npx -y aiusd-core login --browser` | Print browser login URL and exit |
| `npx -y aiusd-core login --poll-session <id>` | Wait for browser sign-in to complete |
| `npx -y aiusd-core login --restore <path>` | Restore from mnemonic backup file |
| `npx -y aiusd-core login` | Interactive prompt (fallback for manual use) |
| `npx -y aiusd-core logout` | Sign out and remove stored token |

To switch account: `npx -y aiusd-core logout`, then `npx -y aiusd-core login --browser` (or `--new-wallet`).

## Capabilities

Before executing commands in a domain, run `npx -y aiusd-core guide <domain>` to get the latest commands, parameters, and workflows. Follow the guide exactly.

| Domain | What it covers | Trigger phrases | Guide |
|--------|---------------|-----------------|-------|
| account | Balances, deposit addresses, transaction history, staking, withdrawals, gas top-up | "balance", "deposit", "withdraw", "stake", "transactions", "how much do I have" | `npx -y aiusd-core guide account` |
| spot | Buy/sell/swap any asset on supported venues | "buy SOL", "sell ETH", "swap TRUMP", "trade", "convert AIUSD to USDC" | `npx -y aiusd-core guide spot` |
| perp | Perpetual futures — long, short, close, deposit/withdraw, orderbook, trade history | "long ETH", "short BTC", "close position", "leverage", "futures", "perps" | `npx -y aiusd-core guide perp` |
| hl-spot | HyperLiquid spot trading — buy/sell on HL spot market | "buy HYPE", "HL spot", "HyperLiquid spot" | `npx -y aiusd-core guide hl-spot` |
| prediction | Polymarket — search markets, buy/sell shares, manage orders and positions | "bet on", "prediction", "Polymarket", "will X happen", "election odds" | `npx -y aiusd-core guide prediction` |
| monitor | Watch signals for trade execution, set conditional auto-buy orders | "monitor @elonmusk", "watch account", "auto-buy", "conditional order" | `npx -y aiusd-core guide monitor` |
| market | Trending assets, price feeds, holder analysis | "trending", "hot tokens", "market data", "stock prices", "holders" | `npx -y aiusd-core guide market` |

Fallback: if `npx -y aiusd-core guide` is unreachable, refer to static files in `skills/` directory.

## Domain Knowledge

### AIUSD is not a token

AIUSD is a centralized balance pegged 1:1 to USDT. It is not a tradeable token — there is no contract address or on-chain balance to query. AIUSD can be used to trade any asset on supported venues. The conversion path is handled internally by the CLI; do not attempt to orchestrate it manually.

### Always guide before operate

Do not guess command syntax or parameters from memory. Before executing commands in any domain, run `npx -y aiusd-core guide <domain>` to get the current reference. Guides may change between CLI versions.

### Asset names can be ambiguous

The same asset symbol may exist on multiple venues. When the user's intent is ambiguous, ask which venue before executing. If the user has a clear preference from context (e.g., "buy SOL" implies Solana), proceed without asking.

### Follow `next_steps`, don't re-confirm

When a command returns `action_required` with `next_steps`, execute those steps directly. The user has already confirmed the intent — do not ask again unless the next step involves a different action than what was originally requested.

## Rules

1. Always confirm trades with the user before executing.
2. Never expose internal details (JSON responses, tool names, file paths) to users.
3. Present results in clear, conversational language.
