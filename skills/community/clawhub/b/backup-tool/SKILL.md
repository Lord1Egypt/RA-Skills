---
name: backup-tool
description: Backup and restore files with compression and encryption. Use when user needs to backup important files, create scheduled backups, sync folders, encrypt sensitive backups, or restore from backup archives.
---

# Backup Tool

Backup and restore files with compression and encryption.

## Quick Start

```bash
# Backup a folder
python scripts/backup.py /path/to/folder --output backup.tar.gz

# Restore
python scripts/backup.py --restore backup.tar.gz --destination /restored
```

## Usage

```bash
python scripts/backup.py SOURCE [OPTIONS]

Options:
  --output PATH       Output backup file
  --compress FORMAT   Compression: gzip, bzip2, xz (default: gzip)
  --encrypt           Encrypt backup with password
  --restore PATH      Restore from backup
  --destination DIR   Restore destination
  --incremental      Create incremental backup
  --exclude PATTERN  Exclude pattern (can repeat)
```

## Examples

```bash
# Simple backup
python scripts/backup.py ~/Documents --output docs-backup.tar.gz

# Encrypted backup
python scripts/backup.py ~/Important --output secure-backup.tar.gz --encrypt

# Incremental backup
python scripts/backup.py /data --output incremental --incremental

# Restore encrypted backup
python scripts/backup.py --restore secure-backup.tar.gz --destination /restored
```

## Scheduling Backups

Add to crontab for automatic backups:
```
0 2 * * * python /path/to/backup.py /home --output /backup/daily.tar.gz
```

## Features

- Compression: gzip, bzip2, xz
- AES-256 encryption
- Incremental backups
- Exclude patterns
- Integrity verification
