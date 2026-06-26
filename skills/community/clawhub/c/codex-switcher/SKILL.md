---
name: codex-switcher
description: Local OpenClaw skill for managing multiple OpenAI Codex accounts through auth snapshots. Use when the user wants to add a Codex account, switch between Codex accounts, inspect which Codex account is active, view remaining Codex quota, refresh expiring Codex tokens, or maintain a local multi-account Codex workflow without relying on third-party installers or bloating openclaw.json.
---

# Codex Switcher

Use this skill to manage **multiple local Codex accounts** on one OpenClaw host with a simple snapshot workflow.

Bundled executable:
- `scripts/cs.sh`

## What this skill is

This is a small local account manager for Codex on OpenClaw.

Core idea:
- keep OpenClaw's active Codex slot as `openai-codex:default`
- store each account as a separate snapshot under `~/.openclaw/auth-snapshots/`
- switch accounts by injecting snapshot credentials into `~/.openclaw/agents/main/agent/auth-profiles.json`
- inspect account identity and quota from the active token itself
- refresh snapshot tokens before expiry

This avoids filling `openclaw.json` with a growing roster of Codex aliases.

## Commands

### `cs list`
Show all saved snapshots with:
- alias
- decoded email
- remaining time before expiry

### `cs current`
Show the **real active account email**, not just the internal profile id.

### `cs quota`
Read the current active token and query remaining Codex usage quota.

### `cs switch <alias>`
Switch to a saved account snapshot by updating only the active Codex credentials in:
- `~/.openclaw/agents/main/agent/auth-profiles.json`

After switching, show:
- current active email
- current quota summary

### `cs add [alias]`
Start a new OAuth login flow for a brand-new account.

Workflow:
1. run `cs add` or `cs add <alias>`
2. sign in in browser
3. run `cs add --apply '<callback-url>' [alias]`
4. if alias was omitted, derive it from the email automatically
5. create a new snapshot file for that account

### `cs refresh <alias>`
Force-refresh one snapshot using its refresh token.

### `cs refresh-all`
Scan every snapshot and automatically refresh only those expiring within 24 hours.

This is intended for cron usage.

## Sensitive files

This skill touches high-sensitivity local auth material.
Main files involved:
- `~/.openclaw/agents/main/agent/auth-profiles.json`
- `~/.openclaw/auth-snapshots/*.json`
- `~/.openclaw/auth-snapshots/backups/*`
- temporary pending OAuth state files under `~/.openclaw/`

Treat all snapshot files as secrets.
Never expose full access tokens or refresh tokens in chat.

## Safety rules

- Do **not** run `curl | bash` installers.
- Do **not** fetch and execute third-party account-switch scripts blindly.
- Prefer local reviewed logic only.
- Back up auth material before risky operations.
- Validate alias names before writing files.
- Use atomic writes for snapshot and auth updates.
- Do not edit unrelated OpenClaw config unless truly required.
- Do not assume a snapshot alias is truthful; decode token email when verifying.

## Recommended workflow

### Add a new account
- `cs add` or `cs add <alias>`
- finish browser login
- `cs add --apply '<callback-url>' [alias]`
- `cs list`

### Switch accounts
- `cs switch <alias>`
- verify output shows the expected email and quota

### Keep snapshots fresh
Run `cs refresh-all` from cron once or twice per day.

## References

- For security concerns around third-party relogin installers, read `references/security-notes.md`.
- For local implementation notes, read `scripts/README-local-flow.md`.
