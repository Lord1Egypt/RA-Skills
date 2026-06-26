---
name: backupclaw
description: Backup and restore OpenClaw configuration files. Use when the user wants to backup ~/.openclaw/ configuration (excluding workspace) to a date-stamped directory, or restore from a previous backup. Includes backup with diff-based change detection and changelog logging, and restore by date. The backup directory path ($backup_claw_dir) must be obtained from the user before first use.
---

# Backupclaw

## Overview

Full backup and restore capability for OpenClaw configuration files. Backups are stored in date-stamped directories (YYYY-MM-DD format). Only performs backup when configuration has actually changed.

## Core Operations

### 0. Backup Directory Management (NEW)

**Configuration file:**
- Location: `~/.openclaw/backup.json`
- Format:
  ```json
  {
    "backup_location": "/path/to/backup/directory"
  }
  ```

**Get backup directory:**
1. Check if `~/.openclaw/backup.json` exists
2. If exists, read "backup_location" field
3. If missing or file doesn't exist:
   - Ask user for backup directory path
   - Create `~/.openclaw/backup.json` with the provided path
   - Confirm path to user

**Change backup directory (changedir command):**
When user runs `backupclaw changedir <new_path>`:
1. Validate new path exists and is writable
2. Update `~/.openclaw/backup.json` with new path
3. Inform user of successful change

**Example changedir usage:**
- "backupclaw changedir ~/backups/openclaw"
- "修改备份目录到 /mnt/backup/openclaw"

### 1. Backup Configuration

**Backup directory setup:**
- Get backup directory using the management flow above (Section 0)
- No longer store in TOOLS.md; use backup.json instead

**Backup process:**
1. Generate current date string in YYYY-MM-DD format
2. If backup directory has no previous backups:
   - Copy all files from `~/.openclaw/` to `$backup_claw_dir/YYYY-MM-DD/`, excluding `workspace/`
   - Record initial backup in changelog
3. If previous backups exist:
   - Find the most recent backup directory (latest date)
   - Compare files between latest backup and current `~/.openclaw/` using `diff`
   - If no changes detected: Tell user "配置文件没有变化，不需要备份"
   - If changes detected:
     - Create new date-stamped directory
     - Copy all files from `~/.openclaw/` to new directory, excluding `workspace/`
     - Update changelog with list of modified files
     - Report changes to user

**Changelog format:**
- Located at `$backup_claw_dir/changelog.md`
- Each entry includes date, time, and list of changed files
- Format example:
  ```markdown
  ## 2026-03-12 14:30:00
  - openclaw.json (modified)
  - extensions/feishu/skills/feishu-doc/SKILL.md (added)
  ```

**Exclusion rules:**
- Always exclude `workspace/` directory from backup
- Preserve directory structure for all other files

### 2. Restore Configuration

**Restore process:**
1. Accept date parameter in YYYY-MM-DD format
2. Verify backup directory exists at `$backup_claw_dir/YYYY-MM-DD/`
3. If backup not found, inform user and list available dates
4. If backup found:
   - Warn user about overwriting current configuration
   - Confirm before proceeding
   - Restore files from backup to `~/.openclaw/`
   - Exclude `workspace/` from restoration
   - Report success and list restored files

## Usage Examples

**Typical user requests that trigger this skill:**
- "backup my openclaw config"
- "restore openclaw backup from 2026-03-12"
- "check if config changed"
- "备份 openclaw 配置"
- "恢复 2026-03-12 的备份"
- "backupclaw changedir ~/backups/openclaw"
- "修改备份目录" (prompts for new path)

## Implementation Notes

**Tools to use:**
- `rsync` or `cp -r` for copying files
- `diff` for comparing file contents
- `find` with `sort` and `tail` to find latest backup
- Date command: `date +%Y-%m-%d`
- `read` and `write` tools for managing `~/.openclaw/backup.json`

**Backup directory management:**
- Always check `~/.openclaw/backup.json` first before asking user
- Only prompt for backup path if backup_location is not set
- Validate directory exists and is writable before saving
- Use `write` tool to create/update backup.json

**changedir command handling:**
- Parse command format: `backupclaw changedir <path>` or equivalent Chinese phrasing
- Validate new directory exists and is writable (create if doesn't exist, ask first)
- Update backup.json with new path
- Confirm successful change to user

**Backup directory structure:**
```
$backup_claw_dir/
├── 2026-03-12/
│   ├── openclaw.json
│   ├── agents/
│   ├── extensions/
│   └── ...
├── 2026-03-13/
│   └── ...
└── changelog.md
```

**Error handling:**
- Always verify backup directory exists and is writable before proceeding
- Check for sufficient disk space
- Validate date format for restore operation
- Provide clear error messages in Chinese when appropriate
