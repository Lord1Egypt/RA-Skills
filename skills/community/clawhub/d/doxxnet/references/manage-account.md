# Manage doxx.net Account

> **Live schema first.** The doxx.net Config API is agent-descriptive. Fetch `https://config.doxx.net/` for the current manifest (every endpoint, params, returns, auth, side effects): this file is a snapshot. Every POST response also includes a `context` field with per-endpoint docs.

You help users manage their doxx.net account settings, recovery options, and subscription.


## API convention

**Auth token -- never enters the AI conversation.**

The token is passed to `curl` via shell expansion, so its plaintext value stays on your machine. Two sources, checked in this order:

1. `$DOXXNET_TOKEN` env var (preferred): user exports it before launching the agent.
2. `~/.config/doxxnet/token` file: used automatically if the env var is unset.

curl commands below use `${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}`, so both work transparently. The shell expands the value at exec time -- the plaintext is never emitted in a tool call to the LLM.

**Config API**: POST to `https://config.doxx.net/v1/`:
```
curl -s -X POST https://config.doxx.net/v1/ -d "ENDPOINT=1&param=value&token=${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}"
```

## Endpoints

- `get_profile`: get account profile. Returns: recovery_email, recovery_phone, email_notifications, sms_notifications, recovery_codes_count
- `update_profile`: update settings. Params: any of `recovery_email`, `recovery_phone`, `notifications`
- `create_account_recovery`: generate new recovery codes. Returns: `codes[]`
- `verify_account_recovery`: verify recovery code (for account recovery flow). Returns: `new_token`
- `subscription_status`: check subscription. Returns: has_active_subscription, tier, subscription (original_transaction_id, product_id, tier, effective_tier, status, purchase_date, expires_date, is_trial, auto_renew), pro_features map
- For token management (create/revoke tokens, set expiry, geo/IP fences, tunnel scoping): see the `manage-tokens` skill

## Guidelines

- Always show current profile before making changes (call get_profile first)
- When generating recovery codes, strongly warn user to save them securely
- Remind users that doxx.net has no passwords: the token IS identity, recovery codes are the backup
- Never display recovery codes in a way that could be accidentally shared
- When showing subscription, explain what the current tier includes
- For account recovery flow, explain that verify_account_recovery issues a new token and the old one is invalidated
- Always check API response `status` field -- HTTP 200 can still be an error
