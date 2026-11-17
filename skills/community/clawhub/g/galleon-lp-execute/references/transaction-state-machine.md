# Transaction state machine

Use this state machine for every write.

```text
DISCOVER -> BIND -> QUOTE -> BUILD
BUILD -> APPROVAL_REQUIRED | SIMULATE
APPROVAL_REQUIRED -> CONFIRM_APPROVAL -> SUBMIT_ONE -> RECEIPT -> REREAD -> BUILD
SIMULATE -> CONFIRM_ACTION -> SUBMIT_ONE -> RECEIPT -> REREAD -> RECONCILE
RECONCILE -> COMPLETE | BUILD_NEXT | STOP | RECOVER
```

## Discover and bind

Read the wallet and chain from the signer, not from prior conversation. Resolve contracts from current official deployment records and verify deployed bytecode. Bind a plan identifier or hash to all material fields.

## Quote and build

Use current onchain state or an official protocol integration. Add hard spend, receive, liquidity, price, slippage, impact, gas, and deadline limits. Reject empty calldata, placeholder payloads, unrecognized selectors, unknown multicalls, and values that exceed the plan.

Return either finite approvals or one ready action. Never treat action calldata built before approval receipts as current. Bind each phase to a canonical plan digest.

## Simulate and confirm

Simulate from the exact wallet with the exact native value. Decode nested calls, approvals, transfers, mints, burns, stakes, and claims. Compare expected state changes with the plan. Then obtain the exact confirmation contract. A confirmation binds the plan digest and all displayed terms.

## Submit one

Submit one transaction. Record the tool request ID, wallet transaction ID, chain hash, nonce, and submission time when available. Do not submit the next dependent transaction yet.

## Receipt and reread

Wait for a receipt on the bound chain. Check status, block, confirmations or finality, target, sender, nonce, logs, and effective gas. Reread balances, allowances, ownership, liquidity, fee or reward state, range, gauge custody, and loose assets.

## Reconcile

Compare the observed state with the expected diff. If exact, complete or build the next dependent step from the mined state. If different, stop and report the delta. Never continue from intended state.

Keep writes serialized per wallet and nonce. A parallel read is safe; parallel dependent writes are not.
