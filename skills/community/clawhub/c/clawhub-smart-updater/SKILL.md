# ClawHub Smart Updater Skill 🔄

## Description

Intelligent ClawHub skill updater with **smart merge** capabilities. Preserves local modifications, detects conflicts, and provides detailed merge recommendations instead of blindly overwriting files.

## When to Use This Skill

Use this skill when:
- You have **locally modified skills** from ClawHub
- You want to update skills **without losing your changes**
- You need **conflict detection** and merge recommendations
- You want **automatic backups** before updates
- You prefer **safe, conservative updates** over risky auto-updates

## Key Differences from auto-updater

| Feature | Smart Updater | auto-updater |
|---------|--------------|--------------|
| Local change detection | ✅ Yes | ❌ No |
| Conflict detection | ✅ Yes | ❌ No |
| Automatic backup | ✅ Yes | ❓ Unknown |
| Merge recommendations | ✅ Yes | ❌ No |
| Update frequency | Weekly (safe) | Daily (risky) |
| Blind overwrite | ❌ Never | ⚠️ Likely |

## Installation

```bash
# Install via ClawHub
clawhub install clawhub-smart-updater

# The skill installs:
# - smart-update.py (main updater script)
# - restore-backup.py (rollback tool)
# - config.json (configuration)
```

## Usage

### Quick Start

```bash
# Run smart update check
python skills/clawhub-smart-updater/smart-update.py

# This will:
# 1. Check all installed skills for updates
# 2. Backup current versions
# 3. Download new versions to temp
# 4. Compare and categorize changes
# 5. Generate report with recommendations
```

### Command Line Options

```bash
# Dry run (no changes)
python smart-update.py --dry-run

# Update specific skill
python smart-update.py --slug image-with-comfyui

# Force update (skip conflict detection)
python smart-update.py --force

# Verbose output
python smart-update.py --verbose

# Cleanup old backups
python smart-update.py --cleanup-backups --older-than 7
```

### OpenClaw Cron Integration

The skill is designed for OpenClaw cron jobs:

```json
{
  "cron": {
    "jobs": [
      {
        "name": "Weekly Smart Update",
        "schedule": {
          "kind": "cron",
          "expr": "0 10 * * 1",
          "tz": "Europe/Prague"
        },
        "payload": {
          "kind": "agentTurn",
          "message": "Run smart-update.py --report and send summary to user"
        },
        "delivery": {
          "channel": "whatsapp",
          "to": "<YOUR_PHONE_NUMBER>"
        }
      }
    ]
  }
}
```

## How It Works

### 1. Discovery Phase
```bash
clawhub list → Get installed skills
clawhub inspect <slug> → Get latest version
Compare: local_version vs latest_version
```

### 2. Backup Phase
```powershell
Copy-Item skills/<slug> skills/<slug>.backup-YYYY-MM-DD -Recurse
```

### 3. Download Phase
```bash
clawhub inspect <slug> --files --output temp/<slug>-new
```

### 4. Analysis Phase
- Hash all files (SHA-256)
- Compare with original ClawHub hashes
- Identify locally modified files
- Categorize changes:
  - **Safe**: Docs, configs, untouched files
  - **Conflict**: Code files modified both upstream and locally

### 5. Merge Phase
- Apply safe changes automatically
- Flag conflicts for manual review
- Generate diff files
- Create merge report

### 6. Report Phase
Generate detailed report:
- What was updated
- What needs review
- Security warnings
- Statistics

## Configuration

### config.json

```json
{
  "backup": {
    "enabled": true,
    "retention_days": 7,
    "directory": "skills/.backups"
  },
  "conflict": {
    "auto_backup": true,
    "generate_diff": true,
    "require_manual_review": true
  },
  "notification": {
    "enabled": true,
    "channel": "whatsapp",
    "target": "<YOUR_PHONE_NUMBER>",
    "on_conflict_only": false
  },
  "update": {
    "auto_apply_safe": true,
    "auto_apply_conflicts": false,
    "ignore_whitespace": true
  }
}
```

## Output Examples

### Success Report

```markdown
## Smart Update Report - 2026-05-07

### ✅ Auto-Updated (2 skills):
- image-with-comfyui: 1.4.8 → 1.4.9 (docs only)
- moltbook-interact: 1.0.0 → 1.0.1 (bugfix)

### ⚠️ Manual Review Required (1 skill):
- fusion-bridge: 1.0.2 → 1.0.3
  - Conflict in main.py (lines 45-67)
  - See: temp/fusion-bridge/diff.txt

### Stats:
- Checked: 23 skills
- Updated: 2
- Conflicts: 1
- Backups cleaned: 3
```

### Conflict Report

```markdown
### ⚠️ fusion-bridge: Conflict Detected

**Local changes:**
- Modified: main.py (custom error handling)
- Modified: SKILL.md (Czech translations)

**Upstream changes:**
- Fixed: main.py (bugfix in connect() function)
- Updated: README.md (new examples)

**Conflict:**
Both local and upstream modified main.py lines 45-67

**Recommendation:**
Manual merge required. Upstream bugfix is important, but preserve custom error handling.

**Actions:**
1. Review: temp/fusion-bridge/diff.txt
2. Merge manually
3. Run: python smart-update.py --accept fusion-bridge
```

## Safety Features

### Backup System
- Automatic pre-update backups
- Dated backup folders
- Configurable retention (default: 7 days)
- Easy rollback with `restore-backup.py`

### Conflict Detection
- SHA-256 content hashing
- Tracks which files you've modified
- Intelligent categorization
- Diff generation for conflicts

### Security
- VirusTotal integration (warns on SUSPICIOUS)
- Dependency change detection
- Permission audit
- No blind overwrites

## Troubleshooting

### "Permission denied" error
**Cause:** File locked by editor or process

**Solution:**
```bash
# Close editors using skill files
# Or force unlock
python smart-update.py --force-unlock
```

### Backup directory too large
**Cause:** Old backups accumulating

**Solution:**
```bash
python smart-update.py --cleanup-backups --older-than 7
```

### False positive conflicts
**Cause:** Whitespace changes detected

**Solution:**
```bash
python smart-update.py --ignore-whitespace
```

## Files Included

- `smart-update.py` - Main updater script
- `restore-backup.py` - Rollback tool
- `config.json` - Configuration
- `SKILL.md` - This documentation
- `README.md` - Extended documentation

## Requirements

- Python 3.10+
- ClawHub CLI installed
- Git (optional, for advanced diff)
- Windows PowerShell (for backup scripts)

## License

MIT-0 - Free to use, modify, and redistribute without attribution.

## Author

**Klepeto 🦞** (vilda)  
Created: 2026-05-07  
Tested on: Windows 11, Python 3.12

## Changelog

### 1.0.0 (2026-05-07)
- Initial release
- Smart merge with conflict detection
- Automatic backup system
- Diff generation
- OpenClaw cron integration
- WhatsApp reporting
