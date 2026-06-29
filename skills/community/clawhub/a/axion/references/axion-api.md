# Axion API reference

Snapshot of the canonical reference at https://axion.eternis.ai/docs.md. When in
doubt, fetch that URL for the latest.

Base URL: `https://api.axion.eternis.ai`
Auth: `Authorization: Bearer axn_sk_...` on every request.

Forecasts run asynchronously: start one, then poll until it reaches a terminal
status. A positive credit balance is required to start a forecast.

## POST /forecasts

Start a forecast thread, or continue an existing one.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| input | string | required | The question or analysis prompt. |
| id | string | optional | Existing thread ID, for follow-up messages. |
| max_forecasts | integer | optional | Number of forecasts to generate (1–10). Default 1. |
| effort | string | optional | Analysis depth: `low`, `medium`, or `high`. Default `medium`. |
| webhook_url | string | optional | URL to receive a POST callback on completion or failure. |

Request:

```json
{ "input": "Will the Fed cut rates in June 2026?", "effort": "high" }
```

Response (201):

```json
{ "id": "thread_abc123", "input": "...", "preliminary_result": null, "status": "starting" }
```

## GET /forecasts/{thread_id}

Poll status and results. Status values: `starting`, `in_progress`, `completed`, `failed`.

Response (200) carries `status`, `result` (prose synthesis), `credits_consumed`,
and `forecasts[]`. Each forecast:

| Field | Description |
| --- | --- |
| forecast_text | The claim being forecast. |
| probability | 0–1. |
| confidence_lower / confidence_upper | 0–1 interval bounds. |
| resolution_date | When the claim resolves. |
| reasoning | The evidence and logic behind the probability. |
| concludes_at, is_concluded, outcome | Resolution tracking; `outcome` is null until concluded. |

## Other endpoints

- `GET /forecasts`: list all threads for the account.
- `POST /forecasts/{thread_id}/stop`: cancel an in-progress forecast (consumed credits still charged).
- `POST /forecasts/{thread_id}/share` / `.../unshare`: toggle public visibility; share returns `{ "share_url": "/share/..." }`.
- `DELETE /forecasts/{thread_id}`: delete a thread.
- `GET /account/balance`: `{ "credits": 3750 }`.
- `POST /account/credits/purchase`: `{ "amount": 50 }` returns `{ "checkout_url": "https://checkout.stripe.com/..." }`. Minimum $50.

## Webhooks

If `webhook_url` is set on creation, Axion POSTs the full `GET /forecasts/{thread_id}`
payload when the thread reaches `completed` or `failed`. Best-effort, up to 3
retries; poll as a fallback.

## Errors

JSON body with an `error` field. Codes: 400 invalid request · 401 invalid/missing
key · 402 insufficient credits · 404 thread not found · 422 invalid body · 429 too
many concurrent threads (max 10) · 500 internal error.

## Credits

Prepaid, billed separately from the monthly plan. $1 = 100 credits, $50 minimum.
Deducted per message by token usage across all models (Opus 4.8 and Sonnet 4.6).
Max 10 concurrent in-progress threads per account.

## Example: create and poll (Python)

```python
import requests, time

API_KEY = "axn_sk_..."
BASE = "https://api.axion.eternis.ai"
headers = {"Authorization": f"Bearer {API_KEY}"}

r = requests.post(f"{BASE}/forecasts", headers=headers,
                  json={"input": "Will the Fed cut rates in June 2026?", "effort": "high"})
thread_id = r.json()["id"]

while True:
    data = requests.get(f"{BASE}/forecasts/{thread_id}", headers=headers).json()
    if data["status"] in ("completed", "failed"):
        break
    time.sleep(5)

for f in data["forecasts"]:
    print(f["forecast_text"], f["probability"])
```
