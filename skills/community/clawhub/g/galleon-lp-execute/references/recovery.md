# Recovery

Never retry an ambiguous write.

## Classify the result

- `not submitted`: the wallet or tool proves no transaction was created
- `submitted`: a chain hash and nonce exist, receipt pending
- `mined success`: receipt status succeeds and state reread matches
- `mined revert`: receipt status fails, no intended state change
- `replaced`: same nonce resolved to another hash
- `unknown`: evidence is insufficient

Timeout is not a result class. It moves the action to `unknown` until resolved.

## Resolve before action

1. Query the known transaction hash on the bound chain.
2. Query the sender and nonce for pending, mined, dropped, or replacement state.
3. Reread allowances, balances, ownership, liquidity, fee or reward state, and gauge custody.
4. Reconstruct the actual position state from chain evidence.
5. Compare it with the expected checkpoint.

Only a proven `not submitted` or `mined revert` state can return to planning without risk of duplicating the write. A dropped transaction still requires nonce and state proof.

## Partial sequence

If an approval succeeded but mint failed, report the live residual allowance. If a decrease succeeded but collect failed, report owed tokens and remaining liquidity. If unstake succeeded but removal failed, report NFT or LP custody. Build recovery from current state, never from the original intended sequence.

Do not hide or auto-clean residual state. Cleanup is a new explicit action with its own simulation and confirmation.
