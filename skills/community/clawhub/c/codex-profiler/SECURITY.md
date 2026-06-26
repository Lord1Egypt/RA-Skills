# Security Notes

This consolidated skill bundles `codex_usage.py` and `codex_auth.py`.

## Scope
- Read-only usage checks (`codex_usage.py`).
- OAuth profile refresh/setup (`codex_auth.py`).

## Data Handling
- Sensitive fields are not emitted in output.
- Usage output applies scrub rules for token-like keys.
- Never echo full callback URLs in responses.

## Network Egress
- Usage checks call trusted ChatGPT usage endpoint.
- OAuth flow uses OpenAI auth endpoints.

## Operational Safety
- Auth queued apply mode may restart gateway.
- Revert command + backups are provided before restart-capable operations.
