# Analysis output

Use this order.

## Verdict

One line: preferred pool, conditional choice, reject, or not assessable.

## Bound identity

Chain ID, protocol version, position model, pool address or PoolId, ordered token addresses or full currency set, fee, tick spacing or invariant, hook, share token, gauge, and observation block.

## Hard gates

| Gate | Result | Evidence |
|---|---|---|
| Identity | pass, fail, unknown | source and read |
| Tokens | pass, fail, unknown | transfer and control findings |
| Pool and hook | pass, fail, unknown | code and state findings |
| Yield | pass, fail, unknown | fees and incentives separated |
| Exit | pass, fail, unknown | quoted full unwind at size |

## Comparable economics

Use the same time windows and units. Show fees, incentives, costs, current depth, active-liquidity fit, and inventory risk. State what is measured, estimated, or unknown.

## Risks and invalidation

List the shortest set of facts that can cause material loss or reverse the choice. Name who controls each mutable parameter.

## Next action

State the one missing read or planning step. Do not include calldata or a wallet prompt.
