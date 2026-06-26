# Session Lifecycle

## Opening a session

A session is opened automatically on the first successful `tools/call` with `payment-signature`.
The response includes these headers:

```
x-session-id: {uuid}
payment-response: {base64_json}
```

The `payment-response` header (base64-encoded JSON) contains settlement confirmation:
```json
{
  "success": true,
  "network": "eip155:143",
  "transaction": "0x<tx_hash>",
  "payer": "0x<wallet_address>",
  "sessionId": "<session_uuid>"
}
```

Save `x-session-id` for subsequent calls. The `transaction` hash can be used to verify on-chain settlement.

The session is tied to an escrow (chain + escrow_id) and remains open until the budget is
exhausted or a timeout expires.

## Using a session

Every subsequent `tools/call` within the session:

```
x-session-id: {uuid}
x-idempotency-key: {new_uuid_each_call}
```

Do not send `payment-signature`. The gatekeeper deducts the call cost from the reserved budget.

## Error codes

| HTTP | Meaning | Action |
|------|---------|--------|
| `402` | No payment and no session | Run payment flow from step 3 |
| `200` | Success | Save `x-session-id` if present |
| `409` | Session conflict (duplicate escrow) | Restart flow from step 3 |
| `410` | Session closed or expired | Restart flow from step 3 |
| `402` (again) | Budget exhausted | Make a new payment |

## Selecting a payment network

The network is chosen from `payment-required.accepts[*].network` at the payment step.
If multiple networks are available (e.g. Base and Monad), the client picks one and signs
`payment-signature` for that network only.

## Session close reasons

- `manual` — explicit close call
- `budget_exhausted` — escrow budget fully spent
- `idle_timeout` — no requests for 15 minutes
- `hard_ttl` — absolute session TTL of 90 minutes reached
- `client_disconnect` — client dropped the SSE connection

## Refund

There is no explicit client-side `refund` step in this skill flow.
After session close, the server runs the release/refund flow automatically:
- actual cost is charged
- unused remainder is returned via escrow contract logic

## Idempotency

`x-idempotency-key` is required on every `tools/call`. It allows safe retries on network
errors — a repeated request with the same key returns the same result without double-billing.

Generate a new UUID for each new logical call.
