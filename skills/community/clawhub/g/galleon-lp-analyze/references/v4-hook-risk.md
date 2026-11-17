# Uniswap v4 hook risk

Use this gate for every pool whose PoolKey has a nonzero hook.

## Bind the hook

- Resolve the PoolKey and derive the PoolId with the current official library.
- Decode the callback permission bits from the hook address and compare them with implemented callbacks.
- Verify source, deployed bytecode, proxy implementation, owners, roles, upgrade delays, pause paths, and fee controllers.
- Treat a mismatch between address permissions, verified source, and deployed code as a failed gate.
- Classify whether the hook preserves ordinary concentrated-liquidity accounting or implements its own reserves, invariant, fungible shares, or multi-pool accounting. Use [share-based hook analysis](share-based-hooks.md) for the latter.

## Fund-loss paths

- `beforeRemoveLiquidity` can block or condition withdrawals. Prove the user can exit under current and adverse state.
- Return-delta callbacks can change swap, deposit, or withdrawal amounts. Inspect all balance-delta signs, bounds, casts, and settlement paths.
- A hook with `beforeSwapReturnDelta` can claim it supplied output while retaining input. Do not accept a benign label as evidence.
- Dynamic fees can change after entry. Identify the controller, bounds, update delay, and current fee.
- External calls, callbacks, donated balances, and hook-owned liquidity add reentrancy and accounting surfaces.

## Identity and settlement

Hook callbacks should accept calls only from the bound PoolManager. Within a callback, `msg.sender` is the PoolManager. The callback `sender` can be a router, not the wallet that initiated the route. User identity carried in hook data is trustworthy only when the supplying router and encoding are authenticated.

Uniswap v4 requires all currency deltas to settle before the unlock completes. Review every take, sync, transfer, settle, mint, burn, and claim path. A successful swap does not prove liquidity can be removed.

## Exit proof

Simulate add, modify, fee collection, full removal, native currency settlement, and failure recovery from the intended wallet. Use the exact hook data and routing path. Test adverse fee, pause, admin, oracle, and callback states where possible.

Return `not assessable` if source, permissions, upgrade control, delta behavior, or a full exit cannot be verified.

Current primary references:

- [Uniswap AI v4 security foundations](https://github.com/Uniswap/uniswap-ai/tree/main/packages/plugins/uniswap-hooks/skills/v4-security-foundations)
- [Uniswap v4 hooks](https://developers.uniswap.org/docs/protocols/v4/concepts/hooks)
