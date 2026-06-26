# 🔐 Agent Backup — Disaster Recovery for OpenClaw

Your agent forgets nothing — but your hard drive can. This skill creates encrypted, verifiable backups of your entire OpenClaw installation with one command.

## Why This Exists

Without this skill, a dead Mac Studio means:
- ✅ **5 minutes** to restore workspace (daily backup covers this)
- ❌ **Hours** to recreate 43 cron definitions from memory
- ❌ **Hours** to rebuild 11 agent configs, channel settings, provider auth
- ❌ **Hunting** through dashboards to re-gather 8+ API keys

With this skill: **one command to backup, one command to restore.** Everything.

## What Gets Backed Up

| Archive | Contents | Where it goes |
|---------|----------|---------------|
| **Operational** `openclaw-backup-*.tar.gz` | Workspace (SOUL, MEMORY, scripts, skills, memory), config (redacted), crons | Local + Google Drive + GitHub ✅ |
| **Secrets** `openclaw-secrets-*.tar.gz.age` | .env (API keys), agent auth profiles (OAuth tokens) | 🔒 Local only, encrypted with `age` |
| **Manifest** `manifest.json` | Checksums, versions, file list, timestamps | Alongside both archives |

**Secrets never touch cloud storage unencrypted.** The push-to-github script hard-refuses if it detects unencrypted secrets.

## Quick Start

```bash
# Basic backup (operational only — safe for cloud)
bash scripts/backup.sh

# Full backup including encrypted secrets
bash scripts/backup.sh --include-secrets --age-recipient age1your_public_key_here

# Verify a backup
bash scripts/verify.sh --manifest path/to/manifest.json --archive path/to/backup.tar.gz

# Dry-run a restore (shows what would happen, changes nothing)
bash scripts/restore.sh --manifest path/to/manifest.json --archive path/to/backup.tar.gz --dry-run

# Real restore
bash scripts/restore.sh --manifest path/to/manifest.json --archive path/to/backup.tar.gz

# Push to private GitHub repo
bash scripts/push-to-github.sh --manifest path/to/manifest.json --archive path/to/backup.tar.gz

# Schedule daily 4 AM backups
bash scripts/schedule.sh
```

## How Restore Works (Safety First)

Restore doesn't just dump files — it uses a 7-step safety flow:

```
1. Verify checksums from manifest
2. Extract to staging directory (not live)
3. Verify critical files exist in staging
4. Backup current state → .pre-restore-backup-TIMESTAMP
5. Atomic swap: staging → live
6. Health check (pre-restart-check.sh)
7. Auto-rollback if health check fails
```

**If anything goes wrong, your previous state is preserved automatically.**

## Setup

### Prerequisites
- `age` — for secrets encryption: `brew install age` (macOS) or `apt install age` (Linux)
- `gh` — for GitHub push: `brew install gh` (optional)

### Generate your encryption key (one time)
```bash
age-keygen -o ~/.config/age/keys.txt
# Save the public key (age1...) — used for encryption
# Save keys.txt somewhere safe — needed for decryption
```

### Schedule daily backups
```bash
bash scripts/schedule.sh
```
This creates (or replaces) an OpenClaw cron job that runs at 4 AM daily.

## Workflows

### `weekly-verify.sh`
Runs a full weekly hygiene pass across `~/.openclaw/backups/`:
- verifies every backup set with a `manifest.json`
- reports total / OK / failed / missing-manifest counts
- prunes expired backup runs using the 14 daily / 8 weekly / 6 monthly retention policy
- removes orphaned manifests and orphaned encrypted secrets files
- prints a short Telegram-friendly summary for cron delivery

```bash
bash scripts/weekly-verify.sh
```

### `monthly-drill.sh`
Runs a monthly restore rehearsal against the newest valid backup set:
- finds the latest run with a manifest + operational archive
- executes `restore.sh --dry-run`
- checks for an explicit dry-run pass signal
- verifies any secrets archive is still encrypted as `.age`
- prints `Restore drill PASSED ✅` or `Restore drill FAILED 🔴 — ...`

```bash
bash scripts/monthly-drill.sh
```

### `pre-change-snapshot.sh`
Creates a fast operational-only snapshot before config edits or gateway restarts:
- skips secrets, GitHub push, and cloud concerns
- renames the archive to `openclaw-snapshot-pre-change-TIMESTAMP.tar.gz`
- keeps only the newest 5 snapshot runs
- outputs the snapshot path so you have a rollback reference

```bash
bash scripts/pre-change-snapshot.sh
```

### GitHub Actions: `verify-backup.yml`
On every push, CI now:
- generates a fixture backup from a temporary OpenClaw home
- validates manifest checksum metadata
- extracts the operational archive
- verifies critical files exist in the archive

## Scheduling with OpenClaw cron

Example system events for recurring workflow checks:

### Weekly verify — Sundays at 3 AM
```bash
openclaw cron create \
  --name "OpenClaw Weekly Backup Verify" \
  --cron "0 3 * * 0" \
  --system-event "Run bash '$HOME/.openclaw/workspace/skills/openclaw-backup/scripts/weekly-verify.sh' and return the output exactly."
```

### Monthly drill — 1st of month at 3 AM
```bash
openclaw cron create \
  --name "OpenClaw Monthly Restore Drill" \
  --cron "0 3 1 * *" \
  --system-event "Run bash '$HOME/.openclaw/workspace/skills/openclaw-backup/scripts/monthly-drill.sh' and return the output exactly."
```

## Disaster Recovery Scenarios

### 🔴 Mac died / disk failure
1. Get a new Mac, install OpenClaw: `npm i -g openclaw && openclaw onboard`
2. Download latest backup from Google Drive or clone from GitHub
3. `bash scripts/restore.sh --manifest ... --archive ... --secrets ... --age-identity ~/.config/age/keys.txt`
4. `openclaw gateway restart`
5. Reinstall Ollama models: `brew install ollama && ollama pull nomic-embed-text`

### 🟡 Config corruption (bad edit, env var removed)
1. Find the last good backup: `ls ~/.openclaw/backups/`
2. Partial restore — config only:
```bash
TMP=$(mktemp -d)
tar -xzf path/to/backup.tar.gz -C "$TMP"
cp "$TMP/openclaw/openclaw.json" ~/.openclaw/openclaw.json
openclaw gateway restart
```

### 🟢 Accidental file deletion
1. Check git first: `cd ~/.openclaw/workspace && git log --oneline -5`
2. Restore specific file: `git checkout HEAD~1 -- MEMORY.md`
3. If not in git, extract from backup:
```bash
TMP=$(mktemp -d)
tar -xzf path/to/backup.tar.gz -C "$TMP"
cp "$TMP/openclaw/workspace/MEMORY.md" ~/.openclaw/workspace/MEMORY.md
```

## Security Model

| Principle | Implementation |
|-----------|---------------|
| **Secrets never in cloud unencrypted** | `age` encryption required, push-to-github refuses plaintext |
| **Config redacted before packaging** | Token/key/secret fields stripped from openclaw.json |
| **Restore is non-destructive by default** | Staging → swap → rollback. Previous state always preserved |
| **Dry-run before real restore** | `--dry-run` shows exactly what would change |
| **Manifest verification** | SHA-256 checksums validated before any restore |
| **Non-interactive safety** | Refuses destructive restore without TTY unless `--force` |

## File Reference

```
scripts/
├── backup.sh               Create operational + encrypted secrets archives
├── weekly-verify.sh        Verify all runs, prune retention, clean orphans
├── monthly-drill.sh        Dry-run restore drill against the newest backup
├── pre-change-snapshot.sh  Fast operational-only rollback snapshot
├── restore.sh              Staged restore with validation and rollback
├── verify.sh               Manifest + checksum validation
├── push-to-github.sh       GitHub private repo push (secrets-protected)
└── schedule.sh             Create/replace daily 4 AM backup cron

.github/workflows/
└── verify-backup.yml       CI check for generated backup archives

references/
├── restore-guide.md        Detailed disaster recovery walkthrough
├── what-to-backup.md       Every file explained — what matters and why
└── retention-policy.md     How long to keep backups, pruning rules
```

## Built By

[Don Zurbrick](https://github.com/zurbrick) — battle-tested on a production OpenClaw agent with 11 agents, 43 crons, and 6 model providers. Council-reviewed by 5 AI models across 4 providers before publishing.

## License

MIT
