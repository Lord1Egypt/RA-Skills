---
name: backup-openclaw-config
description: Backup and restore OpenClaw configuration files. Use when backing up OpenClaw settings before upgrades, transferring configuration to another machine, restoring from a previous backup, or preparing for system maintenance.
---

# Backup OpenClaw Configuration

## Overview

This skill provides automated backup and restore functionality for all OpenClaw configuration files. It creates timestamped archives containing your complete OpenClaw setup, including main configuration, workspace, skills, and user data.

**What gets backed up:**
- `~/.openclaw/` - Main configuration
- `~/.config/openclaw/` - System-level configuration
- `~/.local/share/openclaw/` - Local data
- `~/.openclaw/workspace/` - Workspace, skills, and memory

## Quick Start

### Backup Your Configuration

Run the backup script:

```bash
~/.openclaw/workspace/skills/backup-openclaw-config/scripts/backup_openclaw.sh [output-directory]
```

**Example:**
```bash
# Backup to default location ($HOME/backups/openclaw)
~/.openclaw/workspace/skills/backup-openclaw-config/scripts/backup_openclaw.sh

# Backup to custom location
~/.openclaw/workspace/skills/backup-openclaw-config/scripts/backup_openclaw.sh ~/my-backups
```

**Output:**
- Creates `openclaw_backup_YYYYMMDD_HHMMSS.tar.gz` archive
- Creates `openclaw_backup_YYYYMMDD_HHMMSS.info` metadata file
- Shows backup summary with file list and archive size
- **Automatically deletes backups older than 15 days** to manage disk space

### Restore from Backup

Run the restore script:

```bash
~/.openclaw/workspace/skills/backup-openclaw-config/scripts/restore_openclaw.sh <backup-archive.tar.gz>
```

**Example:**
```bash
~/.openclaw/workspace/skills/backup-openclaw-config/scripts/restore_openclaw.sh \
  ~/backups/openclaw/openclaw_backup_20260306_095000.tar.gz
```

**Process:**
1. Shows backup information from .info file
2. Lists all files that will be restored
3. Requires confirmation before proceeding
4. Backs up existing files with .bak extension
5. Restores configuration to original locations

**After restore:**
```bash
# Restart OpenClaw Gateway to apply changes
systemctl --user restart openclaw-gateway
```

## Workflow

### Backup Workflow

1. **Check prerequisites**
   - Verify backup directory exists or can be created
   - Check if OpenClaw directories exist

2. **Create backup structure**
   - Generate timestamp for unique backup name
   - Create temporary directory for staging

3. **Copy configuration files**
   - Backup `~/.openclaw/` (main config)
   - Backup `~/.config/openclaw/` (system config)
   - Backup `~/.local/share/openclaw/` (local data)
   - Skip directories that don't exist (with warning)

4. **Create archive**
   - Compress all files into `.tar.gz` archive
   - Create `.info` file with metadata (timestamp, hostname, user, size)

5. **Report results**
   - Show archive location and size
   - Display restore command
   - Warn if any directories were missing

### Restore Workflow

1. **Validate backup**
   - Check if archive file exists
   - Display backup information from .info file
   - List contents of archive

2. **Safety confirmation**
   - Show warning about overwriting current config
   - List all files that will be restored
   - Require explicit "yes" confirmation

3. **Backup existing files**
   - Rename existing directories to `.bak`
   - Preserve current configuration before overwriting

4. **Extract and restore**
   - Extract archive to temporary directory
   - Move files to original locations
   - Restore `~/.openclaw/`, `~/.config/openclaw/`, `~/.local/share/openclaw/`

5. **Complete and notify**
   - Show restore completion message
   - Display restart command for Gateway
   - Note that .bak files were created

## Use Cases

### Before Upgrade

```bash
# Backup before updating OpenClaw
~/.openclaw/workspace/skills/backup-openclaw-config/scripts/backup_openclaw.sh

# Then upgrade
openclaw update
```

### Transfer to New Machine

```bash
# On old machine: create backup
~/.openclaw/workspace/skills/backup-openclaw-config/scripts/backup_openclaw.sh

# Transfer backup archive to new machine (scp, rsync, etc.)
scp ~/backups/openclaw/openclaw_backup_*.tar.gz user@new-machine:~/

# On new machine: restore
~/.openclaw/workspace/skills/backup-openclaw-config/scripts/restore_openclaw.sh \
  ~/backups/openclaw/openclaw_backup_*.tar.gz
```

### Disaster Recovery

```bash
# Restore from backup after system failure
~/.openclaw/workspace/skills/backup-openclaw-config/scripts/restore_openclaw.sh \
  /path/to/backup/openclaw_backup_20260306.tar.gz

# Restart services
systemctl --user restart openclaw-gateway
```

## Configuration Locations

For detailed information about what gets backed up, see [config-locations.md](references/config-locations.md).

**Summary:**
- **Main config:** `~/.openclaw/` - Gateway config, extensions, tokens
- **Workspace:** `~/.openclaw/workspace/` - Skills, memory, user data
- **System config:** `~/.config/openclaw/` - systemd services, preferences
- **Local data:** `~/.local/share/openclaw/` - Cache, runtime data

## Best Practices

### Regular Backups

Create backups regularly, especially after:
- Installing new skills
- Modifying configuration
- Adding extensions
- Important workspace changes

### Secure Storage

- Backup archives contain sensitive data (tokens, credentials)
- Store backups in secure location
- Consider encrypting with gpg for sensitive environments
- Don't share backup archives publicly

### Testing Backups

After creating a backup, verify it:
```bash
# Test extraction to temporary location
tar -tzf backup.tar.gz | head

# Verify critical files are present
tar -tzf backup.tar.gz | grep -E "(config.json|AGENTS.md|MEMORY.md)"
```

## Troubleshooting

### Permission Denied

If you see permission errors:
```bash
# Ensure scripts are executable
chmod +x ~/.openclaw/workspace/skills/backup-openclaw-config/scripts/*.sh

# Ensure backup directory is writable
mkdir -p ~/backups/openclaw
chmod 755 ~/backups/openclaw
```

### Gateway Won't Start After Restore

If Gateway fails to start after restore:
```bash
# Check Gateway logs
journalctl --user -u openclaw-gateway -n 50

# Restore from .bak if needed
mv ~/.openclaw ~/.openclaw.bad
mv ~/.openclaw.bak ~/.openclaw

systemctl --user restart openclaw-gateway
```

### Missing Directories

The backup script gracefully handles missing directories:
- Skips directories that don't exist
- Shows warning for each missing directory
- Still creates valid backup with available data
