# Costs, billing and retries

Generated from the API spec - do not edit by hand.

## Prices

| Endpoint | Price |
|---|---|
| `/v2/product-details` | $0.003 per call |
| `/v2/product-reviews` | $0.003 per call |
| `/search` | $0.003 per call |
| `/product` | $0.0024 per item (max 20) |
| `/stock` | $0.0045 per item (max 10) |
| `/v2/best-sellers` | $0.003 per call |
| `/v2/deals` | $0.003 per call |
| `/seller-profile` | $0.0036 per item (max 10) |
| `/v2/seller-products` | $0.003 per call |
| `/v2/seller-reviews` | $0.003 per call |

Batch endpoints are billed per item. Without a key they are cheaper per item
than the single-item equivalents; on a key a `/product` ASIN costs the same
one request as `/v2/product-details`, so the batch saves calls, not money.
Prefer them for more than one item, except that the `/product` record has
no best-seller ranks, category path or merchant id: for those, call
`/v2/product-details` per ASIN.

## What each status means, and whether it costs money

| Status | Billed? | Meaning and what to do |
|---|---|---|
| `400` | no | Bad input (bad ASIN format, unknown geo, missing required param), or a page past the last one Amazon serves for a list (`code: page_out_of_range`, with `reachable_pages`). On agent.apiguru.app an `api_key` in the URL is refused the same way (`code: api_key_in_query`): send it as the X-API-KEY header. NOT billed. |
| `401` | - | Missing or invalid API key on the keyed path. |
| `402` | - | Payment required. On the agent path this carries a PAYMENT-REQUIRED challenge (over MCP: an x402 PaymentRequired tool result, payable in-band via _meta["x402/payment"]). On the keyed path it means the account balance is exhausted. |
| `403` | - | Account disabled, or no active subscription plan. |
| `404` | **yes** | The ASIN genuinely does not exist on that marketplace. BILLED - the lookup was performed and the bad input was the caller's. Retrying will not help; try a different geo. |
| `413` | - | Too many items in a batch request. |
| `429` | no | Per-second rate limit exceeded for the plan (`code: rate_limited`, `Retry-After: 1`). NOT billed. Back off and retry. |
| `500` | no | Internal error. NOT billed. |
| `502` | no | Bad gateway. NOT billed. Same class as 503: retry with backoff. |
| `503` | no | Temporary failure on our side (`code: upstream_unavailable`). NOT billed. Safe and correct to retry. |
| `504` | no | Gateway timeout: no answer within 55 s, so agent.apiguru.app stopped the request before it was billed (`code: deadline_exceeded`). NOT billed. Retry once; a batch with fewer items answers sooner. |
| `timeout` | - | No response before your own client's deadline, or the connection dropped before the answer arrived. A keyless call without a payment is never billed. On an API key, or with an x402 payment attached, the request may still have completed, and is then billed like any answered call: do not repeat it automatically, ask the user. Some marketplaces answer more slowly than others; allow 60s rather than retrying early (agent.apiguru.app answers a 504 itself at 55 s). |

## Retry policy

Retry 429, 500, 502, 503 and 504 with backoff -- none of them are billed -- unless the error body says `retryable: false`. A call on a key or a payment that got no answer (a client-side timeout or a dropped connection) may have completed and been billed: do not repeat it automatically; tell the user and retry only if they agree. Allow 60s before treating a slow call as lost. Never retry 400, 401, 402, 403, 404 or 413: the request itself is the problem and repeating it will not change the answer.

Concretely (the same set `scripts/probe.py` retries):

```python
RETRYABLE = {429, 500, 502, 503, 504}   # answered, and not billed
for attempt in range(4):
    try:
        status, body = call(..., timeout=60)
    except OSError:                  # timeout or dropped connection: no answer
        if api_key:                  # may have finished and billed before it was lost:
            raise                    # stop, tell the user, retry only if they agree
        status, body = 0, None       # keyless and unpaid: never billed
    if (status in RETRYABLE or status == 0) and (body or {}).get('retryable') is not False:
        time.sleep(2 ** attempt)
        continue
    break                            # 200/400/402/404/413 are final
```

A body's `retryable` flag wins over the status table: a 5xx whose
cause is permanent says `retryable: false` and is not worth repeating.
A call with no answer is different: after a timeout or a dropped
connection on an API key (or with an x402 payment attached) the request
may still have completed and been billed, so it is never retried
automatically -- `scripts/probe.py` reports it and stops. Only a call
that never left the machine (the host name did not resolve, or the
connection was refused) is known to be unbilled.

## Free probes

The keyless gateway serves a few free requests per client per rolling
window before it starts charging. Response header
`X-Free-Probes-Remaining` tells you how many are left, and
`X-Price-Next-Call` what the next one will cost.
