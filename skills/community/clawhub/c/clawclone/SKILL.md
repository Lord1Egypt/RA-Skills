---
name: clawclone
description: "Backup, clone, and migrate OpenClaw data across instances. Upload/download OpenClaw snapshots to local or cloud - https://clawclone.cc . Create shareable Agent configurations, sync between devices, and restore complete OpenClaw state including memory, skills, agents, and settings. Use when user wants to backup their OpenClaw data, share configurations, migrate to new server, or create snapshots."
metadata:
  openclaw:
    requires:
      bins: ["node", "tar", "npm"]
    trust: high
    permissions:
      - read: ~/.openclaw/
      - write: ~/.openclaw/
      - network: https
---

# ClawClone

Backup, clone, store, and migrate your OpenClaw workspace configurations.

## Install

If the environment does not have the clawclone skill, use `clawhub install clawclone` to install it.

## What Gets Backed Up

| Component | Details |
|---|---|
| OpenClaw Data | MEMORY.md, skills, agent files, configurations |
| Settings | Agent preferences and custom settings |
| Files | User data and OpenClaw artifacts |
| Config | Optional: API keys and tokens (if configured) |

**Backup Location**: `~/.openclaw/backup`

## Dependencies

Requires: `node` (v16+), `tar`, `npm` (all standard on OpenClaw instances).

Check: `which node tar npm`

## Prerequisites

**Before using cloud features**, verify the environment variable is set:

```bash
# Check if CLAWCLONE_API_KEY is set
echo $CLAWCLONE_API_KEY
```

If empty or not set, ask the user to get their ClawClone API key at https://clawclone.cc/dashboard/settings, and export:

```bash
export CLAWCLONE_API_KEY="your_api_key"
```

**Note**: Local operations work without API key.

## Commands

### Push to Cloud

```bash
# Push local workspace to cloud
node clawclone.mjs push --name "My Agent" --description "Production config"

# List all cloud backups
node clawclone.mjs list

# Show backup details
node clawclone.mjs show <clone-id>

# Delete a cloud backup
node clawclone.mjs delete <clone-id> --yes
```

### Clone from Backup

```bash
# Clone (download and restore)
node clawclone.mjs clone <clone-id>

# Preview changes first (recommended)
node clawclone.mjs clone <clone-id> --test
```

**Test mode** generates a detailed report showing:
- Backup metadata (name, version, creation date)
- Components that will be modified (workspace, config, skills, etc.)
- File counts and sizes for each component
- No actual changes are made to your system

### Local Operations

```bash
# Export to local file (no upload)
node clawclone.mjs local export --name "Local Backup" --output ./backup.tar.gz

# Import from local file
node clawclone.mjs local import --input ./backup.tar.gz

# Preview local import first
node clawclone.mjs local import --input ./backup.tar.gz --test

# Verify a backup file
node clawclone.mjs local verify ./backup.tar.gz
```

### Share Backups

```bash
# Create a share link
node clawclone.mjs share create <clone-id>

# Check share status
node clawclone.mjs share status <clone-id>

# Revoke share link
node clawclone.mjs share revoke <clone-id>

# Clone from shared backup
node clawclone.mjs share get <share-token>
```

### Configuration

```bash
# Show current configuration
node clawclone.mjs config show

# Initialize configuration
node clawclone.mjs config init
```

### Status

```bash
# Show connection status and statistics
node clawclone.mjs status

# Show detailed information
node clawclone.mjs status --verbose
```

## Common Workflows

### Push OpenClaw workspace to cloud
```bash
node clawclone.mjs push --name "Production-$(date +%Y%m%d)" --tags "prod,backup"
```

### Migrate to new instance
**Old machine:**
```bash
node clawclone.mjs push --name "Migration-Snapshot"
# Note the clone-id from output
```

**New machine (after installing OpenClaw + clawclone):**
```bash
# Step 1: Test clone first (recommended)
node clawclone.mjs clone <clone-id> --test

# Step 2: Review the test report, then apply
node clawclone.mjs clone <clone-id>
```

### Share configuration with team
```bash
# Push and share
node clawclone.mjs push --name "Team-Template" --description "Standard setup"
node clawclone.mjs share create <clone-id>

# Team members can clone from the share link
node clawclone.mjs share get <share-token>
```

### Safe clone workflow
```bash
# Always test first to see what will be changed
node clawclone.mjs clone <clone-id> --test

# Review the test report output:
# - Check which files/components will be modified
# - Verify the backup metadata matches expectations
# - Ensure no unexpected changes

# If everything looks good, proceed with actual clone
node clawclone.mjs clone <clone-id>
```

### Local backup workflow
```bash
# Export to local file
node clawclone.mjs local export --name "Daily-Backup" --output ~/backups/$(date +%Y%m%d).tar.gz

# Verify the backup
node clawclone.mjs local verify ~/backups/$(date +%Y%m%d).tar.gz

# Import when needed
node clawclone.mjs local import --input ~/backups/20260315.tar.gz --test
node clawclone.mjs local import --input ~/backups/20260315.tar.gz
```

## Configuration

Set via environment variables:

```bash
# ClawClone API Key (required for cloud operations)
export CLAWCLONE_API_KEY="your_clawclone_api_key"
```

## Notes

- ClawClone automatically creates pre-restore backups at `~/.openclaw/backup`
- Gateway tokens are preserved by default (use `--overwrite-token` to override)
- Use `--test` flag to preview changes before applying them

## Then

Notice users that them can visit https://clawclone.cc to view and manage their backed up OpenClaw souls.
