# Risk Rules

## Levels

- `low`: read-only or tightly scoped commands with no obvious secret or rollback concern
- `medium`: writes are limited in scope and reversible, but still deserve a quick review
- `high`: destructive, privileged, or production-impacting commands that require confirmation
- `critical`: broad destructive targets, inline active credentials, or download-and-execute patterns

## Broad Targets

Treat these as broad targets when the command can delete, move, or overwrite data:

- `.`
- `..`
- `/`
- `\`
- drive roots such as `C:\`
- wildcard-only targets such as `*`, `.\*`, `*.*`
- the workspace or repo root itself

## Approval Guidance

- `low`: approval usually not required
- `medium`: approval depends on user intent and whether a safer rewrite is available
- `high`: require explicit approval before execution
- `critical`: stop automatic execution and narrow the operation first

## Secret Exposure

Treat these as at least `high` risk:

- `Authorization: Bearer ...`
- JWTs beginning with `eyJ`
- AWS access keys such as `AKIA...`
- GitHub PATs such as `ghp_...`
- OpenAI-style keys such as `sk-...`
- query parameters or flags like `token=`, `api_key=`, `password=`, `secret=`
- inline cookie headers or pasted `.env` values

Inline active credentials should be treated as `critical` unless they are clearly redacted.
