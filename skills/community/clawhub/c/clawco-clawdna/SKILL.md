---
slug: clawco-clawdna
name: "ClawDNA -- Identity Backup & Sync"
version: "1.0.0"
tags: [backup, sync, identity, version-control]
license: MIT-0
min_openclaw: "2026.1"
source: "https://github.com/clawco-io/clawdna/tree/main/packages/skill"
homepage: "https://github.com/clawco-io/clawdna#readme"
repository: "https://github.com/clawco-io/clawdna.git"
env:
  CLAWDNA_HUB_TOKEN:
    description: "Authentication token for ClawDNA Hub sync operations (push/pull/clone)"
    required: false
---

# ClawDNA -- Identity Backup & Sync

You have the ClawDNA skill installed. ClawDNA is a CLI tool that versions and syncs your identity files (SOUL.md, AGENTS.md, IDENTITY.md, MEMORY.md, TOOLS.md, USER.md) so they never drift or get lost. Your job is to proactively help the user protect their agent identity using ClawDNA commands.

---

## When to Act

### Suggest a snapshot before risky changes

Before any of the following, suggest running `clawdna snapshot`:

- Upgrading the OpenClaw runtime or any major dependency
- Editing SOUL.md, AGENTS.md, or IDENTITY.md (core personality files)
- Installing or removing skills/plugins that modify TOOLS.md
- Changing channel configurations or workspace structure
- Running `clawdna memory distill` for the first time

Example prompt to the user:

> This change could affect your identity files. Want me to run `clawdna snapshot --name "before-<change>"` first so you can roll back if needed?

### Warn when the last push is stale

If the user mentions syncing, backups, or switching machines -- or if you have reason to believe the last `clawdna push` was more than 24 hours ago -- remind them:

> It's been a while since your last push. Run `clawdna push` to sync your latest identity to the hub, or `clawdna diff` to see what's changed.

### Detect identity drift

If you notice that identity files (SOUL.md, MEMORY.md, etc.) have been edited directly without a subsequent snapshot or push, flag it:

> Your identity files have changed since the last snapshot. Run `clawdna diff --local` to review the changes, then `clawdna push` to sync.

### Guide recovery

If the user mentions lost settings, a broken agent, or setting up a new machine, guide them through recovery:

1. **New machine:** `clawdna clone --agent-id <id>` to pull the full identity from hub
2. **Rollback:** `clawdna restore --bundle <path>` to revert to a previous snapshot
3. **Diagnose:** `clawdna doctor` to check installation health and hub connectivity

---

## CLI Command Reference

### Core Commands

| Command | What it does |
|---------|-------------|
| `clawdna init` | Interactive setup -- detects your workspace and configures the hub (Cloud, Git, or local) |
| `clawdna snapshot [--name <name>]` | Creates a timestamped `.dna` bundle of all identity files |
| `clawdna restore --bundle <path> [--dry-run]` | Restores identity from a `.dna` bundle; use `--dry-run` to preview |
| `clawdna diff [--local \| --hub]` | Shows changes between local identity and hub, or since last sync |
| `clawdna log` | Displays identity change history with timestamps |

### Sync Commands

| Command | What it does |
|---------|-------------|
| `clawdna push [--message <msg>]` | Pushes current identity to the configured hub |
| `clawdna pull [--dry-run]` | Pulls latest identity from hub; shows diff before applying |
| `clawdna clone --agent-id <id>` | Bootstraps a new machine by downloading identity from hub |
| `clawdna fleet [--env-ids <ids...>]` | Pushes identity to multiple environments simultaneously |

### Management Commands

| Command | What it does |
|---------|-------------|
| `clawdna env add\|list\|switch` | Manages environment profiles (per-machine tokens and overrides) |
| `clawdna memory distill [--dry-run]` | Uses an LLM to extract key facts from session memory into core identity |
| `clawdna memory show` | Displays the current contents of MEMORY.md |
| `clawdna daemon start\|stop\|status` | Background sync daemon -- watches for changes and auto-pushes |
| `clawdna doctor` | Health check -- verifies config, permissions, hub connectivity, and OpenClaw state |
| `clawdna upgrade [--channel <ch>]` | Safe OpenClaw upgrade -- snapshots before, verifies identity after, offers rollback |

---

## What Gets Backed Up

ClawDNA manages these identity files from your OpenClaw workspace:

| File | Purpose |
|------|---------|
| `SOUL.md` | Personality, values, and behavioral rules |
| `AGENTS.md` | Workspace conventions and operating rules |
| `IDENTITY.md` | How the agent presents itself |
| `MEMORY.md` | Accumulated knowledge about the user |
| `TOOLS.md` | Installed skills and tool configurations |
| `USER.md` | User-specific context and preferences |
| `openclaw.json` | Runtime configuration (secrets are stripped automatically) |

### What is NOT backed up (secrets protection)

ClawDNA's sanitizer runs as a hard gate before every push, snapshot, and export. It blocks the operation if it detects:

- API keys (OpenAI, Anthropic, etc.)
- Bot tokens (Telegram, Discord)
- JWTs and bearer tokens
- Private key headers
- Any pattern matching user-defined rules in `~/.clawdna/.secretsignore`

Inline secrets in `openclaw.json` are automatically replaced with `$ENV_VAR_NAME` references. The operation aborts if secrets are found in any markdown identity file.

---

## Troubleshooting

### "Secrets detected" error

The sanitizer found a secret in your identity files. This is intentional -- secrets must never leave your machine.

**Fix:** Remove the secret from the flagged file and use an environment variable reference instead. Run the command again after cleaning.

If this is a false positive, you can add an exception pattern to `~/.clawdna/.secretsignore`.

### Hub unreachable

`clawdna push` or `clawdna pull` can't connect to the hub.

**Diagnose:** Run `clawdna doctor` -- it checks hub connectivity and authentication.

**Common causes:**
- Missing or expired hub token (check `CLAWDNA_HUB_TOKEN` env var or run `clawdna env switch`)
- Network issues or firewall blocking the hub URL
- Hub URL misconfigured (check `~/.clawdna/config.json`)

### Conflict on pull (diverged state)

Both local and hub have changes since the last sync.

**Fix:** `clawdna pull` will show the diff and prompt you to choose: hub wins, local wins, or cancel. Review the diff carefully before deciding. You can always `clawdna snapshot` first to save your current state.

### Identity changed after upgrade

`clawdna upgrade` detected that core identity files were modified by the OpenClaw update.

**Fix:** The upgrade command offers an automatic rollback. If you declined, you can still run:
```
clawdna restore --bundle ~/.clawdna/snapshots/pre-upgrade-<version>.dna
```

### Doctor reports permission warnings

Config files should be `600` (owner read/write only) and snapshot directories should be `700`.

**Fix:** Run `chmod 600 ~/.clawdna/config.json` and `chmod 700 ~/.clawdna/snapshots/`.
