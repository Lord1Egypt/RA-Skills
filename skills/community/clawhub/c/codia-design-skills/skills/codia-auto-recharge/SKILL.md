---
name: codia-auto-recharge
description: Manage Codia Open API automatic recharge settings from AI agents. Trigger when the user asks about auto recharge, quota top-up, recharge threshold, or recharge limits for Codia Design Skills.
api: auto-recharge
endpoint: GET /v2/open/auto_recharge  +  POST /v2/open/auto_recharge
cli: codia-design auto-recharge
credits_per_call: 0
sync: true
response_type: object
---

# codia-auto-recharge

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Query or set automatic recharge rules: automatically purchase credits when the balance is below the threshold.

## CLI Commands

```bash
#Query current settings
codia-design auto-recharge get

# Update settings
codia-design auto-recharge set \
  --enabled true \
  --threshold <CREDITS> \
  --credits <RECHARGE_AMOUNT> \
  --monthly_max <MAX_PER_MONTH>
```

## Parameters (set command)

| Flag | Type | Required | Description |
|---|---|---|---|
| `--enabled` | boolean | yes | `true` turns on automatic recharge, `false` turns off |
| `--threshold` | number | yes | Trigger recharge when the balance is lower than this value |
| `--credits` | number | yes | The number of credits for each recharge (the value must be supported by the platform) |
| `--monthly_max` | number | yes | Maximum monthly automatic recharge credits limit |

## Response (get and set return the same format)

```json
{
  "ok": true,
  "data": {
    "enabled": true,
    "threshold_credits": 100,
    "recharge_credits": 500,
    "monthly_max_recharge_credits": 2000
  }
}
```

| Field | Type | Description |
|---|---|---|
| `enabled` | boolean | Whether to enable automatic recharge |
| `threshold_credits` | number | The balance threshold that triggers recharge |
| `recharge_credits` | number | The number of credits automatically recharged each time |
| `monthly_max_recharge_credits` | number | Monthly automatic recharge limit |

## Usage Example

```bash
# View current settings
codia-design auto-recharge get

# Turn on automatic recharge: automatically buy 500 credits when the balance is < 100, with a monthly limit of 2000
codia-design auto-recharge set \
  --enabled true \
  --threshold 100 \
  --credits 500 \
  --monthly_max 2000

# Turn off automatic recharge
codia-design auto-recharge set \
  --enabled false \
  --threshold 0 \
  --credits 500 \
  --monthly_max 0
```

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | `recharge_credits` is not a recharge level supported by the platform | Use the face value of the credits package supported by the platform |

**Credit consumption**: 0 (management operations do not consume credits)
