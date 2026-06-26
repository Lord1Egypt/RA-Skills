---
name: crypto-treasury-ops
description: Safely manage EVM treasury operations and native Hyperliquid trading for OpenClaw agents, including wallet balance checks, guarded token transfers, cross-chain USDC bridging, Hyperliquid deposits, destination gas top-ups, trading safety, and structured quoting.
---

# crypto-treasury-ops

Use this skill when an OpenClaw agent needs to inspect or operate a treasury wallet on Ethereum, Polygon, Arbitrum, or Base with explicit safety controls, or use Solana as a read path and bridge source chain.

## What this skill does

- Checks native and configured stablecoin balances
- Checks Solana native SOL and configured SPL token balances
- Transfers native assets or ERC-20 tokens on one chain
- Bridges tokens across chains through a pluggable provider layer, including Solana -> EVM routes
- Deposits USDC to Hyperliquid with guarded Arbitrum direct flow plus Polygon/Base routing
- Reads Hyperliquid perpetual market state and account state
- Places, protects, and cancels guarded Hyperliquid perpetual orders
- Evaluates treasury safety policy before execution
- Returns structured JSON for reliable downstream agent use

## Runtime contract

Execution tools require environment configuration before build or runtime.

Required variables:

```bash
TREASURY_PRIVATE_KEY=0x...
SOLANA_TREASURY_PRIVATE_KEY=
ZEROX_API_KEY=...
```

Recommended workflow:

```bash
cp .env.example .env
# fill in the treasury private key and optional RPC overrides
npm install
npm run build
```

Important:

- `TREASURY_PRIVATE_KEY` is required for EVM execution tools and as the default destination wallet for Solana -> EVM bridges
- `SOLANA_TREASURY_PRIVATE_KEY` is required for executing Solana bridge transactions
- `SOLANA_TREASURY_ADDRESS` can be used for read-only Solana quote context when no Solana signer is present
- `ZEROX_API_KEY` is required for `swap_token` and swap quotes
- `MAYAN_API_KEY` is optional but recommended for Solana bridge quote / execution rate limits
- `HYPERLIQUID_TRADING_*` variables can further constrain market allowlists, order notional, leverage, and confirmation thresholds
- The skill ships with built-in fallback RPC URL lists for Ethereum, Polygon, Arbitrum, Base, and Solana
- RPC env vars such as `ETHEREUM_RPC_URL` and `SOLANA_RPC_URL` are optional overrides; comma-separated lists are supported
- `get_balances`, `get_hyperliquid_market_state`, `get_hyperliquid_account_state`, `safety_check`, and some quote flows can run without a signer
- Do not pass private keys in tool input JSON; this skill reads them from the environment only
- Prefer a vault, KMS, HSM, or delegated signer in production instead of a raw hot-wallet private key in `.env`
- For state-changing treasury operations, run `quote_operation` or `dryRun=true` immediately before execution so the route and balances are fresh

Invoke tools through the CLI:

```bash
node dist/index.js --action <tool_name> --input '<json>'
```

## Tools

### `get_balances`

Inputs:

- `walletAddress`
- `chain`
- `solanaAddress` optional when `chain=solana`

Returns:

- Native balance
- Configured stablecoin balances for that chain
- Symbols, decimals, raw amounts, and human-readable amounts

Notes:

- `chain=solana` is supported for read-only balance queries
- Solana execution is limited to bridge source flows only

### `transfer_token`

Inputs:

- `chain`
- `token`
- `recipient`
- `amount`
- `approval` optional
- `dryRun` optional

Behavior:

- Validates recipient format
- Resolves token by symbol or address
- Checks wallet balance before sending
- Estimates gas
- Runs safety policy
- Rejects unsafe or underfunded transfers
- Returns transfer summary and transaction hash

### `swap_token`

Inputs:

- `chain`
- `sellToken`
- `buyToken`
- `amount`
- `recipient` optional
- `slippageBps` optional
- `approval` optional
- `dryRun` optional

Behavior:

- Uses the configured swap provider abstraction
- First implementation uses the 0x Swap API
- Supports EVM ERC-20 swaps only
- Rejects native gas token swaps such as raw `ETH` or `POL`; use wrapped tokens such as `WETH`
- Quotes route, minimum received, gas, allowance target, and tx data
- Checks treasury policy and gas reserve before execution
- Executes only when approval and policy conditions pass

### `bridge_token`

Inputs:

- `sourceChain`
- `destinationChain`
- `token`
- `amount`
- `approval` optional
- `dryRun` optional

Behavior:

- Uses the configured bridge provider abstraction
- Supports `solana -> ethereum/arbitrum/base/polygon` through Mayan
- Quotes route, fees, minimum received, and tx data
- Checks treasury policy, fee threshold, and gas reserve
- Executes only when approval and policy conditions pass
- Returns route summary, tx status, and explorer links when available
- The first Solana bridge implementation supports `SOL -> native destination gas token` and same-symbol stablecoin routes such as `USDC -> USDC`
- Solana bridge execution currently returns a submitted / pending status after the signed Solana transaction is broadcast; completion should be re-checked from the destination balance or explorer link

### `deposit_to_hyperliquid`

Inputs:

- `sourceChain`
- `token`
- `amount`
- `destination`
- `approval` optional
- `dryRun` optional

Behavior:

- Supports `USDC` only
- Supports `arbitrum` direct deposits and `polygon/base -> arbitrum -> hyperliquid`
- If Arbitrum gas is insufficient for the final deposit, can reserve source USDC and bridge enough Arbitrum ETH first
- This is a multi-stage flow: optional gas top-up, bridge to Arbitrum, then Arbitrum USDC deposit into Hyperliquid
- The tool now attempts balance-based recovery if a bridge status API is unreliable but funds have already arrived onchain
- Rejects deposits to a different Hyperliquid wallet than the treasury signer
- Does not support Solana-origin deposits or `SOL`
- Hyperliquid may support separate Solana deposits through Unit-managed flows, but those are outside this skill
- Rejects if minimum deposit or gas reserve requirements are not met
- Returns the bridge leg, deposit leg, and final execution summary

Recommended agent workflow:

- Call `quote_operation` first
- If the quote is acceptable, call `deposit_to_hyperliquid` with `dryRun=true`
- Only then call `deposit_to_hyperliquid` with `dryRun=false`
- If execution returns an error after a partial bridge or top-up, do not blindly retry the original amount
- Re-check `base/polygon` and `arbitrum` balances, then re-run `quote_operation` with the remaining source balance if a retry is needed

### `get_hyperliquid_market_state`

Inputs:

- `market` optional

Behavior:

- Returns live Hyperliquid perpetual metadata and context
- If `market` is omitted, returns the full supported perpetual market list
- If `market` is provided, also returns best bid / ask from the live L2 snapshot
- Supports HIP-3 / builder dex markets in `dex:COIN` format such as `xyz:GOLD`

### `get_hyperliquid_account_state`

Inputs:

- `user` optional
- `dex` optional

Behavior:

- Returns Hyperliquid perpetual account summary
- Returns positions and open orders
- If `user` is omitted, the skill uses the treasury signer address
- If `dex` is provided, the tool queries that specific HIP-3 builder dex
- Also returns `abstractionState` and `dexAbstractionEnabled`

### `place_hyperliquid_order`

Inputs:

- `accountAddress` optional for read-only dry-run / quote context
- `market`
- `side`
- `size`
- `orderType`
- `price` required for limit orders
- `slippageBps` optional for market orders
- `reduceOnly` optional
- `leverage` optional
- `marginMode` optional
- `timeInForce` optional for limit orders
- `enableDexAbstraction` optional
- `approval` optional
- `dryRun` optional

Behavior:

- Supports Hyperliquid perpetuals only
- Supports builder dex perps in `dex:COIN` format such as `xyz:GOLD`
- Supports `market` and `limit` orders in the first version
- Market orders are translated into protected IOC orders with a configurable price cap
- Optionally updates leverage before placing the order
- Enforces market allowlist, max single order notional, max daily order notional, max leverage, and confirmation threshold
- `quote_operation` supports this tool
- If `accountAddress` is provided, dry-run and quote can use it for read-only account context
- Real execution only proceeds when the signer matches the target Hyperliquid account
- HIP-3 builder-dex execution requires Hyperliquid `dexAbstraction`
- The skill does not silently switch abstraction mode
- For HIP-3 orders, pass `enableDexAbstraction=true` if you want execution to switch the account into `dexAbstraction` first

Recommended agent workflow:

- Call `quote_operation` first with `operationType=place_hyperliquid_order`
- Review the returned `safety` block and `notionalUsd`
- Call `place_hyperliquid_order` with `dryRun=true`
- Only then call `place_hyperliquid_order` with `dryRun=false`

### `protect_hyperliquid_position`

Inputs:

- `accountAddress` optional for read-only dry-run / quote context
- `market`
- `takeProfitRoePercent` optional, default `100`
- `stopLossRoePercent` optional, default `50`
- `replaceExisting` optional
- `liquidationBufferBps` optional, default `25`
- `enableDexAbstraction` optional
- `approval` optional
- `dryRun` optional

Behavior:

- Reads the live Hyperliquid position for the requested market
- Derives a full-size reduce-only take-profit trigger and a full-size reduce-only stop-loss trigger
- Uses ROE-style rules relative to entry and leverage:
  - `takeProfitRoePercent=100` means position equity doubling
  - `stopLossRoePercent=50` means position equity halving
- If the requested stop-loss would be beyond liquidation, the tool tightens it in front of liquidation using `liquidationBufferBps` and returns a warning
- Uses native Hyperliquid trigger orders with reduce-only semantics
- `quote_operation` supports this tool
- Real execution only proceeds when the signer matches the target Hyperliquid account
- For HIP-3 builder-dex positions, pass `enableDexAbstraction=true` if the account must first switch into `dexAbstraction`

Recommended agent workflow:

- Call `quote_operation` first with `operationType=protect_hyperliquid_position`
- Review any liquidation-adjustment warning before execution
- Call `protect_hyperliquid_position` with `dryRun=true`
- Only then call `protect_hyperliquid_position` with `dryRun=false`

### `cancel_hyperliquid_order`

Inputs:

- `market`
- `orderId`
- `dryRun` optional

Behavior:

- Looks up the matching open order first
- Rejects if the order is not currently open
- Supports dry-run preview before cancellation

### `safety_check`

Inputs:

- `operationType`
- `chain`
- `token`
- `amount`
- `destination` optional
- `approval` optional
- `feeBps` optional
- `slippageBps` optional

Behavior:

- Enforces allowlists
- Enforces max single transfer size
- Enforces max daily transfer amount
- Requires approval above the configured threshold
- Rejects bridge and deposit flows with insufficient gas reserve
- Rejects excessive estimated fees or slippage

### `quote_operation`

Inputs:

- `operationType`
- operation-specific fields

Behavior:

- Estimates balance impact, gas, route fees, and minimum received
- Estimates Hyperliquid order notional, submission price, simulated fill price, and safety outcome for `place_hyperliquid_order`
- Estimates derived TP/SL trigger prices and safety outcome for `protect_hyperliquid_position`
- Returns a structured quote without execution

## Examples

```bash
node dist/index.js --action get_balances --input '{"walletAddress":"0x1111111111111111111111111111111111111111","chain":"arbitrum"}'
```

```bash
node dist/index.js --action get_balances --input '{"chain":"solana","solanaAddress":"HK6y2RbhgDJLQ1gAmJatjEyZTjfK6MSHBtpoSN1Vx85A"}'
```

```bash
node dist/index.js --action transfer_token --input '{"chain":"base","token":"USDC","recipient":"0x2222222222222222222222222222222222222222","amount":"100","approval":true,"dryRun":true}'
```

```bash
node dist/index.js --action swap_token --input '{"chain":"arbitrum","sellToken":"USDC","buyToken":"WETH","amount":"250","approval":true,"dryRun":true,"slippageBps":50}'
```

```bash
node dist/index.js --action bridge_token --input '{"sourceChain":"polygon","destinationChain":"arbitrum","token":"USDC","amount":"2500","approval":true,"dryRun":true}'
```

```bash
node dist/index.js --action bridge_token --input '{"sourceChain":"solana","destinationChain":"ethereum","token":"SOL","amount":"0.02","approval":true,"dryRun":true}'
```

```bash
node dist/index.js --action deposit_to_hyperliquid --input '{"sourceChain":"base","token":"USDC","amount":"500","destination":"0xYourTreasuryWallet","approval":true,"dryRun":true}'
```

```bash
node dist/index.js --action get_hyperliquid_market_state --input '{"market":"ETH"}'
```

```bash
node dist/index.js --action get_hyperliquid_market_state --input '{"market":"xyz:GOLD"}'
```

```bash
node dist/index.js --action get_hyperliquid_account_state --input '{"user":"0xYourHyperliquidWallet"}'
```

```bash
node dist/index.js --action get_hyperliquid_account_state --input '{"user":"0xYourHyperliquidWallet","dex":"xyz"}'
```

```bash
node dist/index.js --action quote_operation --input '{"operationType":"place_hyperliquid_order","walletAddress":"0xYourHyperliquidWallet","market":"ETH","side":"buy","size":"0.01","orderType":"market","approval":true}'
```

```bash
node dist/index.js --action quote_operation --input '{"operationType":"place_hyperliquid_order","walletAddress":"0xYourHyperliquidWallet","market":"xyz:GOLD","side":"sell","size":"0.01","orderType":"market","approval":true,"enableDexAbstraction":true}'
```

```bash
node dist/index.js --action place_hyperliquid_order --input '{"accountAddress":"0xYourHyperliquidWallet","market":"ETH","side":"buy","size":"0.01","orderType":"limit","price":"2000","leverage":2,"approval":true,"dryRun":true}'
```

```bash
node dist/index.js --action place_hyperliquid_order --input '{"accountAddress":"0xYourHyperliquidWallet","market":"xyz:GOLD","side":"sell","size":"0.01","orderType":"market","approval":true,"enableDexAbstraction":true,"dryRun":true}'
```

```bash
node dist/index.js --action quote_operation --input '{"operationType":"protect_hyperliquid_position","walletAddress":"0xYourHyperliquidWallet","market":"BTC","takeProfitRoePercent":100,"stopLossRoePercent":50,"approval":true}'
```

```bash
node dist/index.js --action protect_hyperliquid_position --input '{"accountAddress":"0xYourHyperliquidWallet","market":"BTC","takeProfitRoePercent":100,"stopLossRoePercent":50,"approval":true,"dryRun":true}'
```

```bash
node dist/index.js --action cancel_hyperliquid_order --input '{"market":"ETH","orderId":123456,"dryRun":true}'
```

## Safety defaults

- Do not bypass `safety_check` reasoning. Execution tools perform the check again internally.
- Treat rejected outputs as hard stops.
- Prefer `dryRun=true` first for all new destinations or larger transfers.
- Prefer `quote_operation` plus `dryRun=true` before any new Hyperliquid order.
- Prefer `protect_hyperliquid_position` over ad hoc manual TP/SL math when protecting an existing Hyperliquid position.
- Require explicit `approval=true` for amounts above the configured threshold.
- Never assume a non-allowlisted destination is safe.
- For multi-stage flows such as Hyperliquid deposits, never reuse a stale quoted amount after a partial execution. Re-quote from current balances first.
