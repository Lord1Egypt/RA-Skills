---
name: openclaw-backup
description: >
  Encrypted backup and restore for OpenClaw agents. Two-tier archives:
  operational data safe for cloud storage, secrets encrypted with age for
  local recovery. Manifest verification with SHA-256 checksums. Atomic
  restore with staging, health checks, and auto-rollback. GitHub push with
  secrets protection. Daily scheduled backups. Use when setting up disaster
  recovery, backing up your agent, restoring from backup, or pushing
  archives to GitHub.
---

# 🔐 Agent Backup

One command to backup. One command to restore. Everything encrypted, verified, and rollback-safe.

## Quick Start

```bash
# Backup (operational only — safe for cloud)
bash {baseDir}/scripts/backup.sh

# Backup with encrypted secrets
bash {baseDir}/scripts/backup.sh --include-secrets --age-recipient age1...

# Verify
bash {baseDir}/scripts/verify.sh --manifest <path>/manifest.json --archive <path>/backup.tar.gz

# Restore (dry-run first)
bash {baseDir}/scripts/restore.sh --manifest <path>/manifest.json --archive <path>/backup.tar.gz --dry-run

# Restore for real
bash {baseDir}/scripts/restore.sh --manifest <path>/manifest.json --archive <path>/backup.tar.gz

# Push to GitHub (operational only, secrets blocked if unencrypted)
bash {baseDir}/scripts/push-to-github.sh --manifest <path>/manifest.json --archive <path>/backup.tar.gz

# Schedule daily 4 AM backups
bash {baseDir}/scripts/schedule.sh
```

## Two-Tier Archive Model

| Tier | Contents | Cloud safe? | Encrypted? |
|------|----------|-------------|------------|
| **Operational** | Workspace, redacted config, crons | ✅ Yes | No (no secrets) |
| **Secrets** | .env, agent auth profiles | ❌ Local only | ✅ Required (age) |

Default: operational only. Secrets are opt-in via `--include-secrets`.

## Restore Safety

Restore uses a 7-step safety flow:
1. Verify manifest checksums
2. Extract to staging (not live directory)
3. Verify critical files in staging
4. Backup current state to `.pre-restore-backup-TIMESTAMP`
5. Atomic swap
6. Health check (`pre-restart-check.sh` if available)
7. Auto-rollback on failure

Flags: `--dry-run` (preview only), `--force` (non-interactive)

## Prerequisites

- `age` for secrets encryption: `brew install age` or `apt install age`
- `gh` for GitHub push (optional): `brew install gh`

## Configuration

Set encryption via environment or flags:
```bash
# Environment
export AGE_RECIPIENT="age1your_public_key"
export AGE_PASSPHRASE_FILE="/path/to/passphrase"

# Or flags
bash {baseDir}/scripts/backup.sh --include-secrets --age-recipient age1...
```

## Workflows

- `bash {baseDir}/scripts/weekly-verify.sh` — verify all backup sets, prune by daily/weekly/monthly retention, and clean orphaned files.
- `bash {baseDir}/scripts/monthly-drill.sh` — run a dry-run restore against the newest backup set and report pass/fail.
- `bash {baseDir}/scripts/pre-change-snapshot.sh` — create a fast operational-only snapshot before config edits or gateway restarts.
- `.github/workflows/verify-backup.yml` — GitHub Actions CI that builds a fixture backup, validates manifest checksums, extracts the archive, and checks critical files.

## Reference Files

- `{baseDir}/references/restore-guide.md` — full disaster recovery walkthrough
- `{baseDir}/references/what-to-backup.md` — every file explained
- `{baseDir}/references/retention-policy.md` — how long to keep backups
