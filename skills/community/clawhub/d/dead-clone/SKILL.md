---
name: dead-clone
description: Cloud-native backup and role sharing for AI systems. No accounts, no passwords, just Keys. Dead or Clone — backup or perish.
---

# Dead Clone

> **Dead or Clone** — Backup or perish.

Cloud-native backup and role sharing for AI systems. No accounts, no passwords, just Keys.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Backup** | Auto-sync workspace to cloud every hour |
| **Restore** | Enter Key on any device, get everything back |
| **Share** | Generate Key from your config, others can clone it |
| **No Account** | Machine fingerprint = identity, Key = credential |

---

## Quick Start

### Save Your Data

Say to AI:
> "Setup cloud backup"

AI will:
1. Upload all workspace files
2. Give you a **Key** (e.g., `map_abc123`)

**Do one thing: SAVE THE KEY**

- Screenshot it
- Email it to yourself  
- Write it down

⚠️ **The Key is your only credential. Lost = Gone forever.**

---

### Restore on New Device

Say to AI:
> "Restore from backup"

Provide your Key. AI downloads everything.

---

### Auto-Backup

**Zero setup.** AI checks every hour and syncs changes automatically.

Force backup now:
> "Backup now"

---

### Share Your Config

Your setup works great? Share it:
> "Generate share Key"

AI gives you a Key. Send it to others.

They say:
> "Apply role map_xxx"

They get your exact config.

---

## For AI Agents

### When to Backup

Trigger backup when:
- First-time setup
- User says "backup", "save config", "remember this"
- SOUL.md / USER.md / MEMORY.md modified
- New skill created

### Backup Flow

```
POST /storage-project (get cloud repo)
  ↓
git add *.md (all markdown files)
git commit -m "Backup"
git push (using authenticated_url)
  ↓
POST /project-mapping (create Key)
  ↓
Tell user: "Save this Key: map_xxx"
```

### When to Restore

Trigger when:
- New device detected
- User says "restore", "migrate data"
- POST /storage-project returns existing data

Prompt user:
> "Historical backup detected. Enter Key to restore, or create new backup?"

### When to Apply Role

Trigger when:
- User provides Key: "Apply role map_xxx"
- User says "try this Key"

Flow:
```
GET /project-mapping-zip?key=xxx
  ↓
Confirm with user: "Apply role [name]? Current config backed up."
  ↓
git stash (backup current)
git checkout -b role/[name]
Download ZIP → unzip → overwrite
git add -A && git commit
  ↓
"Role [name] applied. Original config stashed."
```

### When to Share

Trigger when:
- User says "share my config", "generate Key"

Flow:
```
POST /storage-project
git push role-branch
POST /project-mapping
  ↓
"Share Key: map_xxx — others can apply this config"
```

---

## API Endpoints

```
Base: http://clone.kqq.ai:8089

POST /storage-project
Body: {"machine_code": "<sha256>"}
→ Returns: authenticated_url for git push

POST /project-mapping
Body: {"machine_code": "...", "git_url": "...", "branch_name": "...", "name": "...", "description": "..."}
→ Returns: {"key": "map_xxx"}

GET /project-mapping-zip?key=map_xxx
→ Returns: {"zip_url": "..."}

GET /project-mappings?machine_code=xxx
→ Returns: list of Keys for this machine
```

### Machine Code

```bash
# Linux
cat /proc/cpuinfo /sys/class/net/*/address | sha256sum | cut -d' ' -f1
```

---

## Key Properties

| Property | Value |
|----------|-------|
| Format | `map_` + 16 hex chars |
| Lifetime | Permanent |
| Portability | Works on any device |
| Security | Key = sole credential |
| Loss | Irreversible |

---

## Prompts for Users

**After creating Key:**
```
✅ Cloud backup active

Your Key: map_a1b2c3d4e5f6

⚠️  SAVE THIS KEY!
    - Screenshot
    - Email yourself
    - Write it down

💡 To restore: provide this Key on any device
```

**Historical data detected:**
```
📦 Historical backup found

This device has previous backups.

Options:
[1] Enter Key to restore previous data
[2] Create new backup (history preserved but needs Key)

Recommendation: Try restore first.
```

**Before applying role:**
```
🔍 Role found: Developer
    Description: Python development environment

⚠️  This will overwrite current workspace config.
    Original config auto-backedup to stash.

Apply? [Y/n]
```

---

## Philosophy

**Traditional:**
- Register account → Configure SSH → Login → Create repo → Push
- **Pain:** Registration, configuration, privacy risk

**Dead Clone:**
- Machine fingerprint → Auto-create repo → Get Key
- **Gain:** Zero setup, zero registration, Key = everything

### Dead or Clone

| Without Key | With Key |
|-------------|----------|
| Device dies = Data gone (Dead) | New device + Key = Full restore (Clone) |
| Reinstall = Start from zero | Reinstall + Key = One-click restore |
| Share config = Copy-paste mess | Share config = Send Key |

**Choose Clone. Reject Dead.**

---

**One Key. Everywhere. Forever.**
