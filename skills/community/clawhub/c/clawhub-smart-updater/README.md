# ClawHub Smart Updater 🔄

**Intelligent skill updater with merge conflict detection and local change preservation.**

Unlike simple updaters that blindly overwrite files, Smart Updater analyzes changes, detects conflicts, and preserves your local modifications.

## 🌟 Key Features

### Smart Merge Technology
- **Detects local modifications** - Knows which files you've edited
- **Preserves your changes** - Never blindly overwrites local work
- **Conflict detection** - Flags files where upstream and local changes collide
- **Automatic backup** - Creates dated backups before any update
- **Diff generation** - Shows exactly what changed upstream vs locally

### Safe Update Workflow
1. **Backup** current skill version
2. **Download** new version to temp directory
3. **Compare** files using content hashing
4. **Categorize** changes:
   - ✅ **Safe**: Documentation, configs (auto-apply)
   - ⚠️ **Conflict**: Code changes (flag for review)
5. **Report** with merge recommendations
6. **Cleanup** old backups after 7 days

## 📦 Installation

```bash
# Install via ClawHub
clawhub install clawhub-smart-updater

# Or clone manually
git clone https://github.com/yourusername/clawhub-smart-updater.git
```

## 🚀 Usage

### Manual Update Check

```bash
# Run the updater script
python skills/clawhub-smart-updater/smart-update.py

# Or use ClawHub CLI
clawhub update --all
```

### Automated (Cron Job)

Add to your crontab or Task Scheduler:

```bash
# Weekly update check (every Monday at 10:00)
0 10 * * 1 cd /path/to/workspace && python skills/clawhub-smart-updater/smart-update.py --report
```

### OpenClaw Integration

Use with OpenClaw cron tool:

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
          "message": "Run smart-update.py with --report flag"
        }
      }
    ]
  }
}
```

## 📊 Update Report Example

```markdown
## Weekly ClawHub Update - 2026-05-07

### ✅ Auto-Updated (Safe Changes):
- image-with-comfyui: 1.4.8 → 1.4.9
  - Changed: README.md (typo fixes)
  - Changed: docs/usage.md (examples)
  - Status: Applied automatically

- moltbook-interact: 1.0.0 → 1.0.1
  - Changed: SKILL.md (API endpoint update)
  - Status: Applied automatically

### ⚠️ Requires Manual Review:
- fusion-bridge: 1.0.2 → 1.0.3
  - Changed: main.py (upstream bugfix)
  - Local changes: Custom error handling (lines 45-67)
  - Conflict: Both upstream and local modified same function
  - Recommendation: Manual merge required
  - Diff: temp/fusion-bridge/diff.txt

### Security Alerts:
- None

### Statistics:
- Skills checked: 23
- Skills updated: 2
- Conflicts detected: 1
- Old backups cleaned: 3 (>30 days)
```

## 🔧 Configuration

### Update Settings

Edit `config.json`:

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
    "channel": "whatsapp",
    "target": "<YOUR_PHONE_NUMBER>",
    "on_conflict_only": false
  }
}
```

### Advanced Options

```bash
# Dry run (no changes, just report)
python smart-update.py --dry-run

# Force update (skip conflict detection)
python smart-update.py --force

# Update specific skill only
python smart-update.py --slug image-with-comfyui

# Verbose output
python smart-update.py --verbose

# Generate diff files for conflicts
python smart-update.py --generate-diff
```

## 🛡️ Safety Features

### Backup Strategy
- **Pre-update backup**: Every skill backed up before modification
- **Dated folders**: `skill-name.backup-YYYY-MM-DD`
- **Automatic cleanup**: Backups older than 7 days deleted
- **Recovery**: Easy rollback with `restore-backup.py`

### Conflict Detection
- **Content hashing**: SHA-256 comparison of file contents
- **Change tracking**: Knows which files you've modified
- **Intelligent categorization**:
  - Documentation changes → Safe to apply
  - Bug fixes in untouched files → Safe to apply
  - Changes to modified files → Flag for review

### Security Checks
- **VirusTotal integration**: Warns about SUSPICIOUS flagged skills
- **Dependency audit**: Checks for new dependencies in updates
- **Permission review**: Alerts on new file permissions

## 📝 Manual Merge Guide

When conflicts are detected:

1. **Review the diff**:
   ```bash
   cat temp/skill-name/diff.txt
   ```

2. **Compare versions**:
   ```bash
   # Your version
   code skills/skill-name/main.py
   
   # Upstream version
   code temp/skill-name-new/main.py
   ```

3. **Merge manually**:
   - Copy upstream changes you want
   - Preserve your local modifications
   - Test the merged result

4. **Apply or reject**:
   ```bash
   # Accept merge
   python smart-update.py --accept skill-name
   
   # Reject and keep yours
   python smart-update.py --reject skill-name
   ```

## 🐛 Troubleshooting

### Update fails with "Permission denied"
**Cause:** File locked by another process

**Solution:**
```bash
# Close any editors using the skill files
# Or force unlock (Windows)
python smart-update.py --force-unlock
```

### Backup directory too large
**Cause:** Old backups not cleaned

**Solution:**
```bash
# Manual cleanup
python smart-update.py --cleanup-backups --older-than 7
```

### False positive conflicts
**Cause:** Whitespace or formatting changes detected

**Solution:**
```bash
# Ignore whitespace in diff
python smart-update.py --ignore-whitespace
```

## 🤝 Contributing

Found a bug or have improvement ideas?

1. Fork the repository
2. Create a feature branch
3. Test thoroughly with real skills
4. Submit a pull request

## 📚 Related Tools

- **ClawHub CLI** - Official ClawHub command-line tool
- **clawhub-auto-updater** - Simpler auto-updater (no merge)
- **openclaw-safe-audit** - Security audit for OpenClaw

## 📄 License

MIT-0 - Free to use, modify, and redistribute without attribution.

## 👥 Authors

- **Klepeto 🦞** (vilda) - Smart merge logic
- **Community contributors** - Testing and feedback

## 🗺️ Roadmap

- [ ] Git-like three-way merge for automatic conflict resolution
- [ ] Interactive merge tool (terminal UI)
- [ ] Rollback to specific version
- [ ] Update scheduling UI
- [ ] Multi-user collaboration support

---

**Version:** 1.0.0  
**Last Updated:** 2026-05-07  
**Tested On:** Windows 11, Python 3.12
