---
name: fx-sdk-agent
version: 1.0.1
description: Use FX Protocol TypeScript SDK (fx-sdk) to query positions (getPositions returns PositionInfo[] with rawColls, rawDebts, rawCollsToken, rawDebtsToken, decimals), build leverage operation transaction plans, bridge tokens between Base and Ethereum (LayerZero), and fxSAVE (config/totals, balance, redeem status, claimable preview, deposit, withdraw, claim). Generate runnable scripts for increasePosition, reducePosition, adjustPositionLeverage, depositAndMint, repayAndWithdraw, getBridgeQuote, buildBridgeTx, getFxSaveConfig, getFxSaveBalance, getFxSaveRedeemStatus, getFxSaveClaimable, getRedeemTx, depositFxSave, withdrawFxSave. Use when users ask to integrate this SDK into an agent/tool, produce transaction execution code, troubleshoot SDK parameters, or validate FX trading workflows on Ethereum mainnet or Base.
---

# FX SDK Agent Skill

Use this skill to produce reliable `fx-sdk` integrations for agent workflows.

## Follow This Workflow

1. Confirm user intent: read-only query (`getPositions`, `getFxSaveConfig`, `getFxSaveBalance`, `getFxSaveRedeemStatus`, `getFxSaveClaimable`), transaction-producing action (`increase/reduce/adjust/deposit/repay`, fxSAVE `depositFxSave`/`withdrawFxSave`/`getRedeemTx`), or Base–Ethereum bridge (`getBridgeQuote` / `buildBridgeTx`).
2. Collect required inputs before coding:
- `market`: `ETH` or `BTC`
- position type when needed: `long` or `short`
- `positionId`
- token address from `tokens`
- amount fields (`bigint` in wei-like units)
- `slippage` (must be `0 < slippage < 100`)
- `userAddress`
- For bridge: `sourceChainId` (1 | 8453), `destChainId` (1 | 8453), `token` (key or OFT address), `amount`, `recipient`
- For fxSAVE: `userAddress`; for deposit `tokenIn` (`usdc`|`fxUSD`|`fxUSDBasePool`), `amount` (bigint), optional `slippage`; for withdraw `tokenOut`, `amount` (shares wei), `instant` (boolean), optional `slippage` when instant; for claim use `getRedeemTx` when cooldown complete
3. Create `FxSdk` once and reuse it.
4. Return SDK result first (routes/tx plan), then optionally provide transaction sending loop.
5. Keep nonce order from SDK-provided `txs`; send transactions sequentially. **Wait for each tx receipt before sending the next.**
6. After all txs are confirmed, wait at least one block before querying balances or positions — on-chain state may lag the receipt.
7. Validate inputs and surface SDK error messages directly when possible.
8. If input comes from `agent-tools.json` style payloads, convert amount strings to `bigint` before SDK calls.

## Project Ground Truth

Repo: https://github.com/aladdindao/fx-sdk.git

Treat these as canonical project references before generating code:

- `AGENTS.md`
- `README.md`
- `agent-tools.json`

## Canonical Imports

```ts
import { FxSdk, tokens } from '@aladdindao/fx-sdk'
```

Use custom RPC only when provided:

```ts
const sdk = new FxSdk({ rpcUrl, chainId: 1 })
```

## Method Map

- `sdk.getPositions({ userAddress, market, type })`: read-only; returns `PositionInfo[]` (positionId, rawColls, rawDebts, currentLeverage, lsdLeverage, rawCollsToken, rawDebtsToken, rawCollsDecimals, rawDebtsDecimals).
- `sdk.increasePosition(...)`: open new position (`positionId: 0`) or add collateral/leverage.
- `sdk.reducePosition(...)`: reduce or close (`isClosePosition: true`).
- `sdk.adjustPositionLeverage(...)`: rebalance leverage for existing position.
- `sdk.depositAndMint(...)`: long pool only.
- `sdk.repayAndWithdraw(...)`: long pool only.
- `sdk.getBridgeQuote(...)`: fee quote for LayerZero V2 OFT bridge (Base <-> Ethereum). Use source chain RPC.
- `sdk.buildBridgeTx(...)`: build tx payload (to, data, value) to send on source chain; then send with wallet (same pattern as position txs). **When Ethereum is source chain, user must approve `tx.to` (RootEndPointV2) to spend the token before sending the bridge tx.**

**fxSAVE**

- `sdk.getFxSaveConfig()`: fxSAVE protocol totals and config (totalSupplyWei, totalAssetsWei, cooldownPeriodSeconds, instantRedeemFeeRatio, expenseRatio, harvesterRatio, threshold); no user address required.
- `sdk.getFxSaveBalance({ userAddress })`: fxSAVE balance (shares wei, optional assets wei).
- `sdk.getFxSaveRedeemStatus({ userAddress })`: pending redeem amount, cooldown, redeemableAt, isCooldownComplete.
- `sdk.getFxSaveClaimable({ userAddress })`: redeem status plus `previewReceive` (amountYieldOutWei, amountStableOutWei from previewRedeem — fxUSD + USDC to receive on claim).
- `sdk.getRedeemTx({ userAddress, receiver? })`: build claim tx when isCooldownComplete (uses `claim(receiver)`); execute txs in order.
- `sdk.depositFxSave({ userAddress, tokenIn, amount, slippage? })`: deposit USDC/fxUSD/basePool; returns `{ txs }` (approve + deposit).
- `sdk.withdrawFxSave({ userAddress, tokenOut, amount, instant?, slippage? })`: tokenOut `fxUSDBasePool` → redeem; usdc/fxUSD and !instant → requestRedeem; usdc/fxUSD and instant → approve + instantRedeemFromFxSave; execute txs in order.

## Token Addresses

| Token | Ethereum | Base |
|-------|----------|------|
| fxUSD | `0x085780639CC2cACd35E474e71f4d000e2405d8f6` | `0x55380fe7A1910dFf29A47B622057ab4139DA42C5` |

Use `tokens.fxUSD` in SDK calls on Ethereum; pass the Base address directly when building bridge txs with `sourceChainId: 8453`.

## Token Constraints

Honor SDK token checks:

- **Position (ETH/BTC)**  
  - ETH market: `eth`, `stETH`, `weth`, `wstETH`, `usdc`, `usdt`, `fxUSD`  
  - BTC market: `WBTC`, `usdc`, `usdt`, `fxUSD`

- **depositAndMint / repayAndWithdraw** (long only)  
  - ETH long: `eth` | `stETH` | `weth` | `wstETH`  
  - BTC long: `WBTC`

- **fxSAVE**  
  - `tokenIn` / `tokenOut`: `usdc` | `fxUSD` | `fxUSDBasePool`  
  - `fxUSDBasePool` → direct redeem; `usdc`/`fxUSD` → requestRedeem (cooldown) or instant (fee + slippage)  
  - Amounts in wei (18 decimals for fxSAVE shares; 6 for USDC)

## Common Errors

- `"Input amount must be greater than 0"` / `"Amount to reduce must be greater than 0"` → amount must be positive bigint.
- `"Slippage must be between 0 and 100 (exclusive)"` → slippage must be a number in `(0, 100)`.
- `"... must be a valid Ethereum address"` → use valid 0x address or `tokens.*`.
- `"User is not the owner of this position"` → caller must own `positionId`; verify with `getPositions` first.
- `"Input/Output/Deposit/Withdraw token address must be ..."` → use allowed token for the market (see Token Constraints).
- Bridge: `"Unsupported bridge chainId"` → each of `sourceChainId`/`destChainId` must be `1` or `8453` and they must differ. `"Unsupported bridge token"` → use `fxUSD`, `fxSAVE`, or valid OFT address on source chain.
- fxSAVE: `tokenIn`/`tokenOut` must be `usdc`, `fxUSD`, or `fxUSDBasePool`. Instant withdraw requires `slippage`.

## Output Style For Agent Tasks

When user asks to integrate SDK into an AI agent, return:

1. A minimal adapter function with typed input.
2. A safe dry-run mode (`planOnly`) that returns SDK routes without sending transactions.
3. A transaction executor function that consumes one selected route/result and sends `txs` in nonce order.
4. A post-execution step that waits ≥1 block then queries updated balance/positions to confirm the result.
5. A validation checklist and command list.

## Tool Schema Interop

If user provides values from `agent-tools.json`:

- Parse wei strings with `BigInt(value)`.
- Keep `positionId` as number.
- Keep `slippage` as number in `(0, 100)`.
- Normalize token addresses with `tokens.*` when possible.
- For fxSAVE tools, convert `amountWei` string to bigint; use `tokenIn`/`tokenOut` as-is (usdc, fxUSD, fxUSDBasePool).

## Project-Specific References

Read these files when examples are required:

- `example/increase-position.ts`
- `example/reduce-position.ts`
- `example/adjust-position-leverage.ts`
- `example/deposit-and-mint.ts`
- `example/repay-and-withdraw.ts`
- `example/get-positions.ts`
- `example/layerzero-bridge.ts`
- `example/get-fxsave-balance.ts`
- `example/get-fxsave-config.ts`
- `example/fxsave-deposit.ts`
- `example/fxsave-withdraw.ts`
- `example/fxsave-claim.ts` (redeem status + claimable preview + claim; uses getFxSaveClaimable, getRedeemTx)

For reusable request shapes, adapter pattern, and test checklist, read:

- `references/README.md` — index of reference files and when to use each
- `references/sdk-playbook.md` — request templates for all methods, minimal snippets, validation checklist
- `references/agent-adapter-example.ts` — typed FxAction adapter and sample payloads
