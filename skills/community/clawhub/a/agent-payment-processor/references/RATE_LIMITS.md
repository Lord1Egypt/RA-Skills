# Rate Limits

Use this reference when an agent or operator needs to handle throttling safely without assuming fixed operational thresholds.

Rate limits apply to protect platform stability and may change over time. Build integrations to handle throttling gracefully instead of depending on fixed thresholds.

## What To Expect

- Agreement creation and agreement updates are subject to request throttling.
- Metered proxy traffic is limited per active agreement.
- Total usage is also bounded by the agreement terms you created.
- Some payment rails may enforce additional spending caps.

When a limit is reached, the API returns HTTP `429` or a structured agreement or payment error.

## Retry Strategy

When you receive HTTP `429`:

1. Read the `Retry-After` header if present.
2. Otherwise, retry with short exponential backoff.
3. Keep retries bounded and surface the failure if the limit persists.

```python
import time

for attempt in range(3):
    try:
        result = client.post("/endpoint", json=data)
        break
    except Exception as e:
        if "429" in str(e) and attempt < 2:
            time.sleep(2 ** attempt)
            continue
        raise
```

## Best Practices

- Use the SDK for metered proxy calls so request metadata is added correctly.
- Avoid bursty traffic when recording usage or polling status.
- Cache or batch non-urgent reads in your own application where possible.
- Treat published limits as operational guidance, not a permanent contract.
- Surface persistent throttling to a human operator when retries do not resolve the issue.
