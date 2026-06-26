---
name: ayao-updater
description: Automatically update OpenClaw and all installed skills on a schedule. Use when: (1) setting up automatic updates for OpenClaw or skills, (2) running a manual update check, (3) configuring update schedule, skip lists, or pre-release filtering, (4) user says "auto update", "schedule updates", "keep openclaw updated", "update skills automatically". Handles locally-modified skill protection, conflict avoidance, pre-release filtering, and completion or failure notifications.
---

# OpenClaw Auto Update

Keeps OpenClaw and installed ClawHub skills up to date automatically.

## Prerequisites

- `openclaw` CLI — required for `openclaw update`, `openclaw gateway restart`, and notifications
- `clawhub` CLI — required for `clawhub list`, `clawhub inspect`, and `clawhub update`
- `python3` — required for loading `config.json`
- `bash` 4+ — required by the shell scripts for associative arrays and other modern Bash features

## Quick Start

### 1. Install cron job (runs daily at 2 AM by default)

```bash
bash ~/.openclaw/workspace/skills/openclaw-auto-update/scripts/install-cron.sh
```

### 2. Run manually now

```bash
bash ~/.openclaw/workspace/skills/openclaw-auto-update/scripts/update.sh
```

### 3. Preview what would be updated (no changes)

```bash
bash ~/.openclaw/workspace/skills/openclaw-auto-update/scripts/update.sh --dry-run
```

## Configuration

Create `~/.openclaw/workspace/skills/openclaw-auto-update/config.json`:

```json
{
  "schedule": "0 2 * * *",
  "skipSkills": [],
  "skipPreRelease": true,
  "restartGateway": true,
  "notify": true,
  "notifyTarget": null
}
```

See `references/config-schema.md` for all options and examples.

## What It Does

1. **Loads JSON config** — reads `config.json` with `python3` and merges defaults
2. **Updates OpenClaw** — runs `openclaw update --yes --no-restart`; in preview mode it logs the equivalent `openclaw update --dry-run --yes --no-restart` command without making changes
3. **Finds installed skills** — enumerates skills via `clawhub list`, with workspace directory fallback
4. **Checks release channel** — uses `clawhub inspect <slug>` to skip pre-releases when `skipPreRelease: true`
5. **Updates skills** — runs `clawhub update <slug> --no-input` for each eligible installed skill; in preview mode it only logs `clawhub update --all` because the installed `clawhub` CLI does not support update dry runs
6. **Protects local changes** — skips skills with uncommitted git changes
7. **Respects skip list** — never touches skills in `skipSkills`
8. **Restarts gateway** — only if OpenClaw version actually changed
9. **Notifies** — sends `openclaw message send --target <target> -m <message>` when `notifyTarget` is set, otherwise `openclaw system event --text <message> --mode now`

## Change Schedule

```bash
# Change to 3 AM weekly on Sunday
bash ~/.openclaw/workspace/skills/openclaw-auto-update/scripts/install-cron.sh --schedule "0 3 * * 0"

# Uninstall cron job
bash ~/.openclaw/workspace/skills/openclaw-auto-update/scripts/install-cron.sh --uninstall
```

## Logs

```bash
tail -f /tmp/openclaw-auto-update.log
```

## Skip a Specific Skill Permanently

Add to `config.json`:
```json
{ "skipSkills": ["my-custom-skill", "work-internal"] }
```
