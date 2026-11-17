# Smart Backup & Sync

Intelligent file backup with gzip compression, incremental backups, verification, and deduplication.

## Features

- **Full Backups** — Create timestamped, compressed backups with manifest tracking
- **Incremental Backups** — Only back up changed files since last manifest
- **File Sync** — Sync files between directories with dry-run support
- **Backup Verification** — Verify backup integrity (hash comparison)
- **Restore** — Restore backups to a destination directory
- **Deduplication** — Find duplicate files by content hash
- **Status Overview** — View backup stats and storage health
- **Compression** — Built-in gzip compression for backup files

## Installation

```bash
# The skill is auto-loaded by OpenClaw via the skill registry.
# For standalone use:
const SB = require('./smart-backup.js');
```

## Commands

```
--backup <source> <destination>           Create full backup
--backup --dry-run <source> <dest>        Preview backup
--sync <source> <destination>             Sync files between locations
--sync --dry-run <source> <dest>          Preview sync
--verify <backup_file>                    Verify backup integrity
--dedup <dir>                             Content-aware deduplication
--list                                     List available backups
--restore <backup_file> <destination>     Restore from backup
--status                                   Backup status overview
```

## API

### `createBackup(source, destination, dryRun = false)`
Create a timestamped gzip-compressed backup of source directory.

```javascript
SB.createBackup('/home/user/projects', '/backups', false);
```

### `createIncrementalBackup(source, destination, fromManifest, dryRun)`
Only back up files that changed since the last manifest.

```javascript
SB.createIncrementalBackup('/home/user/projects', '/backups');
```

### `syncFiles(source, destination, dryRun)`
Synchronize files from source to destination.

```javascript
SB.syncFiles('/home/user/projects', '/backups/mirror');
```

### `verifyBackup(backupFile)`
Verify backup integrity by comparing file hashes.

```javascript
SB.verifyBackup('/backups/backup-2026-07-18-123456789');
```

### `listBackups()`
List all available timestamped backups.

### `restoreBackup(backupFile, destination)`
Restore a backup to the specified destination.

```javascript
SB.restoreBackup('/backups/backup-2026-07-18-123456789', '/home/user/restored');
```

### `findDuplicates()`
Find and report duplicate files by content hash.

### `getFileHash(filepath)`
Get SHA-256 hash of a file. Returns null for missing files.

### `formatBytes(bytes)`
Format byte count as human-readable string (`1 KB`, `2.5 MB`).

### `collectFiles(dir, skipDirs)`
Recursively collect files in a directory, skipping common non-essential dirs.

### `showStatus()`
Print backup system status (total backups, size, directory).

## Security

- File hashes computed using SHA-256
- Backup files stored with manifest for integrity verification
- No external dependencies — pure Node.js crypto + zlib
- Dry-run mode for safe preview before executing

## Testing

```bash
node tests/run-self-tests.js
```

### Test Coverage

| Suite | Tests | Status |
|---|---|---|
| Self-tests (isolated) | 19 | ✅ Passing |
