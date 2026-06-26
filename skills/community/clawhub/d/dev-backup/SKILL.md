---
name: "dev-backup"
description: "Snapshot progetti con retention, restore, list, checksum, e sicurezza migliorata"
---

# dev-backup

Snapshot the current state of a named project for safe rollback.

## Usage

Each project gets its own snapshot numbering. The project name is always the first argument.

```bash
# Backup any project
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$SCRIPT_DIR/dev-backup.sh" <project-name> --project-dir /path/to/your/project

# Example: backup a "my-app" project
bash "$SCRIPT_DIR/dev-backup.sh" my-app --project-dir /home/user/projects/my-app

# No --project-dir? Uses the current working directory
cd /home/user/projects/my-app
bash "$SCRIPT_DIR/dev-backup.sh" my-app
```

## Naming

Snapshots are named per project:

- **my-app-snapshot-1**, **my-app-snapshot-2**, …
- **another-project-snapshot-1**, **another-project-snapshot-2**, …

Each project tracks its own counter independently.

## Excluded from snapshot

- `.git`, `node_modules`, `.vite`, `.cache`, `*.log`, `.env`, `backups/`

## Restore

To restore a snapshot:

```bash
# Restore latest snapshot
bash "$SCRIPT_DIR/dev-backup.sh" my-app --restore --project-dir /path/to/your/project

# Restore specific snapshot
bash "$SCRIPT_DIR/dev-backup.sh" my-app --restore --snapshot 2 --project-dir /path/to/your/project
```

Or use the `.latest` symlink:

```bash
cp -r <backups-dir>/.latest/ <your-project-dir>/
```

## List

To list all snapshots for a project:

```bash
bash "$SCRIPT_DIR/dev-backup.sh" my-app --list
```

## Retention

By default, only the last 5 snapshots per project are kept. Customize with:

```bash
bash "$SCRIPT_DIR/dev-backup.sh" my-app --keep 10
```

## Verification

After backup, confirm:

```bash
ls -la <backups-dir>/
```

You should see the project-prefixed snapshot and `.latest` symlink.
