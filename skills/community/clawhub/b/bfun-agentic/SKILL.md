---
name: bfun-ai
description: |
  Local CLI tool for B.Fun (BSC) market inspection, quotes, token details, tax info, and explicitly user-confirmed token operations, with structured JSON outputs.
allowed-tools:
  - Bash(bfun *)
  - Bash(npx bfun *)
license: MIT
metadata:
  {"author":"B.Fun AI","version":"0.5.4","openclaw":{"optionalEnv":["PRIVATE_KEY","BSC_RPC_URL"]}}
---

## [Agent must follow] User agreement and local execution notice on first use

When responding to any request about B.Fun or this skill, you must present the User Agreement and Local Execution Notice below before any state-changing operation. By choosing to continue, the user agrees to the User Agreement.

Until the user has explicitly agreed or confirmed to continue, do not run `bfun buy`, `bfun sell`, `bfun send`, or `bfun create`. Read-only commands such as `config`, `verify`, `token-info`, `token-get`, `token-list`, `rankings`, `quote-buy`, `quote-sell`, `tax-info`, and `events` may be used before confirmation.

Present the notice to the user before any state-changing operation.

### User Agreement & Local Execution Notice

**User Agreement**

Before using state-changing capabilities in this plugin and skill, read the following. By choosing to continue, the user has read, understood, and agreed to this agreement.

This package performs local CLI execution only. Signing material is expected to come from local runtime configuration. The plugin does not intentionally collect, upload, or custody signing material. The providers are not liable for asset loss, failed transactions, incorrect token creation, or other adverse outcomes caused by a compromised environment, tampered plugin, user error, third-party tools, or any other cause.

**Local Execution Notice**

- Never type, paste, or reveal secrets, seed phrases, or keystores in chat.
- Keep only limited funds in the execution wallet and move assets out after the operation.
- Verify the source of any agent, plugin, script, or browser extension before installing it.
- Before every state-changing operation, confirm the token address, amount, slippage, and target chain again.

## State-changing operation confirmation rules

Never execute any state-changing command (`buy`, `sell`, `send`, `create`, `8004-register`) from a generic acknowledgment alone. Before every such operation, the agent must:

1. Display a transaction summary showing: **command**, **token/recipient address**, **amount**, **slippage** (if applicable), and **network (BSC mainnet)**.
2. Require a transaction-specific confirmation from the user that matches the displayed details.
3. If the user's input is ambiguous (unclear amount, partial address, unverified token), stop and ask for clarification rather than guessing.
4. Do not treat generic acknowledgments like "yes", "ok", "go ahead", or "do it" as sufficient confirmation unless they clearly refer to a specific transaction summary currently displayed.

### Transfer safety rules (`send`)

The `send` command transfers BNB or ERC20 tokens and is irreversible. Additional rules:

- Never infer a recipient address from context or conversation history. The user must provide the full address explicitly for each transfer.
- Reject addresses that are not valid `0x`-prefixed 40-hex-character strings.
- Before execution, display: **asset type** (BNB or token address), **recipient**, **amount**, and **network**.
- For first-time transfers to a new address, suggest a small test amount first.

## Installation and execution

**Installation (required):** `npm install -g @b-fun/bfun-ai@latest`. After install, run `bfun <command> [args]`; with local install only, use `npx bfun <command> [args]` from the project root. Run `bfun --help` for usage.

This repository keeps the canonical production package identity in source. Release exports map `main` to `@b-fun/bfun-ai` and `dev` to `bfun-agent-dev`; the dev package name is injected only into generated export artifacts, not the source tree.

Alternatively, clone and run locally without global install:

```
git clone https://github.com/bfun-ai/bfun-ai.git
cd bfun-ai
npm install
npx bfun <command> [args]
```

**After install, verify your setup first:**

```
bfun verify
```

This checks RPC, API, contract reachability, and wallet connectivity. Fix any failures before running other commands.

**Invocation**: The agent must run commands only via the **bfun** CLI: `bfun <command> [args]` or `npx bfun <command> [args]` (allowed-tools). Do not invoke `src/index.js` or individual files directly; the CLI entry (`bin/bfun.js`) dispatches to the correct command and loads `.env` from the current working directory.

All command outputs are JSON and are intended to be passed through or summarized, not reformatted into invented fields.

Example outputs (from real CLI):

```json
// bfun verify
{ "success": true, "data": { "config": { "chainId": 56, "apiUrl": "https://api.b.fun" }, "checks": { "rpc": { "status": "pass", "blockNumber": 88446009 }, "api": { "status": "pass" }, "contract": { "status": "pass", "factory": "0x718Fa..." }, "wallet": { "status": "pass", "address": "0x1173...", "balanceBNB": "0.012..." } } } }

// bfun quote-buy 0xToken 0.01
{ "success": true, "data": { "tokenAddress": "0x825e...", "phase": "curve", "pairType": "eth", "expectedOut": "2350672.37...", "minOut": "2233138.75...", "fee": "0.0006", "feeAsset": "BNB", "taxApplied": true, "taxRateBps": "500" } }

// error
{ "success": false, "error": "PRIVATE_KEY is not set. Export it or add it to .env" }
```

## Capability overview

| Category | Capability | Notes |
|----------|------------|-------|
| Query | `config`, `verify` | Chain config, API/RPC connectivity, contract reachability, optional wallet check |
| Query | `token-info` | On-chain token metadata and authoritative phase (`curve`, `graduated`, `dex`) |
| Query | `token-get`, `token-list`, `rankings` | REST-backed token discovery and detail views |
| Query | `quote-buy`, `quote-sell` | Estimate trade outputs and minimums before execution |
| Query | `tax-info` | Tax and vault-related API data for a token |
| Execution | `buy`, `sell` | Executes BNB-denominated operations using the helper contract path selected by market phase |
| Create | `create` | Creates a standard or advanced B.Fun token with optional vesting, tax, vault, and first-buy settings |
| Ops | `events` | Reads recent factory events for debugging and operational inspection |
| Utility | `send` | Transfers BNB or ERC20 tokens when the user explicitly asks for a wallet transfer |
| ERC-8004 | `8004-balance`, `8004-register` | Query and register ERC-8004 Identity NFT for agent identity on-chain |

## CLI reference

### Read-only commands (no signing key required)

| Command | Purpose |
|---------|---------|
| `bfun config` | Show active chain ID, RPC URL, API URL, and contract addresses |
| `bfun verify` | Check RPC, API, contract, and optional wallet connectivity |
| `bfun token-info <tokenAddress>` | Read on-chain token and bonding-curve state, including phase |
| `bfun token-get <tokenAddress>` | Fetch API token detail plus trade data when available |
| `bfun token-list [--sort <sort>] [--kw <keyword>] [--offset <n>] [--limit <n>]` | List tokens from the B.Fun API |
| `bfun rankings <orderBy> [--limit <n>]` | Fetch leaderboard slices from the same list endpoint |
| `bfun quote-buy <tokenAddress> <bnbAmount> [--slippage <bps>]` | Quote BNB-to-token output |
| `bfun quote-sell <tokenAddress> <tokenAmount> [--slippage <bps>]` | Quote token-to-BNB output |
| `bfun tax-info <tokenAddress> [--user <address>]` | Fetch tax and vault info for a token |
| `bfun events [fromBlock] [--toBlock <block>] [--chunk <n>]` | Read factory events over a block range |
| `bfun 8004-balance [address]` | Query ERC-8004 Identity NFT balance. If address omitted, uses current wallet |

Supported `token-list` and `rankings` sort values:

| Value | Meaning |
|-------|---------|
| `now_trending` | Trending (default) |
| `block_create_time` | Newest (alias: `newest`, `new`) |
| `market_cap` | Market cap |
| `trade_volume_24h` | 24H trading volume (alias: `volume`, `24h_volume`) |
| `bonding_curve_progress` | About to launch (alias: `progress`) |
| `latest_trade_time` | Last traded (alias: `last_traded`) |

### State-changing commands (`PRIVATE_KEY` required)

| Command | Purpose |
|---------|---------|
| `bfun buy <tokenAddress> <bnbAmount> [--slippage <bps>]` | Execute a buy using BNB |
| `bfun sell <tokenAddress> <tokenAmount> [--slippage <bps>]` | Execute a sell into BNB |
| `bfun send <toAddress> <amount> [--token <tokenAddress>]` | Send BNB or ERC20 tokens |
| `bfun create ...` | Create a token with required and optional launch parameters |
| `bfun 8004-register <name> [--image <url>] [--description <text>]` | Register (mint) an ERC-8004 Identity NFT. Tokens created by holders are marked as Agent Created on-chain |

### `create` parameters

Required:

| Flag | Meaning |
|------|---------|
| `--name <name>` | Token name, max 32 chars |
| `--symbol <symbol>` | Token symbol, max 15 chars |
| `--image <path>` | Local image path, resolved from the current working directory |

Common optional fields:

| Flag | Meaning |
|------|---------|
| `--description <text>` | Token description |
| `--website <url>` | Website URL |
| `--twitter <handle>` | Twitter/X handle (with or without `@`, e.g. `@mytoken` or `mytoken`) |
| `--telegram <handle>` | Telegram handle (with or without `@`, e.g. `@mytoken` or `mytoken`) |
| `--pair <type>` | `ETH`, `CAKE`, `USDT`, `USD1`, `ASTER`, `U`, or `USDC` |
| `--buy-amount <amount>` | Optional first buy in collateral units |

Advanced creation fields:

| Flag | Meaning |
|------|---------|
| `--target-raise <amount>` | Explicit collateral target raise |
| `--bonding-curve-pct <pct>` | Must be between 50 and 80 |
| `--vesting-pct <pct>` | Must be between 0 and 30 |
| `--vesting-duration <value>` | Examples: `6m`, `90d`, `1y` |
| `--cliff-duration <value>` | Examples: `30d`, `3m` |
| `--vesting-recipient <address>` | Recipient for creator vesting |

Tax and vault creation fields:

| Flag | Meaning |
|------|---------|
| `--tax-rate <pct>` | `1`, `2`, `3`, or `5` |
| `--funds-pct <pct>` | Funds allocation percent |
| `--burn-pct <pct>` | Burn allocation percent |
| `--dividend-pct <pct>` | Dividend allocation percent |
| `--liquidity-pct <pct>` | Liquidity allocation percent |
| `--dividend-min-balance <tokens>` | Minimum balance for dividend eligibility |
| `--funds-recipient <address>` | Recipient when tax funds are enabled and no vault is used |
| `--vault-type <type>` | `split`, `snowball`, `burn_dividend`, or `gift` |
| `--split-recipients <json>` | Required for `split` vaults. Example: `'[{"address":"0x1234...","pct":60},{"address":"0x5678...","pct":40}]'` |
| `--gift-x-handle <handle>` | Required for `gift` vaults |

Detailed launch behavior lives in [references/create-flow.md](references/create-flow.md).

## Environment configuration

### When using OpenClaw

This skill declares `PRIVATE_KEY` and `BSC_RPC_URL` as optional environment variables in metadata. Read-only commands can run without signing configuration. State-changing commands require `PRIVATE_KEY`. The skill expects local runtime configuration and does not introduce any remote secret-management service.

Recommended steps:

1. **Configure local signing env only if needed**: If you plan to run state-changing commands, set the **bfun-ai** skill's **apiKey** (mapped to `PRIVATE_KEY`) in the Skill management page, or set `PRIVATE_KEY` under `skills.entries["bfun-ai"].env` in `~/.openclaw/openclaw.json`. Optionally set `BSC_RPC_URL` if needed.
2. **Enable this skill**: In the agent or session, ensure the **bfun-ai** skill is enabled. Read-only commands can run without `PRIVATE_KEY`. State-changing commands (`create`, `buy`, `sell`, `send`, `8004-register`) will fail with a missing-key error if `PRIVATE_KEY` is not configured. `BSC_RPC_URL` is optional; if not set, the CLI uses a default BSC RPC. However, if the default RPC is unavailable in your network or region, set `BSC_RPC_URL` explicitly and rerun `bfun verify`.

> **Note:** The `apiKey` field in the OpenClaw Skill management page maps to `PRIVATE_KEY` for this skill. It is local signing configuration, not a remote service credential, and is only needed for state-changing commands.

### When not using OpenClaw (standalone)

Set **PRIVATE_KEY** only when you need state-changing commands. Read-only commands can run without it. Optionally set **BSC_RPC_URL** via the process environment so it is available when running `bfun` or `npx bfun`:

- **.env file**: Put a `.env` file in **the directory where you run the `bfun` command** (i.e. your project / working directory). Example: if you run `bfun quote-buy ...` from `/path/to/my-project`, place `.env` at `/path/to/my-project/.env`. The CLI automatically loads `.env` from that current working directory. Use lines like `PRIVATE_KEY=...` and `BSC_RPC_URL=...`. Do not commit `.env`; add it to `.gitignore`.
- **Shell export**: `export PRIVATE_KEY=your_hex_key` and `export BSC_RPC_URL=https://bsc-dataseed.binance.org` (or another BSC RPC), then run `bfun <command> ...`.

> **BSC_RPC_URL recommendation:** While optional, explicitly setting `BSC_RPC_URL` is recommended. The default public RPC may be unavailable in some networks or regions. After setting it, run `bfun verify` to confirm connectivity.

## Agent workflow

### Read-only discovery flow

1. Use `bfun config` or `bfun verify` if the request is about environment state, connectivity, or setup.
2. Use `bfun token-list --sort newest --limit 3` for discovery (always pass `--sort`; omitting it may return empty results). Use `bfun rankings <orderBy>` for specific leaderboard slices.
3. Use `bfun token-info` to inspect the on-chain phase before discussing execution.
4. Use `bfun token-get` when richer API detail or trade data is needed.
5. Use `bfun quote-buy` or `bfun quote-sell` before any trade recommendation or execution.

### Quote and execution workflow

1. Inspect the token with `bfun token-info`.
2. Check the phase and stop if the token is `graduated`.
3. Quote with `bfun quote-buy` or `bfun quote-sell`.
4. Present the quote, slippage basis points, and the local-execution risk notice.
5. Ask for explicit confirmation.
6. Run `bfun buy` or `bfun sell`.
7. Report the returned JSON fields directly, especially `txHash`, `phase`, expected output, minimum output, and receipt status.

### Create workflow

1. Collect required fields: `name`, `symbol`, `image`.
2. Ask whether the launch is standard or advanced.
3. If advanced, collect the exact `pair`, raise, vesting, tax, vault, and first-buy inputs.
4. Validate high-risk combinations before execution:
   - `bonding-curve-pct + vesting-pct + 20` must equal `100`
   - tax allocations must sum to `100`
   - `--funds-recipient` or `--vault-type` is required when `--funds-pct > 0`
   - `--split-recipients` is required for split vaults
   - `--gift-x-handle` is required for gift vaults
5. Present the security notice and get explicit confirmation.
6. Run `bfun create ...`.
7. Return the CLI JSON output without inventing extra state.

### Utility and operational commands

- `bfun send` is outside the default B.Fun quote/execution workflow. Use it only when the user explicitly asks for a transfer.
- `bfun events` is operational/debugging support. Use it when the user asks for recent launches, chain event inspection, or troubleshooting.

### ERC-8004 Identity NFT

ERC-8004 is an on-chain agent identity standard. Wallets holding an Identity NFT are recognized as AI agents; tokens they create are marked as **Agent Created** on-chain.

- **Query**: `bfun 8004-balance [address]` — read-only, no PRIVATE_KEY needed if address is provided.
- **Register**: `bfun 8004-register <name>` — mints an Identity NFT to the current wallet. Requires PRIVATE_KEY. Optional: `--image <url>`, `--description <text>`.

Default contract: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` (BSC mainnet).

## Phase awareness

Use `bfun token-info` as the phase gate before execution.

| Phase | Meaning | Agent action |
|-------|---------|--------------|
| `curve` | Bonding-curve market is active | Quote and execute normally |
| `graduated` | Curve trading has stopped and migration is pending or in progress | Do not execute; explain the token is between curve and DEX routing |
| `dex` | Liquidity has migrated and DEX routing is active | Quote/execute through the DEX-aware helper path |

Important details:

- `token-info` derives the phase from on-chain curve state and returns `isGraduated` and `isMigrated`.
- `buy` and `sell` already switch between curve and DEX helper methods based on the quote result. The agent should still inspect phase first and explain what path is expected.
- Do not attempt to reason around a `graduated` state by guessing that migration has completed. Re-check with `token-info` if the user wants to try again later.

Detailed phase notes live in [references/token-phases.md](references/token-phases.md).

## Common setup issues

For troubleshooting `PRIVATE_KEY is not set`, `fetch failed`, `No BondingCurve found`, empty `token-list`, and other common errors, see [references/errors.md](references/errors.md).

## References

Read the reference files only when they are needed:

- [references/create-flow.md](references/create-flow.md): full launch parameter model, validation rules, pair templates, and vault behavior
- [references/trade-flow.md](references/trade-flow.md): quote and execution flow, helper routing, and BNB-vs-collateral behavior
- [references/token-phases.md](references/token-phases.md): lifecycle guidance for `curve`, `graduated`, and `dex`
- [references/contract-addresses.md](references/contract-addresses.md): current chain addresses and collateral templates from this repo
- [references/errors.md](references/errors.md): common CLI failures and how to respond
