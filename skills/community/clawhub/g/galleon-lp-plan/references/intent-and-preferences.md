# Intent and user preferences

The user chooses the objective, providers and operating style. This pack supports
passive inventory conversion, fee capture, incentive farming and research-only
planning without requiring one strategy, wallet product or maintenance schedule.
Preferences never authorize a transaction.

## Working context

Reuse supplied chain, public wallet, allowed protocols/tokens, pool or position,
base currency, capital bounds, horizon, inventory/loss constraints, maintenance
cadence, incentives preference, custody preference, slippage/gas limits and reporting
format. Keep source/revision and missing values. Use conversation context or a
user-selected artifact; do not require a hosted account or new configuration file.

Apply the latest explicit correction only to affected fields. A changed budget,
recipient, range or route expires dependent execution terms. Descriptions such as
"passive" or "high yield" can guide research but never supply a spend cap, acceptable
custodian, loss limit or approval scope. Offer labeled alternatives when those
choices matter; do not stall public research for missing wallet information.

## Intake by action

| Action | Required action-specific inputs | Preserve or omit |
| --- | --- | --- |
| Mint or add | Budget and maximum spend per token, recipient, pool/range or share model, horizon, inventory constraints, costs, approval terms and minima | Existing range for an increase unless a range change is explicitly requested |
| Collect fees or claim rewards | Exact owned position, claimable assets, requested claim scope, recipient, fee/gas caps, current staking/claim rights | No new range, deposit budget or automatic reinvestment |
| Decrease or exit | Exact liquidity/shares or fraction, asset minima and recipient, withdrawal/staking prerequisites, gas and conversion bounds if requested | Withdraw in kind unless conversion is part of the user's intent; do not silently swap to a preferred base currency |
| Recenter or compound | Old position and full transformation, destination range, maximum swaps/spends, minima, costs, custody/automation changes and dust handling | No extra principal or new operator authority by inference |
| Stake or unstake | Exact position/gauge, quantity, fee/reward rights, custody, lock/exit terms, approvals and costs | No claim, restake or auto-compound unless requested |

All actions retain fresh identity, target/calldata/value, simulation, deadline,
expected state and recovery checks. A non-applicable range or new-capital field is
marked not applicable with a reason, never filled with fabricated values.

## First useful answer

Lead with the proposed effect and whether the plan is ready, blocked or hypothetical.
For a comparison, show alternatives against the user's objective on the same cost
window. Keep exact amounts and transaction terms available in the plan contract.

Example: "Collect the verified claimable fees from NFT 42 to its owner, leaving
liquidity and range unchanged. Quote and simulation are missing, so this is an
unsigned non-executable draft. No swap, compounding or new capital is included."
