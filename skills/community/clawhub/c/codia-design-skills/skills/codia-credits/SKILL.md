---
name: codia-credits
description: Check Codia Open API credit balance from AI agents. Trigger when the user asks for Codia credits, balance, quota, or whether enough credits remain for design API work.
api: credits
endpoint: GET /v2/open/credits
cli: codia-design credits
credits_per_call: 0
sync: true
response_type: object
---

# codia-credits

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Query the credits balance and usage of the current API Key.

## CLI Command

```bash
codia-design credits
```

No parameters.

## Response

```json
{
  "ok": true,
  "data": {
    "product": "open_api",
    "available_credits": 850.0,
    "monthly_credits_remaining": 500.0,
    "topup_credits_remaining": 350.0,
    "used_credits": 150.0,
    "total_credits": 1000,
    "current_period_end": "2026-06-01T00:00:00Z",
    "next_reset_at": "2026-06-01T00:00:00Z",
    "auto_recharge_enabled": false,
    "low_balance_threshold": 100,
    "auto_recharge_credits": 500,
    "monthly_max_recharge_credits": 2000
  }
}
```

| Field | Type | Description |
|---|---|---|
| `available_credits` | number | Current available credits (sum of monthly + one-time recharge). `-1` means no limit |
| `monthly_credits_remaining` | number | The remaining amount of subscription credits this month |
| `topup_credits_remaining` | number | The remaining amount of one-time recharge credits |
| `used_credits` | number | Total credits consumed this month |
| `total_credits` | number | The total credits quota for this month. `-1` means no limit |
| `current_period_end` | string | The end time of the current billing period (RFC3339) |
| `next_reset_at` | string | The next monthly credits reset time (RFC3339) |
| `auto_recharge_enabled` | boolean | Whether to enable automatic recharge |
| `low_balance_threshold` | number | The balance threshold that triggers automatic recharge |
| `auto_recharge_credits` | number | The number of credits for each automatic recharge |
| `monthly_max_recharge_credits` | number | Maximum monthly automatic recharge credits limit |

## Usage Example

```bash
# Check the balance directly when the user asks about credits or quota
codia-design credits
```

## Errors & Billing

**Credit consumption**: 0 (the query itself does not consume credits)
