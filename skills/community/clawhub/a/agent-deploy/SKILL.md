---
name: agent-deploy
description: Deploy a new isolated OpenClaw agent with its own Telegram bot, workspace, and session storage. Use when user asks to create a new agent, add a new bot, or set up multi-agent routing. Uses openclaw config set for safe config updates with doctor validation and auto-rollback.
---

# Agent Deploy & Isolation Skill

## WHEN TO USE THIS SKILL

Use this skill when the user says ANY of the following (or similar):
- "deploy a new agent"
- "add a new agent"
- "create a new agent"
- "set up a new bot"
- "bind a bot to a new agent"
- "add a telegram bot"
- "list agents" or "show agents"
- "remove agent" or "delete agent"

## WHAT YOU NEED FROM THE USER

Before running any deploy script, you MUST collect these two values from the user:

| Required | Example | How to get it |
|----------|---------|---------------|
| **agentId** | `research` | Ask: "What should I name this agent?" (lowercase, no spaces, no special chars) |
| **botToken** | `123456:ABC-xyz` | Ask: "What is the Telegram Bot Token?" (user gets this from @BotFather) |

If the user provides both in their message, proceed immediately.
If the user is missing one or both, ask for the missing value(s) before proceeding.

## HOW TO EXECUTE

### Action: DEPLOY a new agent

Run this exact command, replacing `<agentId>` and `<botToken>` with the user's values:

```bash
bash {baseDir}/scripts/deploy.sh <agentId> <botToken>
```

**Example:** If user says "deploy agent called research with token 123456:ABCdef":
```bash
bash {baseDir}/scripts/deploy.sh research 123456:ABCdef
```

After the script finishes:
- If output contains "SUCCESS": tell the user the agent is deployed.
- If output contains "CONFLICT": tell the user the agent already exists.
- If output contains "ERROR": tell the user what went wrong.
- If output contains "ROLLING BACK": tell the user the change was safely reverted.

DO NOT run `systemctl restart` unless the script output explicitly says to.
The script handles hot-reload automatically for channels and bindings.

### Action: LIST all agents

```bash
bash {baseDir}/scripts/list.sh
```

Show the output table to the user as-is.

### Action: REMOVE an agent

Run this exact command, replacing `<agentId>`:

```bash
bash {baseDir}/scripts/remove.sh <agentId>
```

**Example:** If user says "remove the research agent":
```bash
bash {baseDir}/scripts/remove.sh research
```

## STRICT RULES ??DO NOT VIOLATE

1. **NEVER edit openclaw.json directly.** Do not use `write`, `edit`, `apply_patch`, or any file editing tool on `openclaw.json`. The deploy script uses `openclaw config set` which is the only safe way.
2. **NEVER skip the pre-flight check.** Always run the full deploy.sh script. Do not try to run individual `openclaw config set` commands yourself.
3. **NEVER change the agentId format.** It must be lowercase letters, numbers, and hyphens only. No spaces, no uppercase, no special characters.
4. **NEVER deploy without a valid bot token.** The token must match the format: `digits:alphanumeric` (e.g., `123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`).
5. **NEVER modify the main agent.** The `remove.sh` script refuses to remove the main agent. Do not try to work around this.

## WHAT THE SCRIPT DOES AUTOMATICALLY

You do NOT need to do any of these manually. The script handles everything:

- Creates isolated workspace at `~/.openclaw/workspace-<agentId>/`
- Adds agent to `agents.list` with safe defaults:
  - `tools.deny: ["gateway"]` (agent cannot modify core config)
  - `sandbox.mode: "non-main"` (non-main sessions are sandboxed)
  - `sandbox.scope: "agent"` (one container per agent)
  - `sandbox.workspaceAccess: "none"` (sandbox cannot access host workspace)
- Adds routing binding: `<agentId>` -> `telegram:<agentId>`
- Adds Telegram account with the bot token
- Validates with `openclaw doctor`
- Auto-rollbacks on any failure
- Merges API keys from BOTH global config (`openclaw.json` auth.profiles) AND main agent's auth-profiles.json
- Migrates from single-bot to multi-account mode if needed

## TROUBLESHOOTING

If the user says the new bot is not responding after deploy:

1. First, check logs: `journalctl --user -u openclaw-gateway --no-pager -n 20`
2. Look for `[telegram] [<agentId>] starting provider` in logs
3. If NOT found, restart: `systemctl --user restart openclaw-gateway`
4. If still not working, run: `bash {baseDir}/scripts/list.sh` to verify config

## ENVIRONMENT VARIABLES

These are optional. The scripts use sensible defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENCLAW_CONFIG_PATH` | `~/.openclaw/openclaw.json` | Custom config file path |
| `OPENCLAW_BIN` | `openclaw` | Custom openclaw CLI path |
