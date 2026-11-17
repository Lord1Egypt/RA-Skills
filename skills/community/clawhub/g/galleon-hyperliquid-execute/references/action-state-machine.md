# Action state machine

```text
draft -> reviewed -> approved -> persisted -> sent
sent -> rejected | resting | partially-filled | filled | trigger-wait | unknown
resting/trigger-wait/partially-filled -> reconciled updates
unknown -> found | expired-unconfirmed | unresolved
```

## Before send

Persist ticket revision, action digest, client order IDs, signer, account, network, nonce owner, expiry, and send intent. The durable record must exist before bytes leave the process.

## Send

Submit once with a finite client timeout. Do not wrap in transport retries. Capture local send time and the raw response or exception.

Interpret top-level action rejection separately from per-order statuses. A batch can contain mixed leg results depending on the client and action semantics; inspect every leg.

## Reconcile

Use client order ID or order ID, detailed open orders, fills from the send window, positions, balances, leverage, and margin. Persist each observation and its time.

## Unknown result

A timeout, disconnect, 5xx, or exception after transmission means the action may have arrived.

1. Do not resend.
2. Query each client order ID, open orders, fills, and resulting account state.
3. If found, continue from the observed state.
4. If absent, keep the result unknown. Negative reads do not prove non-arrival.
5. Once the signed expiry has passed, repeat reconciliation. The original action is then incapable of late acceptance under the documented expiry rule.
6. If no expiry was available, stop. A nonce invalidation is a separate write and requires explicit approval and proof before any replacement.
7. Any replacement is a new ticket with fresh client IDs, nonce, expiry, risk sign-off, and approval.

## Done

An action is done only when the exchange record and account state agree on its terminal or resting result and the remaining exposure has verified protection. `expired-unconfirmed` is a terminal uncertainty, not success or rejection.
