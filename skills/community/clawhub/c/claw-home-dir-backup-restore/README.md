# openclaw-backup

Backup and restore your complete OpenClaw setup — config, agents, flows, skills, credentials,
memory, and workspace — as a single portable archive.

Drop the archive on any machine, run `restore.sh`, and OpenClaw is ready to use.

## Structure

```
openclaw-backup/
├── SKILL.md                  — skill instructions for the agent
├── README.md                 — this file
├── references/
│   └── paths.md              — what is included / excluded and why
└── scripts/
    ├── backup.sh             — create a backup archive
    └── restore.sh            — restore from a backup archive
```

## Quick start

```bash
# Backup (saves to ~/openclaw-backups/ by default)
bash scripts/backup.sh

# List available backups
bash scripts/backup.sh --list

# Verify an archive before restoring
bash scripts/restore.sh --verify openclaw-backup-2026-05-24_120000.tar.gz

# Restore
bash scripts/restore.sh openclaw-backup-2026-05-24_120000.tar.gz
```

## Migration to a new machine

1. **Old machine** — create the backup:
   ```bash
   bash scripts/backup.sh --output /tmp
   ```

2. **Copy** the `.tar.gz` to the new machine (USB, cloud, SCP, etc.)

3. **New machine** — install OpenClaw, then restore:
   ```bash
   bash scripts/restore.sh openclaw-backup-2026-05-24_120000.tar.gz
   ```

4. Start OpenClaw — your full config, agents, flows, and credentials are ready.

## Options

### backup.sh

| Flag | Description |
|---|---|
| `--output DIR` | Save archive to a custom directory |
| `--encrypt EMAIL` | GPG-encrypt the archive (requires `gpg`) |
| `--list` | List archives in the backup directory |

### restore.sh

| Flag | Description |
|---|---|
| `--home DIR` | Restore to a custom OpenClaw home (default: `~/.openclaw`) |
| `--force` | Skip confirmation prompts |
| `--verify` | Verify archive integrity without restoring |

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `OPENCLAW_HOME` | `~/.openclaw` | OpenClaw config directory |
| `BACKUP_DIR` | `~/openclaw-backups` | Where backups are stored |
| `BACKUP_GPG_RECIPIENT` | _(none)_ | GPG recipient for encrypted backups |

## What is backed up

Everything needed for a working OpenClaw: config, identity, credentials, secrets, plugins,
skills, agents, flows, cron jobs, memory, workspace, telegram bots, and shell completions.

Excluded: temp files, cache, logs, delivery queues, and transient runtime state that would
be stale on a new machine. See `references/paths.md` for the full list.
