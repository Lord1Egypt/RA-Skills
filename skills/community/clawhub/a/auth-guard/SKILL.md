---
name: auth-guard
description: Standardize API credential handling and startup auth checks to prevent "missing key" regressions across sessions. Use when an agent repeatedly loses auth state, gets intermittent 401/403 errors after restarts, relies on ad-hoc curl calls, or needs a reusable auth-first pattern for HEARTBEAT.md/AGENTS.md and helper scripts.
---

# Auth Guard

Enforce a deterministic auth path: one credential source, one helper command path, one startup check, one fallback policy.

## Quick Workflow

1. Identify the target service endpoint and current failing flow.
2. Define canonical credential source (env var first, credentials file second).
3. Create/update a helper script in workspace (`.pi/`) that always injects auth.
4. Add a startup/auth-check command that verifies credentials and endpoint access.
5. Update HEARTBEAT.md or AGENTS.md to require helper usage (ban raw unauthenticated calls).
6. Add explicit fallback behavior for unauthorized states.

## Rules to Apply

- Prefer `ENV_VAR` override, then `~/.config/<service>/credentials.json`.
- Never embed secrets in logs, memory notes, or chat responses.
- Never call protected endpoints via raw curl if a helper exists.
- Keep fallback behavior explicit and low-noise.
- Store helper scripts in `workspace/.pi/` for easy reuse.

## Runtime Requirements

- `bash`
- `curl`
- `python3`

Check once before using this skill:

```bash
command -v bash curl python3 >/dev/null
```

## Safety Limits

- Pass only trusted credential paths under `~/.config/<service>/...` by default.
- Do not point `--cred-file` at arbitrary workspace files or unrelated secret stores.
- Keep probe URLs scoped to the target service auth endpoint.

## Startup Auth Check Pattern

Run at session start (or before heartbeat loops):

```bash
bash skills/auth-guard/scripts/auth_check.sh \
  --service moltbook \
  --url 'https://www.moltbook.com/api/v1/feed?sort=new&limit=1' \
  --env-var MOLTBOOK_API_KEY \
  --cred-file "$HOME/.config/moltbook/credentials.json"
```

Expected outcomes:
- `AUTH_OK` → proceed with normal authenticated helper flow.
- `AUTH_MISSING` or `AUTH_FAIL_*` → use defined fallback path and record one concise note.

## Reusable Snippets

Use drop-in policy snippets from:
- `references/snippets.md` (HEARTBEAT + AGENTS + helper policy blocks)

## References

- `references/contract.md` for the full Keychain Contract pattern
- `references/snippets.md` for ready-to-paste operational snippets
- `references/examples.md` for multi-service usage examples (Moltbook, GitHub, Slack)
