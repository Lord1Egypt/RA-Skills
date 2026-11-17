# Security invariants

## Identity

- Bind numeric chain ID and wallet address at every write boundary.
- Resolve deployments from current official records; verify code and proxy implementation.
- Bind ordered token addresses and decimals. Symbols are display fields.
- For v4, bind currencies, fee, tick spacing, hook, PoolKey, and PoolId together.
- For Aerodrome, bind factory, stable flag or tick spacing, router, position manager, gauge, voter, and reward token as applicable.

## Arithmetic

- Use exact integers through protocol math and serialization.
- Test decimal asymmetry, zero amounts, maximum values, rounding direction, negative ticks, boundary ticks, and upper-tick exclusivity.
- Use floor division for negative compressed ticks. Language truncation toward zero is wrong.
- Bound tick bitmap and log scans. Mark incomplete results.

## Tokens and approvals

- Test nonstandard return values, transfer taxes, rebases, pausing, blacklist rules, allowance reset, callbacks, and upgradeable behavior.
- Verify spender and approval mechanism. Bound amount and expiry where possible.
- Separate Permit2 token approval from application authorization and one-time signature transfer.
- Track residual approvals after partial failure.
- Prefer approval of one NFT token ID over standing operator approval. Enumerate active automation before transferring or transforming a position.

## Transactions

- Allowlist target roles, selectors, nested calls, native value, recipients, and refund recipients.
- Reject empty calldata, placeholder calldata, unknown multicalls, unexpected delegatecall, and opaque arbitrary execution.
- Enforce max spend, minimum receive or liquidity, price bounds, price impact, gas bounds, deadlines, and plan age.
- Simulate with the exact sender and native value.
- Serialize dependent writes by wallet and nonce.
- Never retry an ambiguous submission.
- Return approvals and ready action calldata as separate plan phases. Rebuild after approval receipts.
- Bind a canonical plan digest to every material transaction field and verify it again at receipt reconciliation.

## Hooks and callbacks

Treat each v4 hook as an independent application. Decode permissions from its address, inspect every enabled callback, admin and upgrade control, external calls, dynamic fees, deltas, and reentrancy assumptions. `beforeRemoveLiquidity` can block exits. Return-delta permissions can change what LPs deposit or receive. In callbacks, `msg.sender` should be the PoolManager and the `sender` parameter can be a router rather than the end user. Do not trust user identity decoded from hook data unless the router is authenticated. Fuzz hook data, callback ordering, delta settlement, and direct callback attempts. A verified PoolManager does not make a hook safe.

If a hook manages fungible shares and internal reserves, test reserve-to-balance reconciliation, transfer assumptions, rate-source failure, amplification or invariant changes, fee rounding, solver convergence, multi-currency refunds, and full withdrawal in degraded states.

## Reporting

A plan, quote, simulation, signature request, or submitted hash must have a distinct type from a mined receipt. Completion requires receipt status and a matching state reread.
