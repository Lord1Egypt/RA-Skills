# EVK live borrow checklist

Use this checklist before running a tiny live borrow canary.

## What this skill proves
- the target borrow vault can issue real debt
- the intended collateral vault share token is accepted by the borrow vault's oracle and LTV config
- the account can rotate into the intended EVC state
- the proof can be isolated to one collateral path when requested

## What this skill does not prove by itself
- large borrow sizing safety
- liquidation safety under volatility
- multi-hop swap portability across every chain
- router compatibility for non Uniswap V3 style venues
- production monitoring or automated unwinds

## Required inputs
Gather these before building the config:
- `rpcUrl`
- `accountAddress`
- `signerEnvName` for live mode
- `operatorAck` for live mode
- wrapped native token address and decimals
- borrow asset address and decimals
- collateral asset address and decimals
- borrow vault address
- collateral vault address
- EVC address
- tiny `borrowAmount`

Optional but often needed:
- stale collateral vaults to disable
- stale controllers to disable
- `repayTopUp` if the debt asset is the wrapped native token
- `repaySwap` if the wallet needs to source the debt asset before repayment
- `collateralSwap` if the wallet needs to source the collateral asset before deposit

## Acceptance criteria before live send
Do not claim success unless all relevant items are true:
- the borrow vault has cash
- the borrow vault has an LTV link for the target collateral vault
- the borrow vault oracle can price the collateral vault share token into the unit of account
- the wallet has enough gas
- the post-rotation EVC state matches the proof you want to claim
- every live swap has an explicit nonzero `amountOutMinimum`
- unlimited approval is enabled only when the operator explicitly opted in

## Config design notes
The bundled executor reads a JSON config with these top-level sections:
- `rpcUrl`, `chainLabel`, `accountAddress`, `signerEnvName`, `operatorAck`
- `tokens`
  - `wrappedNative`
  - `borrowAsset`
  - `collateralAsset`
- `vaults`
  - `borrowVault`
  - `collateralVault`
  - `disableCollateral` array
- `evc`
  - `address`
  - `enableController`
  - `controllersToDisable` array
- `actions`
  - `repayExistingDebt`
  - `depositFullCollateralBalance`
  - `borrowAmount`
- `approvalPolicy`
  - `mode = exact | unlimited`
- `repayTopUp`, `repaySwap`, `collateralSwap`

Legacy configs may still use `privateKeyEnv` and `liveAcknowledgement`, but prefer `signerEnvName` and `operatorAck` for new configs.

## Adapting to other assets and chains
- Change token decimals, not just symbols.
- Change the wrapped native token per chain.
- Change the router and fee tier per venue.
- If there is no compatible single-hop router, source assets another way and disable the swap step.
- If the proof asset is not the wrapped native token, prefer `repaySwap` or pre-fund the wallet.
- If the controller is already correct, leave `enableController` false.
- If the proof must be isolated, list every stale collateral vault that must be disabled first.

## Canonical isolated proof sequence
This is the clean sequence that produced the strongest evidence in the Arbitrum canary:
1. repay old debt
2. source fresh collateral asset
3. deposit that asset into the target collateral vault
4. disable stale collateral vaults in EVC
5. leave only the target collateral path enabled
6. borrow a tiny fresh amount from the target borrow vault
7. report debt, enabled collaterals, and collateral-vault balance

## When to stop instead of forcing it
Stop and report the blocker if:
- the oracle cannot quote the collateral share token
- EVC controller rotation reverts and you cannot safely clear the old controller
- the wallet cannot source the repay or collateral asset
- the vault cash is too low
- the swap venue is not actually compatible with the configured router ABI
- a live swap is missing an explicit nonzero `amountOutMinimum`
- preview reveals that the flow would prove something weaker than the user asked for

## Suggested command pattern
Preview:
`node scripts/evk_live_borrow_proof.js --config <path>`

Live:
`node scripts/evk_live_borrow_proof.js --config <path> --live`

Keep the runtime config outside git if it contains a real wallet address or secrets.
