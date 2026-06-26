# Security Notes

## Scope
- OAuth start/finish for OpenAI Codex profile auth.
- Optional queued apply mode may stop/start gateway to avoid runtime reconciliation races.

## Data Handling
- Reads/writes local auth profile state.
- Never prints full token values.
- Never echo full callback URLs in responses.
- Stores pending OAuth verifier/state in `/tmp/openclaw/codex-auth-pending.json`.

## Network Egress
- OpenAI OAuth authorize/token endpoints only.

## Operational Safety
- Before restart-capable operations, emits a revert command with file backups.
- Uses backups under `/tmp/openclaw/safety-backups`.
- Uses file lock + atomic writes for auth profile updates.
