# Local Flow Sketch

Use this flow when implementing the local Codex multi-account manager.

## Snapshot model

- Keep OpenClaw's active Codex slot as `openai-codex:default`
- Store each account as one minimal snapshot under `~/.openclaw/auth-snapshots/`
- Snapshot files should contain only:
  - `access`
  - `refresh`
  - `expires`
  - `accountId`
- Switch accounts by injecting snapshot credentials into `auth-profiles.json`

## Main flows

### Add account
1. Generate PKCE verifier + challenge
2. Build OAuth authorize URL using official OpenAI endpoint
3. Store only minimal pending OAuth state locally
4. Accept callback URL/code from user
5. Exchange code for tokens with official OpenAI token endpoint
6. Save minimal credentials as a new snapshot file

### Switch account
1. Read target snapshot
2. Update only the active Codex credentials in `~/.openclaw/agents/main/agent/auth-profiles.json`
3. Keep unrelated profiles/config untouched
4. Re-read current email and quota to verify switch success

### Refresh snapshots
1. Read snapshot `expires`
2. Skip snapshots not close to expiry
3. Use snapshot `refresh` token to get a new access token
4. Write refreshed credentials back into the same snapshot file

## Never do

- `curl | bash`
- hidden proxy fallback
- writing unrelated config
- bloating `openclaw.json` with a growing Codex roster
- printing full tokens
- surprise restarts
