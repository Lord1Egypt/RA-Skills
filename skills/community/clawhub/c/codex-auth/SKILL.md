---
name: codex-auth
description: DEPRECATED shim skill for /codex_auth. Use codex-profiler instead; codex-auth is no longer the maintained path.
---

> ⚠️ **Deprecated:** `codex-auth` is no longer maintained as a standalone skill.
> Use **codex-profiler** for all ongoing `/codex_auth` and `/codex_usage` operations.

Run `scripts/codex_auth.py` to generate a login URL and apply callback URL tokens to `auth-profiles.json`.

## Safe defaults
- Treat callback URLs/tokens as sensitive and never echo full values.
- Use queued apply flow for controlled restart behavior.
- See `RISK.md` for allowed/denied operation boundaries.

## Commands
- `/codex_auth` → selector (discovered profiles)
- `/codex_auth <profile>`
- `/codex_auth finish <profile> <callback_url>`

## Interaction adapter
- If inline buttons are supported: show selector buttons.
- If inline buttons are not supported: send text fallback (`default | <profile>`).
- Callback message handling must never echo full callback URLs (treat as sensitive).
- Use callback_data namespace prefix `codex_auth_*` to avoid collisions.

## How to run
Start flow:

```bash
python3 skills/codex-auth/scripts/codex_auth.py start --profile default
```

Finish flow (after browser redirect URL is pasted):

```bash
python3 skills/codex-auth/scripts/codex_auth.py finish --profile default --callback-url "http://localhost:1455/auth/callback?code=...&state=..."
```

Queue safe apply (stops/restarts gateway in background):

```bash
python3 skills/codex-auth/scripts/codex_auth.py finish --profile default --callback-url "http://localhost:1455/auth/callback?code=...&state=..." --queue-apply
python3 skills/codex-auth/scripts/codex_auth.py status
```

## Safety posture
- No remote shell execution (`curl|bash`, `wget|sh`) is allowed by this skill.
- No `sudo`/SSH/system package mutation is performed by this skill.
- OAuth callback URLs are sensitive: never echo full callback URLs or tokens in chat output.
- Writes are limited to auth profile state files with lock-based coordination.

## Notes
- Uses the same OpenAI Codex OAuth constants/method as OpenClaw onboarding (`auth.openai.com` + localhost callback).
- OAuth success here does not guarantee `chatgpt.com/backend-api/wham/usage` acceptance; usage endpoint may reject token/session format with `401` and should be handled by usage/profiler skills.
- Endpoint trust boundary: OpenAI auth hosts + localhost callback flow only; do not send callbacks/tokens to third-party hosts.
- Writes `~/.openclaw/agents/main/agent/auth-profiles.json` with file locking to reduce race risk while gateway is running.
- Profile IDs map as:
  - `default` -> `openai-codex:default` (or first discovered codex profile if default missing)
  - any other selector -> `openai-codex:<selector>`
- Pending auth state is stored in `/tmp/openclaw/codex-auth-pending.json`.
