# asana skill for OpenClaw

A lightweight OpenClaw Asana skill with **PAT-first** auth and optional OAuth support.

## Recommended auth

Use a Personal Access Token (PAT).

Supported auth order:
1. `ASANA_PAT` env var
2. `~/.openclaw/asana/config.json`
3. OAuth token files under `~/.openclaw/asana/`

## Quick start

```bash
node scripts/configure.mjs --mode pat --pat "$ASANA_PAT"
node scripts/asana_api.mjs list-workspaces
```

## Optional OAuth

```bash
node scripts/configure.mjs --mode oauth --client-id "$ASANA_CLIENT_ID" --client-secret "$ASANA_CLIENT_SECRET"
node scripts/oauth_oob.mjs auth-url
node scripts/oauth_oob.mjs token --code "..."
```

## Storage

- `~/.openclaw/asana/config.json`
- `~/.openclaw/asana/credentials.json`
- `~/.openclaw/asana/token.json`
