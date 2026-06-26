# schema

## Raw event fields
Recommended fields for each JSONL event:
- `ts`: ISO timestamp
- `actor`: executor identity
- `kind`: event type
- `target`: affected object
- `risk`: `low|medium|high`
- `privileged`: `true|false`
- `network`: `true|false`
- `summary`: short human-readable description
- `result`: `ok|warn|error`
- `refs`: optional structured references

## Common kinds
- `local_install`
- `config_change`
- `config_secret_injection`
- `system_update`
- `repo_create`
- `repo_visibility_change`
- `repo_history_rewrite`
- `external_publish`
- `export_safety_check`
- `session_maintenance`
- `auth_setup`
- `credential_followup`

## Principle
Prefer stable, reusable event names over highly specific one-off names.
