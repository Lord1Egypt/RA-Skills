# Binance Limits and Error Handling

Treat limits and error codes as operational signals, not generic failures.

## HTTP status behavior

- `4XX` indicates request or rule violations.
- `403` indicates WAF rule violation.
- `409` can appear on cancel-replace partial success.
- `429` indicates rate-limit hit.
- `418` indicates automated IP ban after repeated limit abuse.
- `5XX` indicates server-side uncertainty; do not assume execution failed.

## Critical Spot error codes

- `-1003`: too many requests, reduce request rate immediately.
- `-1007`: backend timeout, execution status unknown, reconcile before retry.
- `-1021`: timestamp outside recvWindow, resync server time.
- `-1022`: invalid signature, rebuild canonical payload and re-sign.

## Backoff policy

1. On `429`, pause and exponentially back off.
2. Respect `retryAfter` when provided.
3. On `418`, stop all traffic until ban expiry.
4. Reduce concurrency and lower polling frequency after recovery.

## Unknown execution status (`-1007`)

1. Query order state with `GET /api/v3/order`.
2. Check user-data stream `executionReport` events.
3. Only submit replacement order after proving original order did not execute.

## Weight-aware planning

- Expensive routes consume more `REQUEST_WEIGHT`.
- Parse response `rateLimits` fields when available.
- Move repetitive reads from REST polling to streams where possible.
