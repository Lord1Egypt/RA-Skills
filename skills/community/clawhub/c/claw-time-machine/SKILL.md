---
name: claw-time-machine
description: "Backup, restore, and migrate OpenClaw installations. Preserve workspace memories, credentials, custom skills, scheduled tasks, and core configuration. Use when the user wants to back up OpenClaw, restore from a backup, migrate to another machine or server, inspect or count existing backups, or mentions backup, restore, migration, 时光机, 迁移, 备份, 恢复."
---

# Claw Time Machine

Back up, restore, and migrate the important state of an OpenClaw installation.

## Run the script

Use the bundled script:

```bash
./scripts/ctm.sh <command> [args]
```

Commands:

- `backup [filename]` — create a backup under `~/.ctm/`
- `list` — show backups, newest first
- `restore <index|filename|latest> [--force]` — restore a backup
- `migrate <user@host> [--remote-dir <dir>] [--clean-remote-archive] [--force]` — copy a backup to another machine and restore it there

## What the script preserves

The script backs up only the important OpenClaw state, not the full installation binaries:

- `workspace/`
- `credentials/`
- `telegram/`
- `skills/`
- `cron/`
- `openclaw.json`
- `identity/`

Each archive also includes a `manifest.txt` file that lists the captured paths.

## Core workflow

### Create a backup

Before a risky change, server migration, or major upgrade:

```bash
./scripts/ctm.sh backup
```

If the user asks how many backups exist or wants to inspect them:

```bash
./scripts/ctm.sh list
```

Report the count, filenames, sizes, and highlight the newest backup.

### Restore a backup

Prefer listing backups first when the user is choosing by index:

```bash
./scripts/ctm.sh list
./scripts/ctm.sh restore 1
```

Use `latest` when the intent is obvious:

```bash
./scripts/ctm.sh restore latest
```

Add `--force` only when non-interactive restore is clearly intended.

### Migrate to another machine

Use the migration command when the user wants a full move to a new server:

```bash
./scripts/ctm.sh migrate user@new-server
```

The script creates a fresh backup, copies it to the target host, and restores it there without requiring the skill to already exist on the target machine.

If the user wants the copied archive removed from the target machine after a successful restore, add `--clean-remote-archive`.

## Important safety rules

1. Treat restore as destructive: it overwrites the preserved state paths.
2. Keep the automatic safety backup path shown by the script so rollback remains possible.
3. This skill does not stop or start Gateway automatically.
4. If the target environment is unusual, read `references/usage.md` before doing a migration.

## Additional guidance

For detailed examples, migration notes, and failure handling, read `references/usage.md`.
