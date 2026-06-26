---
name: hermes-backup
description: "Multi-platform backup and restore for Hermes Agent and OpenClaw. Backs up configuration, memories, skills, sessions, and workspace. Features: optional encryption, optional cloud storage (S3/Google Drive), incremental or full backups, flexible retention, integrity verification, and web-based management UI. Free and open source."
version: 1.0.0
license: MIT-0
---

# Hermes Backup

Universal backup and restore for AI agent platforms. Works with **Hermes Agent** and **OpenClaw**.

## What Makes This Different

- **Multi-platform** — Works with both Hermes (`~/.hermes/`) and OpenClaw (`~/.openclaw/`)
- **Optional encryption** — Password-protect your backups (AES-256)
- **Optional cloud** — Set up S3, Google Drive, or Dropbox if you want off-site storage
- **Flexible backups** — Full or incremental, your choice
- **Smart retention** — Keep last N backups, or N days, or max N GB
- **Integrity checking** — Verify backups before trusting them
- **Web UI** — Browser-based management with progress bars

## Installation

```bash
# Via ClawMart (recommended)
clawmart install hermes-backup

# Or manual
git clone https://github.com/yourname/hermes-backup
chmod +x hermes-backup/scripts/*.sh
```

## Quick Start

```bash
# Create your first backup
hermes-backup create

# Or with the agent
"Create a backup of my agent"
```

## Commands

| Command | Description |
|---------|-------------|
| `hermes-backup create` | Create backup (full or incremental) |
| `hermes-backup restore <file>` | Restore from backup |
| `hermes-backup serve` | Start web UI |
| `hermes-backup config` | Interactive configuration |
| `hermes-backup cloud setup` | Configure cloud storage |
| `hermes-backup list` | Show all backups |
| `hermes-backup verify <file>` | Check backup integrity |
| `hermes-backup schedule` | Set up automatic backups |

## What Gets Backed Up

### Hermes Agent Structure
| Component | Path | Contents |
|-----------|------|----------|
| **Config** | `~/.hermes/config.yaml` | All settings, API keys |
| **Environment** | `~/.hermes/.env` | API keys, secrets |
| **Identity** | `~/.hermes/SOUL.md` | Agent personality |
| **Memory** | `~/.hermes/memories/` | Long-term memories |
| **Sessions** | `~/.hermes/sessions/` | Conversation history |
| **Skills** | `~/.hermes/skills/` | Installed skills |
| **State** | `~/.hermes/state.db` | Database |
| **Workspace** | `~/.openclaw/workspace/` | Cross-platform workspace |

### OpenClaw Structure
| Component | Path | Contents |
|-----------|------|----------|
| **Config** | `~/.openclaw/openclaw.json` | Gateway, models, channels |
| **Workspace** | `~/.openclaw/workspace/` | Agent files, skills |
| **Credentials** | `~/.openclaw/credentials/` | Channel pairing state |
| **Sessions** | `~/.openclaw/agents/main/sessions/` | Chat history |
| **Skills** | `~/.openclaw/skills/` | System skills |
| **Cron** | `~/.openclaw/cron/` | Scheduled jobs |

## Configuration

### Interactive Setup
```bash
hermes-backup config
```

This walks you through:
1. **Platform detection** — Hermes or OpenClaw (auto-detected)
2. **Backup location** — Where to save archives
3. **Encryption** — Enable password protection? (optional)
4. **Backup type** — Full or incremental?
5. **Retention** — How many backups to keep?
6. **Cloud** — Set up cloud storage? (optional)

### Config File (`~/.hermes-backup/config.yaml`)

```yaml
platform: auto  # auto, hermes, or openclaw

backup:
  location: ~/backups/hermes
  type: full  # full or incremental
  compression: gzip  # gzip, bzip2, or none
  encryption: false  # true/false
  
retention:
  strategy: count  # count, days, or size
  keep_count: 10   # keep last N backups
  keep_days: 30    # or keep for N days
  max_size_gb: 5   # or max total size

incremental:
  enabled: false
  base_backup: null  # reference full backup
  
cloud:
  enabled: false
  provider: null  # s3, gdrive, dropbox
  # Provider-specific settings added during setup
  
integrity:
  verify_after_backup: true
  checksum_algorithm: sha256
```

## Creating Backups

### Full Backup (Default)
```bash
hermes-backup create
# → ~/backups/hermes/hermes-backup_20260326_143022.tar.gz
```

### Incremental Backup
```bash
# First, create a base backup
hermes-backup create --full --tag base-2026-03-26

# Then incremental backups reference the base
hermes-backup create --incremental --base base-2026-03-26
```

### Encrypted Backup
```bash
hermes-backup create --encrypt
# Prompts for password (not echoed)
```

**⚠️ Warning:** If you lose the encryption password, the backup is unrecoverable. Store it in a password manager.

### With Cloud Upload
```bash
hermes-backup create --cloud-upload
# Creates backup locally, then uploads to configured cloud storage
```

## Restoring Backups

### Standard Restore
```bash
# Always dry-run first
hermes-backup restore ~/backups/hermes/hermes-backup_20260326_143022.tar.gz --dry-run

# If it looks good, apply
hermes-backup restore ~/backups/hermes/hermes-backup_20260326_143022.tar.gz
```

### Encrypted Restore
```bash
hermes-backup restore ~/backups/hermes/hermes-backup_20260326_143022.tar.gz.enc
# Prompts for password
```

### Selective Restore
```bash
# Restore only specific components
hermes-backup restore backup.tar.gz --components workspace,skills
```

## Cloud Storage Setup

### Amazon S3
```bash
hermes-backup cloud setup s3

# Prompts for:
# - AWS Access Key ID
# - AWS Secret Access Key  
# - Bucket name
# - Region (optional, defaults to us-east-1)
```

### Google Drive
```bash
hermes-backup cloud setup gdrive

# Opens browser for OAuth authentication
# Or provides manual token setup for headless
```

### Dropbox
```bash
hermes-backup cloud setup dropbox

# OAuth flow or manual token
```

### Testing Cloud Connection
```bash
hermes-backup cloud test
# Verifies credentials and uploads a test file
```

## Scheduling Automatic Backups

### Via Cron
```bash
hermes-backup schedule

# Interactive setup:
# - How often? (daily, weekly, hourly)
# - What time?
# - Full or incremental?
# - Cloud upload?
```

### Manual Cron Entry
```bash
# Add to crontab
0 3 * * * /usr/local/bin/hermes-backup create --quiet --cloud-upload
# Daily at 3am, quiet mode, upload to cloud
```

## Web UI

```bash
hermes-backup serve --port 7373 --token YOUR_TOKEN

# Opens browser UI at http://localhost:7373
# Features:
# - Create backups (click button)
# - Download backups
# - Upload and restore
# - View backup history
# - Configure settings
# - Progress bars for operations
```

## Integrity Verification

```bash
# Verify a specific backup
hermes-backup verify ~/backups/hermes/hermes-backup_20260326_143022.tar.gz

# Check all backups
hermes-backup verify --all

# Results:
# ✓ Backup is valid and restorable
# ✗ Backup is corrupted or incomplete
```

## Listing Backups

```bash
hermes-backup list

# Output:
# BACKUP NAME                           SIZE     DATE       TYPE   ENCRYPTED  CLOUD
# hermes-backup_20260326_143022.tar.gz  45MB     2026-03-26 full   no         yes
# hermes-backup_20260325_090015.tar.gz  2MB      2026-03-25 incr   yes        no
```

## Migration Between Platforms

### Hermes → OpenClaw
```bash
# On Hermes machine
hermes-backup create --platform hermes

# Transfer file to OpenClaw machine
scp backup.tar.gz user@newserver:~/

# On OpenClaw machine
hermes-backup restore backup.tar.gz --platform openclaw
```

### OpenClaw → Hermes
Same process, reverse direction.

## Security Considerations

### Backup Archive Contents
Backups contain **highly sensitive data**:
- API keys (OpenAI, Anthropic, ElevenLabs, etc.)
- Bot tokens (Telegram, Discord, etc.)
- Session data
- Personal memories/conversations

### Security Best Practices

1. **File Permissions**
   - Backups created with `chmod 600` (owner only)
   - Never `chmod 777` a backup

2. **Storage**
   - Keep local backups in encrypted disk/VeraCrypt
   - Cloud backups: use provider encryption at rest
   - Never commit backups to git

3. **Transmission**
   - Use scp/sftp, not email
   - Cloud uploads use HTTPS
   - Web UI uses token authentication

4. **Encryption Password**
   - Use a password manager (1Password, Bitwarden)
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - Never reuse passwords

5. **Rotation**
   - Old backups may contain old API keys
   - Rotate API keys periodically
   - Delete backups older than needed

## Troubleshooting

### "Permission denied" on backup
```bash
# Check directory permissions
ls -la ~/backups/hermes/

# Fix
chmod 700 ~/backups/hermes/
```

### "Backup is corrupted"
```bash
# Try to verify
hermes-backup verify backup.tar.gz

# If corrupted, check disk space
df -h

# Check for disk errors
fsck /dev/sda1  # (unmount first)
```

### "Cloud upload failed"
```bash
# Test connection
hermes-backup cloud test

# Check credentials
hermes-backup cloud status

# Re-configure if needed
hermes-backup cloud setup s3
```

### Restore fails halfway
```bash
# Auto-backup is created before restore
# Check /tmp/hermes-pre-restore-*.tar.gz

# Restore from auto-backup
hermes-backup restore /tmp/hermes-pre-restore_TIMESTAMP.tar.gz
```

## Scripts Reference

### `scripts/backup.sh`
Main backup script. Creates `.tar.gz` archive with MANIFEST.json.

### `scripts/restore.sh`
Restores from archive. Always dry-runs first. Creates pre-restore backup.

### `scripts/serve.sh`
Starts web UI server. Requires `--token` for security.

### `scripts/verify.sh`
Verifies backup integrity using checksums.

### `scripts/cloud-upload.sh`
Uploads backup to configured cloud storage.

### `scripts/config.sh`
Interactive configuration wizard.

## Version History

### v1.0.0
- Initial release
- Multi-platform support (Hermes + OpenClaw)
- Full and incremental backups
- Optional encryption (AES-256)
- Optional cloud storage (S3, Google Drive, Dropbox)
- Web UI for browser-based management
- Integrity verification
- Flexible retention policies
- Migration support between platforms

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.

---

**Built for the MyClaw.ai ecosystem** — the open AI personal assistant platform.
