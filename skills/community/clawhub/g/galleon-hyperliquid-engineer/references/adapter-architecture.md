# Adapter architecture

Keep these components separate and typed:

```text
official metadata -> identity registry -> read adapter -> normalized state
                                              |             |
strategy or UI -> intent -> risk engine -> unsigned action  |
                                  |             |            |
approval record ------------------+------> signer boundary   |
                                                |            |
durable send ledger -> submit once -> raw response -> reconciler
                                                |            |
                                                +------ exchange state
```

## Contracts

- Identity registry resolves network, DEX, product class, coin, asset ID, precision, and margin table from current metadata.
- Read adapter returns `fresh`, `stale`, `partial`, `unavailable`, or `unsupported`, never a false empty success.
- Risk engine consumes normalized state and produces a pass or explicit gate failure.
- Unsigned action contains exact wire fields, client order IDs, account, network, expiry, and expected state change.
- Approval record binds a user-authored approval to the immutable action digest and expiry.
- Signer receives only an approved unsigned action. It owns private material and nonce serialization.
- Send ledger persists intent before submission and records exactly one transport attempt.
- Reconciler combines order status, open orders, fills, positions, balances, and account mode into a result.

Do not place strategy decisions, retries, or key loading inside the protocol adapter. Do not let a stream callback bypass the risk and approval contracts.
