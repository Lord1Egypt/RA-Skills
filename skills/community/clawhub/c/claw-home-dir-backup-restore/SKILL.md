---
name: openclaw-backup-restore
description: >
  Backup or restore a complete OpenClaw installation (config, agents, flows, skills,
  credentials, memory, workspace, telegram bots) as a single portable .tar.gz archive.
  Use for backup: "backup my openclaw", "snapshot my openclaw setup".
  Use for restore: "restore openclaw", "migrate openclaw to this machine".
  On restore, any existing ~/.openclaw is automatically preserved with a timestamp before
  being replaced, so the previous state is never lost.
license: Apache-2.0
compatibility: macOS, Linux, Windows (Git Bash or WSL). Requires bash, tar, gzip. Optional: gpg for encrypted backups.
metadata:
  author: vbrunotech
  version: "1.0.0"
  category: devops
  domain: configuration-management
  openclaw:
    emoji: "🦞"
    requires:
      bins: ["bash", "tar", "gzip"]
    install:
      - id: brew-deps
        kind: brew
        formula: ["gnupg"]
        bins: ["gpg"]
        label: "Install gpg (optional, for encrypted backups)"
---

# OpenClaw Backup & Restore Skill

Snapshot and migrate your complete OpenClaw setup — config, agents, flows, skills, credentials,
memory, and workspace — as a single portable archive.

## What this skill does

- **Backup**: Archives the entire `~/.openclaw/` directory into a timestamped `.tar.gz`
  (or `.tar.gz.gpg` if encrypted) — no files excluded.
- **Restore**: Extracts an archive back into `~/.openclaw/`, preserving directory structure and
  permissions, so OpenClaw works immediately after extraction.
- **List**: Shows available backup archives in the configured output directory.
- **Verify**: Validates a backup archive's integrity before restore.

Use this skill when the user says:

- "backup my openclaw setup"
- "migrate openclaw to my new machine"
- "snapshot my openclaw config"
- "restore openclaw from backup"
- "what backups do I have?"

## What is backed up

The entire `~/.openclaw` directory — every file and subdirectory — is included in the archive.
No exclusions. The restored machine gets an exact copy of the original, and OpenClaw works
immediately without any missing configuration, credentials, skills, or state.

See `references/paths.md` for details on sensitive paths and restore-time permissions.

## Workflow

### Backup

1. Resolve the OpenClaw home directory (`OPENCLAW_HOME`, defaults to `~/.openclaw`).
2. Resolve the output directory (`BACKUP_DIR`, defaults to `~/openclaw-backups`).
3. Archive the full `~/.openclaw` directory into a timestamped `.tar.gz`.
4. Optionally encrypt with GPG: `--encrypt` flag or `BACKUP_GPG_RECIPIENT` env var.
5. Print the archive path and size.

### Restore

1. Validate the archive (non-empty, valid gzip, no path traversal).
2. Warn if `~/.openclaw` already exists and prompt for confirmation (or use `--force`).
3. Optionally decrypt if `.gpg` extension detected.
4. Extract to `~/.openclaw/` with `--strip-components=0`.
5. Fix permissions on sensitive files (`credentials/`, `secrets/`, `identity/`).
6. Print a summary of restored paths.

### List

Print all `.tar.gz` and `.tar.gz.gpg` files in `BACKUP_DIR` with size and date.

### Verify

Run `gzip -t` on the archive and list its top-level contents without extracting.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/backup.sh` | Create a backup archive |
| `scripts/restore.sh` | Restore from a backup archive |

## Usage examples

```bash
# Create a backup in ~/openclaw-backups/
bash scripts/backup.sh

# Backup to a custom directory
bash scripts/backup.sh --output /Volumes/USB/backups

# Backup with GPG encryption
bash scripts/backup.sh --encrypt you@example.com

# List available backups
bash scripts/backup.sh --list

# Verify a backup without restoring
bash scripts/restore.sh --verify openclaw-backup-2026-05-24_120000.tar.gz

# Restore (will prompt before overwriting)
bash scripts/restore.sh openclaw-backup-2026-05-24_120000.tar.gz

# Restore without confirmation prompt
bash scripts/restore.sh --force openclaw-backup-2026-05-24_120000.tar.gz

# Restore to a custom openclaw home
bash scripts/restore.sh --home /opt/openclaw openclaw-backup-2026-05-24_120000.tar.gz
```

## Migration workflow (old machine → new machine)

1. On the **old machine**: run `bash scripts/backup.sh` — copy the `.tar.gz` to the new machine.
2. On the **new machine**: install OpenClaw binary, then run `bash scripts/restore.sh <archive>`.
3. OpenClaw will start with your full config, agents, skills, credentials, and workspace intact.

## Security notes

- `credentials/` and `secrets/` contain sensitive API keys. Keep backups in a secure location.
- Use `--encrypt` with a GPG key for backups stored in cloud storage or on shared drives.
- The restore script sets `chmod 700` on sensitive directories automatically.

## Guardrails

- Never extract archives with path components that escape `~/.openclaw/` (path traversal check).
- Always show the archive size and file count after backup so the user can sanity-check completeness.
- If OpenClaw is running during backup, warn the user — SQLite databases may be in a dirty state.
- Do not backup `identity/device-auth.json` without informing the user it contains auth tokens.
