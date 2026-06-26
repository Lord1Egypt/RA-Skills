---
name: backup-tool
description: "Backup and restore OpenClaw configuration, skills, memory, and workspace files. Essential for protecting your agent setup and enabling recovery after crashes or new installations."
metadata:
  {
    "version": "1.0.0",
    "openclaw": {
      "requires": { "bins": ["tar", "gzip", "git"] },
      "depends": ["sudo-tool"],
      "install": []
    },
    "license": "MIT",
    "homepage": "https://github.com/stigg86/backup-tool",
    "allowed-tools": ["exec", "read"]
  }
---

# Backup Tool 📦

**Backup and restore your OpenClaw setup.** Protect your skills, memory, identity, credentials, and workspace. One command to backup everything, easy restore when needed.

---

## Quick Start

```bash
# Check what will be backed up
python3 ~/.openclaw/backup-tool/backup_tool.py status

# Create backup
python3 ~/.openclaw/backup-tool/backup_tool.py backup

# Push backup to GitHub (requires repo setup)
python3 ~/.openclaw/backup-tool/backup_tool.py backup --push
```

---

## What Gets Backed Up

| Item | Path | Description |
|------|------|-------------|
| skills | `~/.openclaw/skills/` | All installed skills |
| workspace | `~/.openclaw/workspace/` | Memory, identity, config |
| memory | `~/.openclaw/workspace/memory/` | Daily memory files |
| identity | `~/.openclaw/identity/` | Agent identity |
| credentials | `~/.openclaw/credentials/` | API keys, tokens |
| vpn_mesh | `~/.openclaw/vpn-mesh/` | VPN mesh config |
| health_monitor | `~/.openclaw/health-monitor/` | Health monitor config |

---

## Commands

### `status` — Show backup status
Shows what files would be backed up, existing backups, and total backup size.

### `backup` — Create backup
Creates a timestamped `.tar.gz` archive in `~/.openclaw/backups/`.
Add `--push` to automatically push to GitHub.

### `list` — List backups
Shows all available local backups with timestamps and sizes.

### `restore` — Restore from backup
Restore specific items from a backup tarball:
```bash
python3 ~/.openclaw/backup-tool/backup_tool.py restore openclaw_backup_20240604.tar.gz
```

### `push` — Push to GitHub
Push the latest backup to a GitHub repository for off-site storage.

---

## GitHub Setup (Optional)

For cloud backups, create a GitHub repo called `openclaw-backup`:

1. Go to https://github.com/new
2. Name: `openclaw-backup`
3. Description: "OpenClaw agent backup repository"
4. Keep it private (contains credentials!)
5. Add your GitHub token to the skill or use `sudo-tool`

The backup tool will clone/push to this repo automatically.

---

## Recovery Scenarios

### New installation
```bash
# After fresh OpenClaw install
python3 ~/.openclaw/backup-tool/backup_tool.py restore openclaw_backup_latest.tar.gz
```

### Recovery after crash
```bash
# List backups
python3 ~/.openclaw/backup-tool/backup_tool.py list

# Restore everything
python3 ~/.openclaw/backup-tool/backup_tool.py restore openclaw_backup_20240604.tar.gz
```

### Move to new machine
```bash
# On new machine, install OpenClaw
# Then restore from GitHub
python3 ~/.openclaw/backup-tool/backup_tool.py push  # or pull from GitHub
```

---

## Automation

Add to cron for automatic daily backups:

```bash
# Daily backup at 3am
0 3 * * * python3 ~/.openclaw/backup-tool/backup_tool.py backup --push >> ~/.openclaw/backup-tool/backup.log 2>&1
```

---

## Files

```
~/.openclaw/backup-tool/
├── backup_tool.py   # Main script
├── backup.log        # Backup log
└── config.json       # Configuration (optional)

~/.openclaw/backups/
└── openclaw_backup_YYYYMMDD_HHMM.tar.gz
```

---

## Security Notes

- Credentials directory contains sensitive API keys — keep backups private
- GitHub repo should be **private** if storing credentials
- Backup files are stored locally with `chmod 755` restrictions
- Restore operation overwrites existing files (careful!)

---

## Required By

- **All skills** — protects your entire OpenClaw setup
- **Disaster recovery** — recover from crashes, new SD cards, or moves
- **Migration** — move setup to new Raspberry Pi

---

## Dependencies

- `sudo-tool` — for secure file operations
- `tar`, `gzip` — for archive creation
- `git` — for GitHub push (optional)