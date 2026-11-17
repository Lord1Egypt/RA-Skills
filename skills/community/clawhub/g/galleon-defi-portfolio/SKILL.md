---
name: galleon-defi-portfolio
description: Reconcile cross-chain DeFi holdings, protocol positions, debt and cash flows into a sourced portfolio report or rebalance plan. Use when assessing exposure, net asset value, performance or treasury monitoring while avoiding receipt-token double counts and confusing price changes with investment profit.
license: MIT
compatibility: Portable agent instructions. Optional Zerion, DeBank, CoinGecko, DefiLlama and protocol reads require supported coverage and the user's own access. No custody, transaction execution or recurring scheduler is bundled.
metadata:
  author: Galleon Labs
  version: "0.2.1"
---

# DeFi portfolio and treasury

Answer what the selected accounts own, owe and can access, what changed, and what evidence is missing. A portfolio report or target allocation is not authorization to move funds.

## Start with the requested task

Read [task examples and user configuration](references/task-examples.md) for a completed example and recovery path. Apply only the workflow stages needed by the current request. Reuse supplied preferences and compatible tools; ask only for missing terms that affect this task. Public explanation or comparison does not require transaction fields. Keep any existing authorization within its exact scope.

## Define the scope

Establish included accounts and chains, ownership boundaries, reporting currency, valuation time, comparison period and purpose. Distinguish a watchlist from the user's own holdings. Preserve smart accounts, multisigs, exchange subaccounts and vault positions as separate identities; do not infer access to private exchange balances from an onchain address.

Use [provider interfaces](references/providers.md) to fetch bounded account data through existing official tools. Use filters and pagination deliberately: a wallet-token endpoint may omit protocol positions. Mark unsupported chains, partial pages, delayed indexers and missing accounts as coverage gaps, not zero balances. Record provider retrieval time and position observation time separately.

## Reconcile before aggregating

- Identify each position by chain namespace/ID, account, exact token or native-asset identity, protocol deployment, position ID and valuation block/time. Preserve provider IDs as opaque identifiers; a ticker or cross-chain logo is not a key.
- Represent quantities as base-unit integers plus decimals, or exact decimal strings. Keep conversion rates, units and sources. Avoid binary float rounding when reconciling raw balances or debt.
- Classify wallet holdings, supplied collateral, borrowed liabilities, LP/vault shares, staking/restaking receipts, locked positions, pending withdrawals/bridges and unclaimed rewards separately.
- Choose a valuation representation: receipt shares or their attributable underlying exposure. Never add both to equity. Break an LP position into underlying exposures for allocation without also counting its total value again. Reconcile provider overlap and internal account transfers.
- Show gross assets, debt and net equity. Keep leverage/notional exposure separate from equity; a derivative's notional is not cash value. Price stablecoins from evidence rather than assuming a dollar peg.

For receipt tokens, debt, pending states and performance calculations, apply [accounting rules](references/accounting.md). Corroborate material quantities and time-sensitive risk with chain or protocol state at a recorded block. Market APIs provide marks; they do not establish custody or immediate exit proceeds.

## Explain changes and propose actions

Separate deposits/withdrawals, internal transfers, price movement, fees/rewards, debt interest and trading effects. When cost basis or flow history is incomplete, report mark-to-market change with that limitation rather than inventing realized PnL or returns. Handle missing prices as unpriced exposure; do not quietly drop an asset from the denominator.

Use [report and rebalance workflow](references/reporting.md) to identify concentration, liquidity constraints, debt risk, exit queues and discrepancies. A rebalance plan should include dependencies, estimated costs, slippage limits, timing and the unchanged “do nothing” case. It must not execute, revoke approvals, enroll paid data, create a scheduler or publish private holdings without the user's corresponding request and authority.

## Deliver

Return net equity with its valuation time and coverage, gross assets/debt, allocation/exposure, changes with known flows, material risks and actionable unknowns. Link primary evidence and disclose stale or missing data. Keep private account mappings and snapshots in the user's approved location outside source control. If recurring reporting is requested, use the host's existing scheduler and storage conventions rather than creating a competing agent runtime.

Use [evaluation scenarios](references/evals.md) to test reporting behavior without paid APIs or real account actions.
