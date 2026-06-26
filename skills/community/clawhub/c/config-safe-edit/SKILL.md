---
name: config-safe-edit
description: Safe configuration file editing workflow. Before modifying openclaw.json, models.json, or any system config file, activate this skill. Core value: backup before edit + diff after change = no surprises. Prevents config corruption that can brick your system.
---

# Config Safe Edit

Edit config files without breaking things.

## The Problem

Configuration files are where agents cause the most irreversible damage. One wrong keystroke and your system won't start. This skill makes config changes predictable and reversible.

## Core Principle

**Backup → Edit → Diff → Commit or Recover**

Never edit a config file without being able to undo it.

---

## Standard Workflow (5 Steps)

### Step 1: Scope the Change

Before touching anything, answer these:
1. **What file?** Full path.
2. **What fields?** Exact key paths.
3. **What should change?** Before/after values.

If any answer is unclear → **stop and ask**.

### Step 2: Choose Your Tool

| Tool | When to use |
|------|-------------|
| `gateway config.patch` | Safe, validates JSON, hot-reload when possible |
| Direct file edit (`edit` tool) | Credentials, protected paths, or when patch fails |

**Protected paths that always need direct edit**: `appId`, `clientSecret`, `appSecret`, `token`, `apiKey`, `apiKey*`, `password`

Test if a field is protected by trying `config.patch` first. If it errors with "cannot change protected config paths" → use direct edit.

### Step 3: Locate Before You Edit

Use search to find exact line numbers, then edit precisely:

```bash
# Find field and surrounding context
grep -n "the_field_name" /path/to/config.json
```

```powershell
# PowerShell equivalent
Select-String -Path "C:\path\to\config.json" -Pattern "the_field_name" -Context 0,2
```

**Never do blind edits.** Always confirm you know exactly which occurrence to change.

### Step 4: Backup

```bash
# Linux/Mac
cp /path/to/config.json /path/to/config.json.backup

# Windows
Copy-Item "C:\path\to\config.json" "C:\path\to\config.json.backup"
```

**Always overwrite the same file — no date suffix.** This keeps exactly one backup on disk. After diff confirms the change is correct, the backup is no longer needed and can be overwritten by the next edit.

### Step 5: Diff Before Restarting

```bash
# Linux/Mac
diff /path/to/config.json.backup.* /path/to/config.json

# PowerShell
diff (Get-Content "config.bak") (Get-Content "config.json")
```

**Only proceed if diff shows exactly what you intended.** Any unexpected lines = revert immediately.

---

## Common Failure Patterns

### 1. Protected field with wrong tool
**Symptom**: `gateway config.patch` errors with "cannot change protected config paths"
**Fix**: Use direct `edit` on the file instead

### 2. Typo in field name
**Symptom**: Config appears correct but system behaves unexpectedly
**Fix**: Always search first (Step 3), don't guess field names

### 3. JSON syntax error
**Symptom**: Gateway won't start, error about JSON parse failure
**Fix**: Before any edit, validate JSON: `python3 -c "import json; json.load(open('config.json'))"`

### 4. Trailing comma or missing bracket
**Symptom**: Same as above — JSON malforms
**Fix**: After any edit, always validate JSON before restarting

### 5. Only one backup file exists
**Problem**: Backup is overwritten each time — no historical versions
**Fix**: If you need a dated snapshot before a risky edit, manually `cp config.json config.json.backup.2026-05-07` first. The standard workflow uses a single overwrite-safe backup.

---

## Recovery Checklist

When something goes wrong:
1. `diff` current vs backup → identify the unexpected change
2. Copy backup over current: `cp backup.json config.json`
3. Validate JSON: `python3 -c "import json; ..."` or `Get-Content x.json | ConvertFrom-Json`
4. Only after JSON validates clean → restart

---

## Quick Reference

```
SCOPE:   What file, what field, what's new value?
LOCATE:  grep/Select-String before touching anything
BACKUP:  cp config.json config.json.backup   # overwrite-safe, no date suffix
EDIT:    edit tool or config.patch
DIFF:    diff backup vs new — only proceed if exact match
RECOVER: cp config.json.backup config.json → validate → restart
```

## When to Skip This Skill

- Read-only operations (reading config, searching)
- Non-critical files (user preferences, cosmetic settings)
- Files with automatic backup (version-controlled config files)

**Always use this for**: credentials, API keys, server addresses, port numbers, security settings, channel configurations.

---

## High-Risk Edits: OpenClaw Startup Files

Some edits can lock you out of your own system. Treat these with extra care.

### What Counts as High-Risk

Edits to these fields are high-risk — they can prevent OpenClaw from starting:
- `gateway.port`, `gateway.bind`, `gateway.auth`
- `plugins`, `plugins.allow`, `plugins.entries`
- `meta.version`, `meta.lastTouchedVersion`
- `channels` (channel misconfiguration can crash the plugin loader)

### High-Risk Workflow (adds 2 extra steps)

**Before the edit**: Manually create a dated snapshot backup:
```bash
# Windows
Copy-Item "openclaw.json" "openclaw.json.backup.$(Get-Date -Format 'yyyy-MM-dd')"
```

**After the edit, before saying "OK to restart"**: Always validate JSON syntax:
```bash
# Windows PowerShell
python3 -c "import json; json.load(open('C:/path/to/openclaw.json'))"
```

If Python returns nothing → JSON is valid. If it throws an exception → syntax error, fix before continuing.

**After restart**: If Gateway won't come back:
1. OpenClaw auto-generates `.bak` files on each config save — find the latest one in the same directory
2. If the directory is accessible from outside (e.g., via Explorer): restore the `.bak` file
3. If Gateway is completely unresponsive: this is a true lockout — human intervention required

### Honest Limit

If the JSON is valid but the config is semantically wrong (e.g., wrong port number), Gateway will start but behave unexpectedly. There is no automated fix for this — it requires human diagnosis. The best defense is **Step 1 (Scope)**: always know exactly what you're changing and why before you touch anything.