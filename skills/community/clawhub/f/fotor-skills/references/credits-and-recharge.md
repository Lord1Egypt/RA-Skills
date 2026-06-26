# Credits and Recharge

Use this reference when the user asks about account credits, remaining balance, recharge, payment links, or when a task fails because credits are insufficient.

## Credit Lookup

For account credit checks such as total credits or remaining credits, use the SDK client directly instead of `run_task.py`.

```python
import os
from fotor_sdk import FotorClient

client = FotorClient(
    api_key=os.environ["FOTOR_OPENAPI_KEY"],
    endpoint=os.environ.get("FOTOR_OPENAPI_ENDPOINT", "https://api-b.fotor.com"),
)
credits = client.get_credits_sync()
print("credits:", credits)
```

Returns a dict like:

```python
{"businessId": "", "total": 2000, "remaining": 1973}
```

## Recharge Links

If the user asks how to recharge, buy more credits, top up, or purchase tokens, call the payment-links endpoint directly with the same API key:

```bash
curl -sS -X GET https://api-b.fotor.com/v1/payment/links \
  -H "Authorization: Bearer $FOTOR_OPENAPI_KEY"
```

Successful responses look like:

```json
{
  "code": "000",
  "msg": "success",
  "data": [
    {
      "url": "https://api-b.fotor.com/v1/recharge/...",
      "planName": "500 Tokens (for 2 years)",
      "credits": 500,
      "currency": "USD",
      "amount": 39.99,
      "urlExpireTime": "2026-04-03T03:05:19Z"
    }
  ]
}
```

Field meanings:

- `url`: payment link for that package
- `planName`: display name of the package
- `credits`: tokens included after purchase
- `currency`: billing currency
- `amount`: price
- `urlExpireTime`: payment link expiration time returned by the API as an ISO 8601 UTC timestamp string

## Recharge Guidance Rules

- Summarize the available plans in plain language before listing raw URLs.
- Tell the user they can open any returned `url` to complete the purchase.
- Keep `urlExpireTime` in the returned result structure for internal use, but do not surface the raw timestamp to users by default.
- When guiding the user, simply say the payment link is valid for 30 minutes.
- If the returned payment link has already expired or is close to expiry, fetch fresh links again before asking the user to pay.
- When helpful, suggest the smallest plan that covers the user's immediate task, but do not invent package details that were not returned by the API.
- If the user asked about remaining balance first, answer the balance question directly and then offer to fetch recharge options only if they need more credits.

## Insufficient Credits

Treat any task failure containing `code=510` or `No enough credits` as insufficient credits, even when the error string combines primary and fallback failures such as `primary=No enough credits (code=510); fallback=No enough credits (code=510)`.

- When using `scripts/run_task.py`, expect insufficient-credit failures to return immediately without fallback retry.
- Explain that the generation did not succeed because the account currently lacks enough credits.
- After explaining the failure, fetch the latest payment links and present the recharge options instead of ending with the raw error.
- After recharge guidance, tell the user they can retry the same image or video request once credits are available.
