# crypto-treasury-ops

`crypto-treasury-ops` is a production-oriented OpenClaw / ClawHub skill package for guarded crypto treasury operations on EVM chains, Solana balance support, Solana-to-EVM bridging, and native Hyperliquid perpetual trading. It exposes a CLI entrypoint with structured JSON responses so an agent can quote, validate, and execute treasury actions with explicit safety checks.

## Features

- `get_balances` for Ethereum, Polygon, Arbitrum, Base, and Solana
- `transfer_token` for native assets and ERC-20 tokens
- `swap_token` for guarded ERC-20 swaps on one chain
- `bridge_token` through a pluggable bridge provider layer, including Solana -> EVM routing
- `deposit_to_hyperliquid` with guarded Arbitrum direct deposits and Polygon/Base USDC routing into Hyperliquid
- `get_hyperliquid_market_state` and `get_hyperliquid_account_state` for native Hyperliquid read paths
- `place_hyperliquid_order`, `protect_hyperliquid_position`, and `cancel_hyperliquid_order` for guarded Hyperliquid perpetual order flow
- `safety_check` with allowlists, thresholds, gas reserve checks, and daily limits
- `quote_operation` to preview fees, gas, and expected received amounts
- JSONL audit logging for every action in `.runtime/treasury-ops.log`

## Chain and asset coverage

Initial chain support:

- Ethereum
- Polygon
- Arbitrum
- Base
- Solana for balance checks and source-side bridging

Initial treasury token support:

- Native gas tokens
- USDC
- USDT
- DAI
- WETH
- WBTC
- ARB on Arbitrum
- cbBTC on Base
- Polygon USDC.e and Arbitrum USDC.e for balance visibility only

## Swap support

The first swap implementation uses the 0x Swap API through a provider abstraction.

- Supported chains: Ethereum, Polygon, Arbitrum, Base
- Supported assets by symbol out of the box: stablecoins plus WETH/WBTC/cbBTC/ARB where configured
- Custom ERC-20 token addresses are also supported
- Execution requires `ZEROX_API_KEY`
- This first version is intentionally limited to ERC-20 swaps
- Native gas token swaps are not executed directly; use wrapped tokens such as `WETH`

## Hyperliquid note

The Hyperliquid deposit flow is intentionally conservative:

- It only supports `USDC`.
- It only supports wallet-based deposits where the treasury wallet is the same wallet credited on Hyperliquid.
- It uses Hyperliquid's Arbitrum USDC bridge address.
- Arbitrum deposits are direct `Arbitrum USDC -> Hyperliquid`.
- Polygon and Base deposits are executed as `Source USDC -> Arbitrum USDC -> Hyperliquid`.
- If Arbitrum gas is too low for the final deposit leg, the tool can automatically reserve a small amount of source USDC to bridge enough Arbitrum ETH first.
- The execution path is multi-stage and may involve more than one onchain transaction before the final Hyperliquid deposit completes.
- If a bridge provider status API is unreliable, the skill now falls back to onchain balance confirmation so the flow can continue safely.
- If the destination Hyperliquid account differs from the treasury EOA, the tool rejects the request.

This matches Hyperliquid's current bridge model, where Arbitrum USDC deposits are credited to the sending wallet.

## Hyperliquid trading note

The first native Hyperliquid trading implementation is intentionally conservative:

- It supports perpetual markets only
- It supports both main-dex perps such as `BTC` and HIP-3 / builder-dex perps in `dex:COIN` format such as `xyz:GOLD`
- It exposes read-only market and account state queries
- `place_hyperliquid_order` currently supports `market` and `limit` orders only
- `protect_hyperliquid_position` derives native Hyperliquid reduce-only trigger orders for take-profit and stop-loss management on an existing position
- Market orders are sent as protected IOC orders with a configurable slippage cap
- Optional leverage updates are supported before order placement
- `cancel_hyperliquid_order` cancels a specific open order by `market + orderId`
- `protect_hyperliquid_position` accepts ROE-style thresholds such as "take profit when equity doubles, stop when margin halves"
- If the requested stop-loss would be beyond liquidation, the protection tool tightens it in front of liquidation and returns a warning
- `get_hyperliquid_account_state` accepts an optional `dex` field to inspect a builder dex account state
- HIP-3 orders require Hyperliquid `dexAbstraction`
- The skill will not silently switch abstraction mode; builder-dex execution requires `enableDexAbstraction: true`
- Trading safety is separate from treasury transfer safety:
  - market allowlist
  - max single order notional
  - max daily order notional
  - max leverage
  - confirmation threshold above which `approval=true` is required
- `quote_operation` supports `place_hyperliquid_order`
- `quote_operation` supports both `place_hyperliquid_order` and `protect_hyperliquid_position`
- Dry runs can use `accountAddress` / `walletAddress` for read-only account context
- Real order execution still requires `TREASURY_PRIVATE_KEY`, and execution only proceeds when the signer matches the target Hyperliquid account

## Solana note

This skill now supports Solana balance checks and Solana -> EVM bridging, but general Solana execution is still intentionally narrow.

- `get_balances` supports native `SOL` plus configured SPL stablecoin mints
- `bridge_token` supports `solana -> ethereum/arbitrum/base/polygon`
- The first Solana bridge implementation uses Mayan
- Solana execution requires `SOLANA_TREASURY_PRIVATE_KEY` or `SOLANA_TREASURY_ADDRESS` for read-only quote context
- `MAYAN_API_KEY` is optional but recommended for higher quote rate limits
- Solana bridge routing currently supports `SOL -> native gas token` and same-symbol stablecoin routes such as `USDC -> USDC`
- It cannot move `SOL` from Solana to Hyperliquid.
- `deposit_to_hyperliquid` only supports EVM USDC flows from Base, Polygon, or Arbitrum.
- Hyperliquid itself supports some Solana deposits through Unit-managed flows, but that path is not implemented in this skill.

If you need `SOL -> Hyperliquid`, that requires a separate Solana signer and a Solana-side deposit or swap/bridge flow that is not implemented in this package.

## Setup

1. Copy `.env.example` to `.env`.
2. Fill in the private key and treasury safety policy values.
3. Add `ZEROX_API_KEY` if you want to use `swap_token` or swap quotes.
4. Add `SOLANA_TREASURY_PRIVATE_KEY` if you want to execute Solana bridge transactions.
5. Optionally add `MAYAN_API_KEY` if you want higher Solana bridge quote limits.
6. Optionally tune `HYPERLIQUID_TRADING_*` safety variables if you want to trade on Hyperliquid.
7. Install dependencies:

```bash
npm install
```

6. Build:

```bash
npm run build
```

Built-in RPC defaults:

- The skill ships with fallback public RPC lists for Ethereum, Polygon, Arbitrum, Base, and Solana.
- Environment variables such as `ETHEREUM_RPC_URL` and `SOLANA_RPC_URL` are now optional overrides.
- Comma-separated override lists are supported, and custom URLs are tried before built-in defaults.

## CLI usage

Each tool returns structured JSON to stdout.

### get_balances

```bash
node dist/index.js --action get_balances --input '{
  "walletAddress": "0x1111111111111111111111111111111111111111",
  "chain": "polygon"
}'
```

```bash
node dist/index.js --action get_balances --input '{
  "chain": "solana",
  "solanaAddress": "HK6y2RbhgDJLQ1gAmJatjEyZTjfK6MSHBtpoSN1Vx85A"
}'
```

### transfer_token

```bash
node dist/index.js --action transfer_token --input '{
  "chain": "base",
  "token": "USDC",
  "recipient": "0x2222222222222222222222222222222222222222",
  "amount": "250",
  "approval": true,
  "dryRun": true
}'
```

### swap_token

```bash
node dist/index.js --action swap_token --input '{
  "chain": "arbitrum",
  "sellToken": "USDC",
  "buyToken": "WETH",
  "amount": "500",
  "approval": true,
  "dryRun": true,
  "slippageBps": 50
}'
```

### bridge_token

```bash
node dist/index.js --action bridge_token --input '{
  "sourceChain": "polygon",
  "destinationChain": "arbitrum",
  "token": "USDC",
  "amount": "1000",
  "approval": true,
  "dryRun": true
}'
```

Solana example:

```bash
node dist/index.js --action bridge_token --input '{
  "sourceChain": "solana",
  "destinationChain": "ethereum",
  "token": "SOL",
  "amount": "0.02",
  "approval": true,
  "dryRun": true
}'
```

### deposit_to_hyperliquid

```bash
node dist/index.js --action deposit_to_hyperliquid --input '{
  "sourceChain": "base",
  "token": "USDC",
  "amount": "500",
  "destination": "0xYourTreasuryWallet",
  "approval": true,
  "dryRun": true
}'
```

Recommended execution pattern:

1. Run `quote_operation` for the intended source balance.
2. Run `deposit_to_hyperliquid` with `dryRun: true`.
3. Run `deposit_to_hyperliquid` with `dryRun: false`.
4. If a multi-stage execution errors, re-check `base/polygon` and `arbitrum` balances before retrying.
5. Re-quote with the remaining source balance instead of blindly replaying the previous amount.

### get_hyperliquid_market_state

```bash
node dist/index.js --action get_hyperliquid_market_state --input '{
  "market": "ETH"
}'
```

If `market` is omitted, the tool returns the full perpetual market list with metadata and live context.

HIP-3 example:

```bash
node dist/index.js --action get_hyperliquid_market_state --input '{
  "market": "xyz:GOLD"
}'
```

### get_hyperliquid_account_state

```bash
node dist/index.js --action get_hyperliquid_account_state --input '{
  "user": "0xYourHyperliquidWallet"
}'
```

HIP-3 dex example:

```bash
node dist/index.js --action get_hyperliquid_account_state --input '{
  "user": "0xYourHyperliquidWallet",
  "dex": "xyz"
}'
```

### place_hyperliquid_order

Read-only quote path:

```bash
node dist/index.js --action quote_operation --input '{
  "operationType": "place_hyperliquid_order",
  "walletAddress": "0xYourHyperliquidWallet",
  "market": "ETH",
  "side": "buy",
  "size": "0.01",
  "orderType": "market",
  "approval": true
}'
```

HIP-3 quote example:

```bash
node dist/index.js --action quote_operation --input '{
  "operationType": "place_hyperliquid_order",
  "walletAddress": "0xYourHyperliquidWallet",
  "market": "xyz:GOLD",
  "side": "sell",
  "size": "0.01",
  "orderType": "market",
  "approval": true,
  "enableDexAbstraction": true
}'
```

Dry-run order path:

```bash
node dist/index.js --action place_hyperliquid_order --input '{
  "accountAddress": "0xYourHyperliquidWallet",
  "market": "ETH",
  "side": "buy",
  "size": "0.01",
  "orderType": "limit",
  "price": "2000",
  "leverage": 2,
  "approval": true,
  "dryRun": true
}'
```

HIP-3 execution notes:

- Use `market: "dex:COIN"` for builder dex assets
- Pass `enableDexAbstraction: true` the first time you execute on a builder dex
- The skill will quote and warn about the abstraction switch before execution

### protect_hyperliquid_position

Read-only quote path:

```bash
node dist/index.js --action quote_operation --input '{
  "operationType": "protect_hyperliquid_position",
  "walletAddress": "0xYourHyperliquidWallet",
  "market": "BTC",
  "takeProfitRoePercent": 100,
  "stopLossRoePercent": 50,
  "approval": true
}'
```

Dry-run execution path:

```bash
node dist/index.js --action protect_hyperliquid_position --input '{
  "accountAddress": "0xYourHyperliquidWallet",
  "market": "BTC",
  "takeProfitRoePercent": 100,
  "stopLossRoePercent": 50,
  "approval": true,
  "dryRun": true
}'
```

Notes:

- The tool reads the live Hyperliquid position and derives full-size reduce-only trigger orders
- `takeProfitRoePercent: 100` means position equity doubling from entry
- `stopLossRoePercent: 50` means position equity halving from entry
- If the requested stop-loss would sit beyond liquidation, the tool tightens it in front of liquidation and returns a warning
- This tool is intended for protecting an existing position, not opening a new one

### cancel_hyperliquid_order

```bash
node dist/index.js --action cancel_hyperliquid_order --input '{
  "market": "ETH",
  "orderId": 123456,
  "dryRun": true
}'
```

### safety_check

```bash
node dist/index.js --action safety_check --input '{
  "operationType": "bridge_token",
  "chain": "polygon",
  "token": "USDC",
  "amount": "12000",
  "destination": "0x2222222222222222222222222222222222222222",
  "approval": false,
  "feeBps": 35,
  "slippageBps": 20
}'
```

### quote_operation

```bash
node dist/index.js --action quote_operation --input '{
  "operationType": "deposit_to_hyperliquid",
  "sourceChain": "base",
  "token": "USDC",
  "amount": "2500",
  "destination": "0xYourTreasuryWallet"
}'
```

## Output contract

Successful calls return:

```json
{
  "ok": true,
  "tool": "transfer_token",
  "status": "success",
  "requestId": "uuid",
  "timestamp": "2026-03-13T00:00:00.000Z",
  "data": {}
}
```

Rejected or failed calls return:

```json
{
  "ok": false,
  "tool": "transfer_token",
  "status": "rejected",
  "requestId": "uuid",
  "timestamp": "2026-03-13T00:00:00.000Z",
  "errors": [
    "Destination is not allowlisted."
  ],
  "data": {
    "safety": {}
  }
}
```

## Implementation notes

- Environment variables are the only secret input path.
- Bridge execution is abstracted behind provider classes. `LI.FI` is implemented first because its quote and status APIs are mature and public.
- Hyperliquid deposits from Base and Polygon are automatically decomposed into bridge and deposit legs, with optional Arbitrum gas top-up planning when the destination wallet is short on gas.
- Hyperliquid trading uses native Hyperliquid `info` and `exchange` API flows through a dedicated service, with perps-only scope in this first release.
- HIP-3 support is implemented for builder-dex perpetuals via `dex:COIN` routing and explicit dex-abstraction handling.
- Swap execution is abstracted behind provider classes. `0x` is implemented first because it covers the initial target chains with a simple quote and execution API.
- `Relay` and `Across` provider classes are present as extension points and intentionally throw until implemented.
- Runtime logs are written as JSON lines to `.runtime/treasury-ops.log`.
- Daily limit enforcement is calculated from the runtime log.

## TODOs for production rollout

- Add secrets management backed by a real vault or HSM signer instead of a raw environment private key.
- Add destination address books per chain and per operation class.
- Implement dedicated `Relay` and `Across` providers.
- Add persistent state storage for transfer counters instead of deriving from the local log file.
- Add alert hooks for rejected or high-value operations.
- Add multi-signature confirmation workflows above the confirmation threshold.
- Add native Hyperliquid spot trading and fuller TP/SL grouping semantics once the safety model is expanded.
