# Binance Troubleshooting

Use this runbook for frequent production failures.

## Signature invalid (`-1022`)

- Rebuild canonical param string exactly as sent.
- Ensure no hidden whitespace or URL-encoding mismatch.
- Confirm signing key type matches API key type.

## Timestamp out of range (`-1021`)

- Fetch server time each signed batch.
- Use server time offset if local clock drifts.
- Keep `recvWindow` conservative.

## Unknown order status (`-1007`)

- Do not send immediate duplicate orders.
- Query order by `orderId` or `clientOrderId`.
- Reconcile with `executionReport` events before retry decisions.

## Rate limit lockouts (`429` and `418`)

- Decrease request burst size and concurrent workers.
- Shift repeated price reads to streams.
- Resume traffic gradually after ban window expires.

## Silent WS disconnect patterns

- Rotate sockets before the 24-hour connection cap.
- Handle server ping frames and return pong quickly.
- Reconnect with jitter and re-subscribe deterministically.

## WAF blocks (`403`)

- Recheck endpoint path and request shape.
- Remove suspicious high-frequency or malformed traffic.
- Use documented endpoints only.

## Incident logging

Record every major incident in `~/binance/incidents.md` with error code, endpoint, and validated mitigation.
