# Target and calldata policy

## Allowlist by role and code

Each target must match the selected chain, protocol version, official deployment role, and expected deployed bytecode or verified implementation. A familiar address on another chain is not valid. Proxies require implementation and admin review.

## Decode before signing

Decode the outer selector and every nested call. Verify:

- target and function are needed for the confirmed action
- token addresses and token0/token1 order match the pool
- recipient and refund address are the user's wallet unless explicitly confirmed otherwise
- amounts, minimums, limits, ticks, fee, hook data, deadline, and native value match the plan
- no unexpected transfer, permit, delegatecall, approval, arbitrary call, bridge, swap, sweep, unwrap, or fee recipient exists

For swap-assisted liquidity actions, also bind quote provider, quote time, expiry, allowance target, router target, path, per-leg minimum output, and refund behavior. Reject a combined-value minimum when one required pool-token leg can fall below its mint requirement.

Reject opaque arbitrary calldata when a trusted decoder cannot explain it. Do not accept a frontend's label as a decode.

## Approval limits

Verify the exact spender. Prefer a bounded amount and expiry. Distinguish direct ERC-20 approval, NFT operator approval, Permit2 token allowance, Permit2 application authorization, and one-time signature transfer. Revoke residual authority when the confirmed plan requires it and the cleanup action is itself reviewed and confirmed.

Prefer approval of one NFT token ID over `setApprovalForAll`. Treat a transfer-and-callback utility as a contract call with encoded instructions, not as an ordinary NFT transfer.

## Plan freshness

Embed or enforce a deadline and price or state constraints. Reject stale placeholder calldata. If a transaction builder returns no calldata for a required live action, stop. Never submit an empty payload to make progress appear successful.
