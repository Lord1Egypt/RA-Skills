---
name: galleon-compound-borrow
description: "Use when planning a Compound III Comet base-asset borrow, repayment or collateral withdrawal and checking baseBorrowMin and collateral factors."
license: MIT
compatibility: "Read-only EVM RPC or official provider tools; Bun is optional for offline examples. No signer required."
metadata:
  version: "0.3.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Compound III borrowing

Work on one **Comet deployment**, not Compound V2 cTokens. Resolve chain, Comet proxy, base token and account. Compound III borrows one base asset per market; a supplied collateral asset does not earn the base supply interest rate.

## Read the position

Read `baseToken()`, base decimals, `baseBorrowMin()`, `balanceOf(account)`, `borrowBalanceOf(account)`, `numAssets()`, and each `getAssetInfo(index)`. For each collateral, read `collateralBalanceOf(account, asset)`, its scale, priceFeed, borrowCollateralFactor, liquidateCollateralFactor and supplyCap. Read prices through Comet's `getPrice(feed)` and retain their scales. Do not use an unrelated market's USDC configuration for a WETH base market.

Read `isBorrowCollateralized(account)` and `isLiquidatable(account)`, plus supply/withdraw pause flags. Inspect utilization and rates through the deployment's documented rate functions; APR estimates must disclose accrual interval and exclude rewards unless valued separately. Check available base liquidity independently from collateral value.

## Construct the action

Compound III uses `withdraw(baseToken, amount)` to remove base supply and then create debt if the withdrawal exceeds the positive base balance. If supply is 400 and withdrawal is 1,000, the new debt is about 600 before accrual, not 1,000. A new borrow must satisfy the configured minimum position size. Do not increase an amount merely to meet `baseBorrowMin` without authorization for the larger debt.

Calculate two limits separately: borrow capacity from borrowCollateralFactor and liquidation capacity from liquidateCollateralFactor. Passing liquidation capacity is insufficient for a new borrow. Simulate the actual withdrawal to handle accrued indices, rounding and configuration exactly; an offchain budget alone is not acceptance.

Repaying uses `supply(baseToken, amount)`. It reduces debt first; excess becomes base supply. Collateral supply is different and does not repay debt. An ERC20 approval permits supply, while Comet manager `allow` grants account-management authority. A direct self-action should not silently introduce a manager or Bulker approval.

For withdrawal of collateral, model remaining collateral and debt at current and stressed oracle prices. An LTV-style estimate cannot substitute for both protocol boolean checks. After execution, reread base supply, debt and collateral individually; a successful approval or supply event is insufficient to prove a requested borrow or full debt repayment.

## Evidence and completion

Return the requested decision, exact deployment and chain, block/time, raw-unit observations, calculation assumptions, and the next missing read. Distinguish an indexed estimate, an onchain read, a simulated call and a confirmed transaction. Research ends with an actionable decision record; it does not require connecting a wallet.

For a requested write, prepare the complete unsigned sequence and simulate with the actual sender, amount, recipient and allowance state. Preserve authorization already supplied; research does not grant debt, spending or signing authority. Never request keys. After an authorized transaction, verify its receipt and the relevant balance or position change. On an ambiguous timeout, reconcile its hash and nonce before retrying.

Read [protocol references and worked record](references/recipe.md) only for the selected operation. Documentation checked 2026-09-27; refresh deployments and current parameters at use time. This directory is independently installable.
