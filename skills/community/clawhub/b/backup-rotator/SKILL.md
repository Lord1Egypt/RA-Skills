---
name: backup-rotator
description: "Smart backup rotation and retention manager. Create backups, enforce flexible retention policies (grandfather-father-son), verify integrity, and clean up old backups automatically. Use when the user wants to: (1) Create timestamped backups of files or directories, (2) Set up automated backup rotation with retention policies, (3) Keep N daily / M weekly / K monthly backups, (4) Clean up old backup files automatically, (5) Verify backup file integrity with SHA256 checksums, (6) Schedule backup rotation via cron, (7) Audit existing backups in a directory."
---

# Backup Rotator

Create, rotate, and verify backups with configurable retention policies. Uses only Python standard library — no pip install needed.

## Quick start

```bash
# Create a backup
python3 skills/backup-rotator/scripts/backup_rotator.py --backup /path/to/source /path/to/backups

# Create backup with compress
python3 skills/backup-rotator/scripts/backup_rotator.py --backup /path/to/dir /backups --compress

# List existing backups
python3 skills/backup-rotator/scripts/backup_rotator.py --list /backups --name myproject

# Rotate (clean old backups)
python3 skills/backup-rotator/scripts/backup_rotator.py --rotate /backups --name myproject

# Dry run (see what would be deleted)
python3 skills/backup-rotator/scripts/backup_rotator.py --rotate /backups --name myproject --dry-run

# Verify backup integrity
python3 skills/backup-rotator/scripts/backup_rotator.py --verify /backups
```

## Retention Policy (default)

| Category | Keep | Description |
|----------|------|-------------|
| Daily | 7 | Most recent daily backups |
| Weekly | 4 | Most recent Sunday backups |
| Monthly | 3 | First 7 days of each month |
| Old | 0 | Beyond all retention → deleted |

Default policy keeps **14 backups** minimum.

## Config File (for cron)

Create a JSON config file for fully automated backup + rotation:

```json
{
  "backup_source": "/var/lib/postgresql/database.dump",
  "backup_dest": "/backups/db",
  "backup_name": "postgres",
  "keep_daily": 7,
  "keep_weekly": 4,
  "keep_monthly": 3,
  "compress": true,
  "verify": true
}
```

Then run:

```bash
python3 skills/backup-rotator/scripts/backup_rotator.py --cron config.json
```

Output:
```
  Backup Rotator — 2026-05-10 13:30:00
  ==================================================
  Name prefix:       postgres
  Keep daily:        7
  Keep weekly:       4
  Keep monthly:      3
  Compress:          yes
  Verify:            yes

  📦 Creating backup...
  Compressing /var/lib/postgresql/database.dump → /backups/db/postgres_20260510-133000.tar.gz
  Size:    42.3M
  SHA256:  a1b2c3d4e5f6...

  🔄 Rotating old backups...
  Summary: 12 keep, 3 delete
  Keeping:
    ✅ postgres_20260510-133000.tar.gz (42.3M) - keep (daily)
    ✅ postgres_20260509-020000.tar.gz (41.8M) - keep (daily)
    ...
  Deleting:
    🗑  postgres_20260428-020000.tar.gz (40.1M) - delete (past retention)

  ✅ Verifying remaining backups...
  ✅ postgres_20260510-133000.tar.gz SHA256: a1b2...
  ✅ postgres_20260509-020000.tar.gz SHA256: b2c3...
```

## Common commands

| Command | Action |
|---------|--------|
| `--backup SOURCE DEST` | Create timestamped backup |
| `--list DIR` | List all backups with age and category |
| `--rotate DIR` | Apply retention policy, delete old backups |
| `--dry-run` | Preview rotation without deleting |
| `--verify DIR` | Check SHA256 checksums of all backups |
| `--cron config.json` | Full automated run: backup + rotate + verify |
| `--name PREFIX` | Filter backup files by name prefix |
| `--compress` | Compress directory backups to tar.gz |
| `--no-verify` | Skip SHA256 verification |

## Automation with Cron

Add to crontab for daily automated backups:

```cron
# Daily at 2am
0 2 * * * cd /home/user && python3 skills/backup-rotator/scripts/backup_rotator.py --cron /home/user/configs/backup-postgres.json >> /var/log/backup-rotator.log 2>&1
```

## Requirements

- **Python 3.6+** (no pip install needed)
- Uses only standard library: `os`, `shutil`, `hashlib`, `json`, `argparse`
- Works on Linux, macOS (partial)
- No external API calls — fully offline
