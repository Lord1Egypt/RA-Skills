# Pre-send checks

Run every item immediately before requesting final approval. Record PASS or the exact mismatch.

1. Ticket ID, immutable action digest, risk sign-off, requested approval phrase, and expiry refer to the same revision.
2. Network and REST endpoint equal the ticket. Mainnet is never inferred.
3. User or subaccount address equals the ticket. Signer is an approved API wallet for that account, not the account key.
4. Account abstraction mode is unchanged. Read every balance and margin surface required by that mode.
5. DEX, coin, asset ID, precision, margin table, and market status still match live metadata.
6. Current mid, mark, oracle, spread, and book impact remain within ticket tolerances.
7. Live position, order, balance, free margin, borrow state, action budget, and daily risk still pass.
8. Size is rounded down, price is valid, notional meets current minimum, leverage fits the post-trade margin tier, and available-to-trade covers the action.
9. Every order leg has a fresh persisted client order ID. The nonce belongs to the signer process. Expiry is encoded when supported.
10. The result leaves every open position protected. Partial-fill and unknown-result recovery paths are ready.
11. No earlier write by this signer remains unreconciled.
12. The trusted signer will show or enforce the same target, action, network, account, and digest.

Any failure stops the send. A changed field requires a new ticket or revision and new approval.
