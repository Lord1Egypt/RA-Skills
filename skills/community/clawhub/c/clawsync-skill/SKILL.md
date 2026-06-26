---
name: clawsync-skill
description: |
  Backup and sync your entire OpenClaw configuration - skills, memory, settings, and history. One-click backup and restore for complete OpenClaw migration and disaster recovery.
  
  Keywords: backup tool, config sync, migration tool, OpenClaw backup, settings export, configuration manager, dotfiles sync, 备份工具, 配置同步, 迁移工具, 导出配置
  
  Use this skill when:
  - "Backup my OpenClaw setup"
  - "OpenClaw backup tool"
  - "I'm moving to a new computer"
  - "Move to new computer"
  - "Sync settings between devices"
  - "Export my skills and configuration"
  - "Export OpenClaw config"
  - "Restore from backup"
  - "What did I configure last month?"
  - "Archive my OpenClaw data"
  - "备份OpenClaw配置"
  - "迁移到新电脑"
  - "同步设置"
  
  One-click backup and restore for complete OpenClaw migration and disaster recovery. Supports encryption, multiple storage backends, and selective restore.
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# ClawSync - OpenClaw Configuration Sync

Never lose your OpenClaw setup again. One command to backup everything, one command to restore anywhere.

## When to Use

✅ **Use this skill when:**
- "Backup my OpenClaw setup"
- "I'm moving to a new computer"
- "Sync settings between devices"
- "Export my skills and configuration"
- "Restore from backup"
- "Archive my OpenClaw data"
- "Share my configuration with team"

❌ **Don't use when:**
- Real-time sync needed (use dedicated sync tools)
- Only backing up specific files (use cp/rsync)

## Features

### 1. Complete Backup
- **Skills** - All installed skills and configurations
- **Memory** - Agent memory, conversation history
- **Settings** - All `.openclaw` config files
- **Credentials** - Encrypted API keys and tokens
- **Workspace** - Projects and files
- **History** - Command and session history

### 2. Smart Restore
- **Selective restore** - Choose what to restore
- **Version control** - Keep multiple backup versions
- **Conflict resolution** - Handle existing files
- **Cross-platform** - Windows/macOS/Linux

### 3. Encryption & Security
- **Password encryption** - Protect sensitive data
- **GPG support** - Enterprise-grade encryption
- **Selective encryption** - Choose what to encrypt
- **Secure deletion** - Wipe temporary files

### 4. Storage Options
- **Local** - External drive, NAS
- **Cloud** - GitHub Gist, S3, Dropbox
- **Git** - Version controlled backups
- **Compressed** - ZIP with encryption

## Quick Start

### Create backup
```bash
# Full backup with encryption
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup --encrypt

# Quick backup (skills + settings only)
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup --quick

# Backup to specific location
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup --output ~/Backups/openclaw_backup.zip
```

### List backups
```bash
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py list
```

### Restore
```bash
# Interactive restore
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py restore

# Restore specific backup
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py restore --backup ~/Backups/openclaw_20260322_120000.zip

# Restore to new machine
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py restore --backup backup.zip --fresh-install
```

## Commands

### backup
Create a complete backup of OpenClaw configuration.

```bash
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup [options]

Options:
  --output PATH         Output file/directory (default: timestamped in ~/clawsync-backups)
  --encrypt            Encrypt backup with password
  --gpg                Use GPG encryption
  --include-history    Include full conversation history
  --include-workspace  Include workspace files (may be large)
  --exclude-skills     Don't backup skills (use clawhub to reinstall)
  --quick              Quick backup (settings + skills only)
  --compress LEVEL     Compression level 1-9 (default: 6)
```

### restore
Restore OpenClaw configuration from backup.

```bash
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py restore [options]

Options:
  --backup PATH        Backup file to restore from
  --selective          Choose what to restore
  --overwrite          Overwrite existing files
  --merge              Merge with existing configuration
  --fresh-install      Setup on new machine
  --dry-run            Preview changes
```

### list
List available backups.

```bash
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py list [options]

Options:
  --location PATH      Backup directory to scan
  --details            Show detailed info
```

### export
Export specific components.

```bash
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py export COMPONENT [options]

Components:
  skills               Export only skills
  memory               Export only memory
  settings             Export only settings
  credentials          Export credentials (encrypted)
```

## Backup Contents

### Structure
```
openclaw_backup_20260322_120000/
├── manifest.json           # Backup metadata
├── README.txt             # Restoration instructions
├── skills/                # All installed skills
│   ├── skill1/
│   ├── skill2/
│   └── ...
├── memory/                # Agent memory
│   ├── conversations/
│   ├── memory/
│   └── ...
├── settings/              # Configuration files
│   ├── config.yaml
│   ├── settings.json
│   └── ...
├── credentials/           # Encrypted credentials
│   └── credentials.enc
└── workspace/             # Workspace files (optional)
```

### What's Included
| Component | Default | Quick | Full |
|-----------|---------|-------|------|
| Skills | ✓ | ✓ | ✓ |
| Settings | ✓ | ✓ | ✓ |
| Memory | ✓ | ✗ | ✓ |
| Credentials | ✓ | ✓ | ✓ |
| History | ✗ | ✗ | ✓ |
| Workspace | ✗ | ✗ | ✓ |

## Examples

### Example 1: Pre-Migration Backup
```bash
# Before moving to new laptop
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup \
  --encrypt \
  --include-workspace \
  --output ~/migration_backup.zip
```

Output: Encrypted ZIP with everything needed to recreate setup.

### Example 2: Daily Auto-Backup
```bash
# Add to cron/job scheduler
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup --quick
```

Keeps last 7 days of quick backups automatically.

### Example 3: Team Configuration Sharing
```bash
# Export only skills (no credentials)
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py export skills \
  --output team_skills.zip

# Team members import
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py restore \
  --backup team_skills.zip \
  --selective skills
```

### Example 4: Disaster Recovery
```bash
# New machine, restore everything
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py restore \
  --backup openclaw_backup_20260322_120000.zip \
  --fresh-install

# Verify installation
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py verify
```

## Storage Locations

### Default Locations
- **Linux/macOS**: `~/clawsync-backups/`
- **Windows**: `%USERPROFILE%\clawsync-backups\`

### Cloud Integration

#### GitHub Gist
```bash
# Backup to private Gist
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup --github-gist

# Restore from Gist
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py restore --github-gist GIST_ID
```

#### S3
```bash
# Backup to S3
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup --s3-bucket my-backups
```

#### Git Repository
```bash
# Version-controlled backups
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup --git-repo ~/dotfiles
```

## Encryption

### Password Encryption
```bash
# Will prompt for password
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup --encrypt

# Or use environment variable
export CLAWSYNC_PASSWORD="secure_password"
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup --encrypt
```

### GPG Encryption
```bash
# Encrypt with specific GPG key
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup --gpg --gpg-key user@example.com
```

## Automation

### Cron Job (Linux/macOS)
```bash
# Daily backup at 2 AM
0 2 * * * /usr/bin/python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup --quick

# Weekly full backup
0 3 * * 0 /usr/bin/python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup
```

### Task Scheduler (Windows)
```powershell
# Create scheduled task
schtasks /create /tn "ClawSync Backup" /tr "pythonw.exe %USERPROFILE%\.openclaw\workspace\clawsync\scripts\clawsync.py backup --quick" /sc daily /st 02:00
```

## Safety Features

- ✅ **Dry-run mode** - Preview what will be backed up/restored
- ✅ **Incremental backups** - Only changed files
- ✅ **Rotation** - Keep N recent backups, delete old ones
- ✅ **Integrity check** - Verify backup integrity
- ✅ **Atomic operations** - All-or-nothing restore

## Configuration

Create `~/.clawsync/config.json`:

```json
{
  "backup_location": "~/Backups/OpenClaw",
  "retention": {
    "daily": 7,
    "weekly": 4,
    "monthly": 12
  },
  "encryption": {
    "enabled": true,
    "method": "password"
  },
  "exclude": [
    "*.log",
    "cache/",
    "tmp/"
  ],
  "auto_backup": {
    "enabled": true,
    "schedule": "0 2 * * *"
  }
}
```

## Requirements

- Python 3.8+
- 7z/p7zip (for compression)
- GPG (optional, for encryption)
- Git (optional, for version control)

## Installation

```bash
# Install dependencies
pip install -r ~/.openclaw/workspace/clawsync/requirements.txt

# Verify installation
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py --version
```

## Troubleshooting

### Large backups
Exclude workspace or use incremental backups:
```bash
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py backup --exclude workspace
```

### Permission errors
Ensure read access to `~/.openclaw` and write access to backup location.

### Corrupted backup
Verify integrity:
```bash
python3 ~/.openclaw/workspace/clawsync/scripts/clawsync.py verify --backup backup.zip
```

## Migration Guide

### From Old Computer
1. Run backup on old machine
2. Transfer backup file (USB, cloud, scp)
3. Install OpenClaw on new machine
4. Run restore

### To New Computer
1. Install OpenClaw
2. Install ClawSync skill
3. Restore from backup
4. Restart OpenClaw

## License

MIT License - See LICENSE file

## Support

For issues and feature requests, visit the GitHub repository.
