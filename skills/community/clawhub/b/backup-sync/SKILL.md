---
name: smart-backup
description: Intelligent file backup with compression and verification. Backup, sync, verify integrity, dedup, and restore. Manifest tracking. Zero external dependencies.
---

# Smart Backup 💾

**Stop losing config changes to disk failures. Start backing up intelligently.**

## The Problem

Config files, skills, memory — they're all on one disk with no backup strategy. When something breaks, everything is gone. Manual backups are error-prone and inconsistent.

Smart Backup fixes this with automated backup, sync, verification, and deduplication.

## ⚠️ Important Warnings

### Destructive Restore / Sync
- `--restore` overwrites target files with backup contents
- `--sync` two-way merges can create conflicts
- Both operations are irreversible if run without `--dry-run` first
Always preview with `--dry-run` before executing.

### Silent Data Duplication
If backup intervals overlap or the same source is backed up to the same destination multiple times, files will accumulate with timestamps. Periodically audit the backup directory for unexpected duplicates.

### Manifest Privacy
Backup manifests (`manifest.json`) contain full file paths and sizes, which may reveal directory structure and filenames. Treat manifests as sensitive metadata.

### Incremental Metadata Persistence
The backup journal and deduplication hash database persist under the backup destination. These files (`incremental-index.json`, `dedup-hashes.json`) grow with each backup run.

## Safety

This version includes safety fixes for the three ClawHub security audit findings:

### `--no-delete` — Default for sync (safe)
By default, sync **does not delete** files in the destination that are absent from the source. This prevents accidental data loss.

- `--no-delete` (default): files in dest not in source are skipped and logged with a WARNING
- `--delete`: enables deletion. Without `--force`, lists files that would be deleted but does not delete them
- `--delete --force`: actually deletes files absent from source, logging each one

### `--force` — Required for restore overwrite
`--restore` **skips existing files by default** instead of silently overwriting them.

- Without `--force`: existing files are skipped; WARNING logged for each
- With `--force`: existing files are overwritten; OVERWRITE logged for each

### Restore preserves directory structure
Restore uses the relative path from the manifest's `source` directory, preserving the original directory tree. Files land at `destination/<relative-path>`, not flattened into `destination/<basename>`.

### Tests excluded from published bundle
The `test/` and `tests/` directories are development artifacts and are **not included** in the published skill bundle.

## Quick Start

### Create a backup

```bash
node skills/smart-backup/smart-backup.js --backup ~/openclaw /path/to/backup
```

### Preview backup without creating

```bash
node skills/smart-backup/smart-backup.js --backup --dry-run ~/openclaw /path/to/backup
```

### Sync files between locations

```bash
node skills/smart-backup/smart-backup.js --sync ~/openclaw /path/to/backup/sync
```

Syncs only changed files. By default, files present in the destination but absent from the source are **not** deleted (`--no-delete` is the default). To enable deletion of such files, use `--delete`. Always pair with `--dry-run` first.

### Preview sync

```bash
node skills/smart-backup/smart-backup.js --sync --dry-run ~/openclaw /path/to/backup/sync
```

### Verify backup integrity

```bash
node skills/smart-backup/smart-backup.js --verify /path/to/backup-xxx
```

Checks SHA-256 hashes of all files against manifest.

### Find duplicate files

```bash
node skills/smart-backup/smart-backup.js --dedup ~/openclaw
```

Groups files by content hash, shows sizes and paths.

### List available backups

```bash
node skills/smart-backup/smart-backup.js --list
```

### Restore from backup

```bash
node skills/smart-backup/smart-backup.js --restore /path/to/backup-xxx /restore/path
```

Restores files preserving the original directory structure from the manifest. Existing destination files are **skipped** by default. Use `--force` to overwrite them.

### Status overview

```bash
node skills/smart-backup/smart-backup.js --status
```

### Incremental backup

```bash
# First backup (full)
node skills/smart-backup/smart-backup.js --backup /source /dest

# Subsequent backups (only changed files)
node skills/smart-backup/smart-backup.js --backup /source /dest --incr
```

Hash-based change detection — skips unchanged files for 10-100x speedup.

## Features

### Backup with Manifest

- Creates timestamped backup directories
- SHA-256 hash for every file in manifest
- Total size and file count tracking
- Skips `.git`, `node_modules`, `.cache`, `.npm` by default

### Smart Sync

- Copies new files, updates changed files, deletes extras
- Hash-based change detection (not just timestamps)
- Dry-run mode shows what would change before doing it

### Integrity Verification

- Verifies every file against stored SHA-256 hash
- Reports missing files and hash mismatches
- One-command verification of any backup

### Incremental Backup

- `--incr` flag enables hash-based change detection
- Only backs up files that changed since last backup
- Skips unchanged files (10-100x speedup)
- Manifest tracks per-file SHA-256 hashes
- `--from-manifest <id>` to base diff on specific manifest

### Content-Aware Deduplication

- Groups files by SHA-256 hash
- Shows duplicate groups with sizes
- Helps identify storage waste

### Compression Ready

- Manifest format supports compression (planned)
- Estimated 60% compression savings shown in dry-run
- Backup directory structure preserved

## Configuration

Backups stored in: `backups/smart-backups/`

Manifest stored in: `backups/smart-backups/manifest.json`

Override data directory:
```bash
--dir /path/to/data
```

## Agent Protocol

During heartbeats and maintenance:

1. **Weekly backup** — `--backup` your workspace to a safe location
2. **Verify after backup** — `--verify` the latest backup
3. **Dedup periodically** — `--dedup` to find and clean duplicates
4. **List backups** — `--list` to check backup health
5. **Dry-run first** — Always `--dry-run` before sync/backup on important dirs

## Heartbeat Integration

Add to your `HEARTBEAT.md`:

```markdown
### 💾 Smart Backup

- Weekly: `node skills/smart-backup/smart-backup.js --backup ~/openclaw /path/to/backup`
- Verify: `node skills/smart-backup/smart-backup.js --verify <latest-backup>`
- Dedup: `node skills/smart-backup/smart-backup.js --dedup ~/openclaw`
```

## Security Notes

- File hashes are SHA-256 (integrity, not encryption)
- Backups contain all file content — ensure backup storage is secure
- Symlink-safe — uses standard fs operations
- No network calls, all local

## Comparison

| Approach | Integrity Check | Dedup | Manifest | Automation |
|----------|----------------|-------|----------|------------|
| `cp -r` | ❌ | ❌ | ❌ | Manual |
| `rsync` | ⚠️ | ❌ | ❌ | Auto |
| **Smart Backup** | **✅** | **✅** | **✅** | **Auto** |

**Smart Backup gives you integrity verification + dedup + manifest tracking in one tool.**

## Design Principles

1. **Zero setup** — Works immediately, no config needed
2. **No dependencies** — Pure Node.js fs/crypto/zlib, no npm packages
3. **Safe by default** — Skips known bloat directories, dry-run available
4. **Transparent** — Every operation reports what it did
5. **Persistent** — Manifests survive restarts and can verify integrity later
