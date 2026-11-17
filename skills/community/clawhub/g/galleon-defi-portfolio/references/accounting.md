# Reconciliation and performance

These are explicit report conventions. Label them and adjust to the user's reporting purpose; do not present the result as a tax filing or audited statement.

## Position ledger

Each row should retain account, canonical chain, asset/deployment address (or native identity), protocol/position identifier, role, quantity/decimals, source block/time, price/currency/time, gross value, liability value and coverage status. Use precise decimal arithmetic; round at display boundaries. Two addresses with the same symbol remain different assets until an explicit representation mapping is established.

Map account-controlled claims without counting a wrapper and its backing twice. An aToken can represent supplied principal; a vault share can represent a basket; staked LP receipts can represent another receipt. Keep the ownership claim for equity and expand underlying exposure in a separate allocation view. Only expand the account's attributable fraction; never import the whole vault's TVL. Unclaimed rewards belong once, with claimability and pricing caveats.

Retain gross assets and liabilities even when net equity is small or negative. A borrow's debt may grow with accrued interest or use scaled units; use the protocol's current conversion. If provider net value already subtracts debt, do not subtract that debt again. Distinguish funding/interest accrual from principal changes and quote the observation time.

For derivatives, report account equity, collateral, unrealized PnL, notional and directional exposure in separate fields. Do not add full notional to net worth. A large market-neutral pair can have small net delta while retaining gross liquidation and counterparty risks.

## Pending and constrained assets

A submitted withdrawal request is not liquid cash. Preserve queue/request identity, underlying claim, completion condition and expected amount as uncertain until finalized. For a bridge, represent the in-transit claim once; reconcile source removal and destination arrival rather than counting both snapshots. An internal transfer among scoped accounts is not new portfolio capital.

Report unavailable prices, stale observations, spam/quarantined assets and nontransferable claims separately. A zero mark is not a synonym for missing data. Show priced net equity plus an unpriced-items count/quantity and explain coverage; a percentage allocation over priced assets must say that unpriced items are excluded.

## Performance and flows

For one consistent reporting currency and valuation basis:

`economic change = ending equity - starting equity - external contributions + external withdrawals`

This removes external capital flows but is not automatically realized PnL, a time-weighted return or a money-weighted return. Changes can combine market marks, interest, fees, rewards and trading. Reconcile residuals instead of attributing them arbitrarily.

Do not treat transfers between included accounts as contributions/withdrawals. Reclassify them if the reporting scope changes and disclose the scope break. A borrowed inflow is an asset plus a liability, not a deposit profit. Failed transfers and reverted transactions do not create position flows; gas costs may still exist.

Realized PnL requires disposal events and a stated cost-basis method with sufficiently complete history, including fees and asset transformations. A provider's 24-hour price change or wallet-value change is not realized profit. If history is missing, give observed balance/mark changes and the unresolved basis gap. Calculate time-weighted returns only with valuations bracketing relevant flows; use dated flows and a disclosed solver/convention for money-weighted returns. Do not compare yield rates across incompatible compounding periods or treat variable APY as a guarantee.

## Cash-flow journal

When the agent keeps its own flow journal, make entries append-only and idempotent. Derive each ID deterministically from chain, transaction hash, asset and kind, and aggregate every same-asset transfer log within one transaction into one net delta before recording; a second ID for the same flow doubles net positions. Record gas as a separate negative native-asset fee, and never enter a fee twice when a net trade delta already includes a token-denominated fee. Deposits and internal transfers are capital, not profit; a USD mark is a valuation, not a cash flow. If duplicates are found, fail closed on totals until receipts resolve them, and exclude reviewed rows with an audit reason rather than inserting reversing entries. Reconcile journal net deltas with chain balances at a recorded block before assigning any profit; a journal is an observation record, not proof of receipts.
