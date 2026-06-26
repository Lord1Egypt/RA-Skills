# SKILL.md - OpenClaw Backup

Backup and restore your OpenClaw agent (workspace + config).

## When to Use

- User wants to create a backup of their agent
- User wants to move to a new computer
- User asks how to preserve their agent's memory/identity
- Important memories or updates happened — time to save!

## What Gets Backed Up

1. **Workspace** — `~/.openclaw/workspace/` (agent memory, identity, files)
2. **OpenClaw Config** — `~/.openclaw/` (settings, sessions, agents)

## Commands

### Create Backup (Manual)

```bash
cd ~/.openclaw/workspace
./skills/openclaw-backup/openclaw-backup.sh create
```

Creates: `~/openclaw-backups/openclaw-backup-YYYY-MM-DD_HHMMSS.tar.gz`

Keeps last 10 backups automatically.

### Auto-Backup Setup

```bash
./skills/openclaw-backup/openclaw-backup.sh setup-auto
```

Creates a hook at `~/.openclaw/workspace/.hooks/post-memory-save.sh`

Call it manually when important memories are saved:
```bash
~/.openclaw/workspace/.hooks/post-memory-save.sh
```

Or add daily backups via crontab:
```bash
crontab -e
# Add: 0 2 * * * ~/.openclaw/workspace/skills/openclaw-backup/openclaw-backup.sh create
```

### List Backups

```bash
./skills/openclaw-backup/openclaw-backup.sh list
```

### Restore from Backup

```bash
./skills/openclaw-backup/openclaw-backup.sh restore ~/Downloads/openclaw-backup-2026-03-09.tar.gz
```

## Moving to a New Computer

### 1. On OLD computer:
```bash
cd ~/.openclaw/workspace
./skills/openclaw-backup/openclaw-backup.sh create
ls ~/openclaw-backups/
```

### 2. Copy the `.tar.gz` file to new computer
- USB drive, cloud sync, email, Discord... whatever works
- Put it in your Downloads folder or anywhere you can find

### 3. On NEW computer:

**If OpenClaw is already installed:**
```bash
tar -xzf ~/Downloads/openclaw-backup-2026-03-09.tar.gz -C ~
openclaw gateway start
```

**If OpenClaw is NOT installed:**
```bash
# 1. Install OpenClaw (see docs)
# 2. Then restore:
tar -xzf ~/Downloads/openclaw-backup-2026-03-09.tar.gz -C ~
openclaw gateway start
```

### 4. Done!
Open http://127.0.0.1:18789/ — your agent is back! 🎉

## Requirements

- Linux/WSL2 (tested on Ubuntu/WSL2)
- tar (pre-installed on most systems)
- ~1-2MB per backup (excludes logs and temp files)

## Notes

- Excludes logs, temp files, node_modules, .git to keep backup small
- Tested on WSL2 / Linux systems
