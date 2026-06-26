---
name: codex-profile-orchestrator
description: deterministic openclaw codex profile failover for windows workspaces with duplicate detection, workspace variant aliases, quota-aware profile choice, telegram session sync, network outage protection, and install helpers. use when chatgpt needs to stabilize or rebuild multi-account codex switching, inspect auth-profiles.json, select the healthiest account, or package a safer replacement for fragile profile rotation logic.
---

# Codex Profile Orchestrator

Use this skill to manage multiple Codex OAuth profiles without a fuzzy AI loop.

## Core resources

- `scripts/codex_profile_orchestrator.py` contains the full orchestrator, reporting, and self-test flow.
- `scripts/install_codex_profile_orchestrator.py` writes a Windows-friendly config and starter script into an OpenClaw workspace.
- `references/state-model.md` explains how identities, variants, duplicates, and invalid streaks are tracked.

## Recommended workflow

1. Install the config into the target workspace.
2. Run a dry run first and inspect the JSON payload.
3. Apply once.
4. Start daemon mode only after the dry run looks correct.

## Rules

- Treat internet or ChatGPT reachability failures as transport incidents, not as broken accounts.
- Quarantine only 401, 403, 400, missing-token, or clearly expired-token profiles.
- Keep weekly availability as a hard gate. Keep five-hour remaining as the primary tie-breaker for switching.
- Detect same email plus same user plus same account as a duplicate.
- Detect same email plus same user plus different account as a workspace variant and register it as `ws2`, `ws3`, and so on.
- Sync Telegram and other OpenClaw session overrides to the selected profile.
