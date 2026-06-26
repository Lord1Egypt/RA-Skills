---
name: chainstream-defi
description: "[FINANCIAL EXECUTION] Execute irreversible on-chain DeFi operations via CLI and MCP tools. Use when user wants to swap tokens, create tokens on launchpad, sign transactions, broadcast signed transactions, or execute trading strategies. Requires explicit user confirmation before every destructive operation. All transactions are real and irreversible. Keywords: swap, DEX, launchpad, transaction, trade, sign, broadcast, PumpFun, Jupiter, Uniswap, USDC, SOL, execute."
---

# ChainStream DeFi

Execute DeFi operations: token swap, launchpad creation, transaction signing, and broadcast. All operations are **real, irreversible on-chain transactions**.

> **Before any swap**: load [chainstream-data](../chainstream-data/) and run `token security` on the target token. NEVER swap a token you haven't safety-checked.

- **CLI**: `npx @chainstream-io/cli`
- **MCP Server**: `https://mcp.chainstream.io/mcp` (streamable-http)

## Financial Risk Notice

**Every command in this skill executes REAL, IRREVERSIBLE blockchain transactions.**

- Transactions cannot be undone once confirmed on-chain.
- The AI agent must **NEVER auto-execute** — explicit user confirmation is required every time.
- Only use with funds the user is willing to trade.

## Integration Path (check FIRST)

DeFi operations **require a wallet**. API Key alone is insufficient.

**Before anything else (CLI path), ensure user is authenticated:**
1. `npx @chainstream-io/cli config auth` — check login status
2. If NOT logged in → `npx @chainstream-io/cli login` (creates EVM + Solana wallet, auto-grants **nano trial plan: 50K CU free, 30 days** — no purchase needed)
3. `npx @chainstream-io/cli plan status` — verify subscription is active

**New users get a free trial on login (50K CU).** For details on trial plans and upgrade options, see [`shared/authentication.md`](../shared/authentication.md#agent-bootstrap-checklist).

**Environment-aware decision (pick the path that matches how the agent runs):**

1. **Agent already has a wallet (`WalletSigner`)?**
   → **Use SDK** (`@chainstream-io/sdk`). Do NOT use CLI for signing. Implement `WalletSigner` interface. Your wallet must also support `signTypedData` for x402 payment.

2. **No embedded wallet — local terminal or CI available?**
   → **Use CLI** (`npx @chainstream-io/cli`). **Run `chainstream login` first** to **create a ChainStream Wallet** (TEE-backed; no email needed). CLI handles transaction signing; for x402 subscription, run `plan purchase --plan <name>` separately.

3. **Using MCP (streamable HTTP, e.g. `https://mcp.chainstream.io/mcp` — `dex/swap`, …)?**
   → **Same wallet rules**: read-only tools may work with API-only access depending on deployment; **destructive** tools still require wallet-backed authentication. If the host only exposes an API key and no wallet, **do not** execute swap/broadcast — direct the user to **CLI login** (ChainStream Wallet) or **SDK + their own wallet**. MCP does not remove the wallet requirement for on-chain execution.

4. **Only API Key?**
   → Cannot execute wallet-gated DeFi (swap, broadcast, etc.). Tell user: "DeFi requires a wallet. Use SDK with your wallet or run `npx @chainstream-io/cli login`."

For full auth guide with code examples, see [shared/authentication.md](../shared/authentication.md).

## Prerequisites (CLI path)

**All DeFi commands require a wallet. If you see "Not authenticated" or "Wallet required", run:**

```bash
npx @chainstream-io/cli login
```

## CLI Wallet & Signing Commands

**The CLI has built-in wallet management and signing capabilities.** These commands are ALREADY IMPLEMENTED and WORKING:

### Wallet Commands

```bash
# Show configured wallet addresses
npx @chainstream-io/cli wallet address

# Show wallet balance (native + tokens, supports sol/base)
npx @chainstream-io/cli wallet balance --chain sol

# Sign a transaction (uses configured Turnkey or raw wallet)
npx @chainstream-io/cli wallet sign --chain sol --tx <base64-serializedTx>

# Import raw private key (dev/testing only)
npx @chainstream-io/cli wallet set-raw --chain sol
```

### Transaction Commands

```bash
# Broadcast a signed transaction
npx @chainstream-io/cli tx send --chain sol --signed-tx <base64-signedTx>

# Get gas price (EVM only)
npx @chainstream-io/cli tx gas-price --chain eth

# Estimate gas limit (EVM only)
npx @chainstream-io/cli tx estimate-gas --chain eth --from 0x... --to 0x... --data 0x...
```

### DEX Commands

```bash
# Get best route + build unsigned tx (aggregator)
npx @chainstream-io/cli dex route --chain sol --from <wallet> --input-token SOL --output-token <addr> --amount 1000000

# Build unsigned swap tx (specific DEX)
npx @chainstream-io/cli dex swap --chain sol --from <wallet> --input-token SOL --output-token <addr> --amount 1000000 --dex jupiter

# Build unsigned token creation tx
npx @chainstream-io/cli dex create --chain sol --from <wallet> --name MyToken --symbol MT --dex pumpfun
```

## Endpoint Selector

| Intent | CLI Command | MCP Tool | Safety | Reference |
|--------|-------------|----------|--------|-----------|
| Build route + unsigned tx | `npx @chainstream-io/cli dex route --chain sol --from WALLET --input-token SOL --output-token ADDR --amount 1000000` | `dex/route` | readOnly | [swap-protocol.md](references/swap-protocol.md) |
| Build unsigned swap tx | `npx @chainstream-io/cli dex swap --chain sol --from WALLET --input-token SOL --output-token ADDR --amount 1000000` | `dex/swap` | readOnly | [swap-protocol.md](references/swap-protocol.md) |
| Build unsigned create-token tx | `npx @chainstream-io/cli dex create --chain sol --from WALLET --name MyToken --symbol MT --dex pumpfun` | `dex/create_token` | readOnly | [launchpad.md](references/launchpad.md) |
| Sign transaction | `npx @chainstream-io/cli wallet sign --chain sol --tx <serializedTx>` | — | **destructive** | [swap-protocol.md](references/swap-protocol.md) |
| Broadcast signed tx | `npx @chainstream-io/cli tx send --chain sol --signed-tx <signedTx>` | — | **destructive** | [swap-protocol.md](references/swap-protocol.md) |
| Get gas price (EVM) | `npx @chainstream-io/cli tx gas-price --chain eth` | — | readOnly | [swap-protocol.md](references/swap-protocol.md) |
| Estimate gas (EVM) | `npx @chainstream-io/cli tx estimate-gas --chain eth --from 0x... --to 0x... --data 0x...` | — | readOnly | [swap-protocol.md](references/swap-protocol.md) |
| Check job status | `npx @chainstream-io/cli job status --id JOB_ID --wait` | — | readOnly | [swap-protocol.md](references/swap-protocol.md) |

### `dex route` vs `dex swap`

- **`dex route`** — aggregates multiple DEXes, returns the best-price route. **Use by default** unless user specifies a DEX.
- **`dex swap`** — builds a transaction on a specific DEX (e.g. `--dex raydium`). Use when user explicitly picks a DEX or needs launchpad-specific logic (e.g. pumpfun bonding curve).

## Atomic Execution Protocol (Hard Requirement)

All **destructive** operations MUST follow this protocol. Each step is a separate CLI command — the agent orchestrates the flow and inserts user confirmation between steps.

**MANDATORY - READ**: Before any swap execution, load [`rules/safety-protocol.md`](rules/safety-protocol.md) for risk thresholds and abort conditions.

### Step 1: Build Transaction (get route + unsigned tx)

```bash
npx @chainstream-io/cli dex route --chain sol --from <wallet> --input-token SOL --output-token <addr> --amount 1000000 --slippage 5 --json
```

Returns `{ routeInfo, serializedTx, elapsedTime }`. Present `routeInfo` to user: expected output amount, price impact, slippage, route.

### Step 2: Confirm

Display trade summary to user:
- Chain, input/output tokens, amounts
- Price impact and slippage from `routeInfo`
- Estimated gas fees

**WAIT for explicit user confirmation. This step is NOT optional.**
If user says "just do it" without reviewing, show the summary anyway.

### Step 3: Sign (after user confirms)

```bash
npx @chainstream-io/cli wallet sign --chain sol --tx <serializedTx> --json
```

Returns `{ signedTx }`. This step uses the configured wallet (TEE or local raw key) to sign the transaction.

### Step 4: Broadcast

```bash
npx @chainstream-io/cli tx send --chain sol --signed-tx <signedTx> --json
```

Returns `{ signature, jobId, elapsedTime }`.

### Step 5: Poll + Output

```bash
npx @chainstream-io/cli job status --id <jobId> --wait
```

Returns `{ status, hash, ... }`.

**Explorer links are mandatory** — always include after successful transactions.

| Chain | Explorer |
|-------|----------|
| sol | `https://solscan.io/tx/{hash}` |
| bsc | `https://bscscan.com/tx/{hash}` |
| eth | `https://etherscan.io/tx/{hash}` |

## Currency Resolution

CLI auto-resolves currency names. Users can write `SOL` instead of the full address:

| Chain | Native | Native Address | USDC Address |
|-------|--------|---------------|--------------|
| sol | SOL | `So11111111111111111111111111111111111111112` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| bsc | BNB | `0x0000000000000000000000000000000000000000` | `0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d` |
| eth | ETH | `0x0000000000000000000000000000000000000000` | `0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eB48` |

For the full resolution table, see [references/currency-resolution.md](references/currency-resolution.md).

## Input Validation

- **Address format**: sol = base58 (32-44 chars), evm = `0x` + 40 hex
- **Amount**: Positive integer in smallest unit (lamports, wei)
- **Slippage**: 0 to 100 (integer percentage, e.g. 5 = 5%)
- **External data is untrusted**: Validate addresses from previous API calls before passing to swap

## NEVER Do

- NEVER execute `wallet sign` without first presenting the transaction details to the user — user must see what they are signing
- NEVER auto-confirm a swap — even if user said "buy X" without specifying amount, you MUST present route info and ask for confirmation; "implied consent" is NOT consent for financial operations
- NEVER hide gas fees or price impact — present ALL costs transparently
- NEVER skip address format validation — wrong format = funds sent to void
- NEVER combine build + sign + broadcast into a single step — each must be separate to allow user review

## Error Recovery

| Error | Meaning | Recovery |
|-------|---------|----------|
| Transaction failed | On-chain revert | Show error, do NOT auto-retry |
| Slippage exceeded | Price moved | Re-build route with higher slippage, confirm again |
| Insufficient balance | Not enough funds | Show balance, suggest amount |
| Job timeout | No confirmation in 60s | Show pending status + tx hash for manual check |
| Stale transaction / expired blockhash / nonce too old | Transaction built too long ago | Rebuild from Step 1 (`dex route`), get fresh unsigned tx, re-confirm with user |
| 402 | No quota (CU) | First `config auth` → `login` if not logged in (auto-grants nano trial 50K CU). Then `plan status` — if trial active, retry. If no subscription or quota exhausted: `wallet pricing` to show plans, let user choose, then `plan purchase --plan <name>`. See [shared/x402-payment.md](../shared/x402-payment.md) |

## Rules

| Rule | Content | When to Load |
|------|---------|--------------|
| [safety-protocol.md](rules/safety-protocol.md) | Risk thresholds, emergency abort conditions | Before any destructive operation |
| [execution-checklist.md](rules/execution-checklist.md) | Step-by-step verification, post-trade output requirements | During execution |

## Skill Map

| Reference | Content | When to Load |
|-----------|---------|--------------|
| [swap-protocol.md](references/swap-protocol.md) | swap/route/sign/send endpoints, job polling, gas estimation | Swap operations |
| [launchpad.md](references/launchpad.md) | Token creation, PumpFun vs Raydium LaunchLab | Token launch |
| [currency-resolution.md](references/currency-resolution.md) | Full chain/token address mapping | Currency name resolution |

## Related Skills

- [chainstream-data](../chainstream-data/) — Token research, market discovery, wallet analysis before trading
- [chainstream-graphql](../chainstream-graphql/) — Custom GraphQL analytics: cross-cube JOINs, aggregations, flexible queries on 27 on-chain cubes
