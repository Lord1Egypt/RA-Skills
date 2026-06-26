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

## Config design notes
Build the proof config from the actual deployment outputs and live wallet state, not from memory.

The local executor reads a JSON config with these top-level sections:
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
- `repayTopUp`, `repaySwap`, `collateralSwap`

## Deployment output → proof config reminders
- take the borrow vault address from the fresh deployment result, not an older canary market
- take the collateral vault address from the collateral path you actually want to prove
- derive the EVC address from the live borrow vault or chain deployment context
- derive token decimals from live token contracts when possible
- keep stale controller and collateral cleanup lists tied to the proof wallet's current state

## Adapting to other assets and chains
- Change token decimals, not just symbols.
- Change the wrapped native token per chain.
- Change the router and fee tier per venue.
- If there is no compatible single-hop router, source assets another way and disable the swap step.
- If the proof asset is not the wrapped native token, prefer `repaySwap` or pre-fund the wallet.
- If the controller is already correct, leave `enableController` false.
- If the proof must be isolated, list every stale collateral vault that must be disabled first.
- Treat the proof path as generic across supported assets: build the config from the fresh deployment outputs and current wallet state, not from whichever asset pair happened to be used in an earlier canary.

## Canonical isolated proof sequence
Use this as the generic isolated proof sequence:
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
- preview reveals that the flow would prove something weaker than the user asked for

## Controller → executor handoff
The public skill plans the proof and generates the config.
The bundled skill executor executes it.

Canonical local executor path:
- `scripts/evk_live_borrow_proof.js`

Preflight checks:
1. confirm the installed skill bundle exists
2. confirm `scripts/evk_live_borrow_proof.js` exists
3. confirm the config file path is explicit
4. confirm the signer env name is supplied only through local runtime setup
5. run preview before considering `--live`

## Suggested command pattern
Preview:
`node ./scripts/evk_live_borrow_proof.js --config <path>`

Live:
`node ./scripts/evk_live_borrow_proof.js --config <path> --live`

For live mode, also require:
- `config.operatorAck` matches the script's required live-send acknowledgement phrase
- `config.accountAddress` matches the signer address derived from `signerEnvName`

Keep the runtime config outside git if it contains a real wallet address or secrets.
