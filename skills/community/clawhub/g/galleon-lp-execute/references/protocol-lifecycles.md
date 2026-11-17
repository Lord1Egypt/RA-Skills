# Protocol lifecycles

Verify current deployments and interfaces before using these lifecycle models.

## Uniswap v2

```text
approve tokens -> add liquidity -> receive LP token
approve LP token -> remove liquidity -> receive reserve share
```

Fees are normally embedded in reserves. There is no separate ordinary collect step. Confirm refund and minimum-amount behavior. Fee-on-transfer tokens require a supported path and additional scrutiny.

## Uniswap v3

```text
approve or permit tokens -> mint NFT
increase liquidity -> same NFT
decrease liquidity -> tokens owed
collect -> tokens transferred
zero liquidity and zero owed -> burn NFT
```

Decrease and collect are distinct. Confirm NFT owner, operator approval, recipient, ticks, amounts, minimums, and deadline.

## Uniswap v4

Use the deployed position manager and action model. Bind the full PoolKey. Verify hook permissions and hook data, manager unlock behavior, currency settlement, native value, Permit2 path, and nested actions. Do not reuse v3 calldata or infer safety from a matching pair and fee.

A hook-issued fungible share model has a different lifecycle: approve currencies, add proportional liquidity or use a reviewed zap, receive shares, then burn shares for proportional withdrawal. Verify all currencies, internal reserves, rate sources, minimum shares, per-currency minima, refunds, and whether swaps or adds can fail while withdrawal remains available.

## Aerodrome classic

```text
approve tokens -> add stable or volatile liquidity -> receive LP token
approve LP token -> deposit in gauge -> accrue verified rewards
claim rewards or withdraw gauge -> remove liquidity
```

The required order and fee ownership vary by deployed model. Verify router, pool factory, gauge, voter, reward token, epoch, and whether the LP route owns swap fees.

## Slipstream

```text
approve or permit tokens -> mint concentrated NFT
keep unstaked for verified fee rights
or approve and deposit or stake in gauge for verified emissions
unstake when required -> decrease -> collect -> burn when empty
```

Staking can forfeit swap fees. Verify gauge custody, reward accrual, fee rights, required unstaking, epoch timing, and stale reward triggers after every range change.

## Atomicity

Prefer protocol-supported atomic actions when all state changes can be simulated and decoded together. Do not force a multi-step venue lifecycle into an invented atomic transaction. For non-atomic sequences, checkpoint each mined state before building the next transaction.
