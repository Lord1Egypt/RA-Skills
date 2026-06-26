---
name: core-files-management
description: "Core Files Management for OpenClaw workspace agents. Use when: (1) managing or updating core Markdown files (identity.md, soul.md, agents.md, user.md, memory.md, tools.md, bootstrap.md), (2) checking file organization, (3) ensuring no duplication between core files, (4) applying language rules, (5) user or agent asks about file structure or management. This skill manages the 6 core files + bootstrap.md in any OpenClaw workspace. Language rules: User communication → agent's native language, Between agents → Chinese, Code/Technical → English."
---

# CORE FILES MANAGEMENT 📁

> Universal management of OpenClaw core files

| Info | Value |
|------|-------|
| **Version** | 1.1.0 — 2026-05-07 |
| **Status** | OPERATIONAL |

---

## 1. PURPOSE AND SCOPE

### Objective

Manage the 6 core files + bootstrap.md in an OpenClaw workspace without duplication.

### Universal Design

This skill works for ANY OpenClaw agent. Adapt language rules to your user's preferences.

### When to Use

| Trigger | Action |
|---------|--------|
| Modify a core file | Check distribution rules |
| Verify organization | Read all core files |
| Avoid duplication | Use modification checklist |
| User asks about structure | Read this skill and give summary |

---

## 2. THE 6 CORE FILES

| # | File | Definition | Key Content |
|---|------|------------|-------------|
| 1 | **identity.md** | Agent's "first impression" | Name, avatar, signature, functions, language architecture |
| 2 | **soul.md** | Agent's "heart" — personality & values | Essence, values, L7/L8 memory integration |
| 3 | **agents.md** | Logic & procedures manual | Specs, workspace rules, heartbeat, red lines |
| 4 | **user.md** | User context | User's info, preferences, infrastructure |
| 5 | **memory.md** | Long-term memory | Important events, key configs, workflows |
| 6 | **tools.md** | Technical configuration | Endpoints, hosts, commands, services |

### Plus: bootstrap.md

| File | Definition | Purpose |
|------|------------|---------|
| **bootstrap.md** | Machine startup sequence | NOT soul — machine boot order only |

---

## 3. DISTRIBUTION RULES

| Content Type | Target File |
|--------------|------------|
| Identity | `identity.md` |
| Personality/Values | `soul.md` |
| Operational Rules | `agents.md` |
| User Context | `user.md` |
| Persistent Facts | `memory.md` |
| Technical Config | `tools.md` |
| Startup Sequence | `bootstrap.md` |

**Rule:** Each file has ONE purpose. Don't mix content types.

### Cluster Integration

| Component | Purpose | Location |
|-----------|---------|----------|
| identity.md | Agent's first impression | Workspace root |
| soul.md | Agent's heart | Workspace root |
| agents.md | Operational rules | Workspace root |
| cluster configuration | Agent connections | Workspace/cluster/ |
| skill storage | Published skills | workspace/skills/ |

---

## 4. LANGUAGE RULES

Adapt to your agent's context:

| Context | Language | Example |
|---------|----------|---------|
| **User communication** | Agent's native language | "Bonjour!" / "Hello!" / "你好!" |
| **Between agents** | Chinese | "你好！很高兴与你交流" |
| **Code/Technical** | English | `python3 script.py` |

**Rule:** Every identity.md MUST state the user's communication language.

---

## 5. TOOLS

### Required OpenClaw Tools

| Tool | Usage | Mode |
|------|-------|------|
| `read` | Read core files | Required |
| `write` | Modify core files | Required |
| `edit` | Fix specific sections | Optional |
| `exec` | Verify file status, backup | Optional |

### Verification Commands

```bash
# List core files
ls -la ~/.openclaw/workspace/*.md

# Check file content
head -20 ~/.openclaw/workspace/identity.md

# Backup before modification
cp ~/.openclaw/workspace/<file>.md ~/.openclaw/workspace/<file>.md.bak

# Count lines in all files
wc -l ~/.openclaw/workspace/*.md

# Verify file exists
test -f ~/.openclaw/workspace/identity.md && echo "exists"

# Count files
ls ~/.openclaw/workspace/*.md | wc -l

# Full file listing
find ~/.openclaw/workspace -maxdepth 1 -name "*.md" -type f
```

### Required Permissions

| Permission | Purpose |
|------------|---------|
| Read workspace | Access core files |
| Write workspace | Modify core files |
| Exec (optional) | File operations, backups |

### Backup & Restore

```bash
# Create backup
cp ~/.openclaw/workspace/identity.md ~/.openclaw/workspace/identity.md.backup

# Restore from backup
cp ~/.openclaw/workspace/identity.md.backup ~/.openclaw/workspace/identity.md

# List backups
ls ~/.openclaw/workspace/*.backup
```

---

## 6. MODIFICATION CHECKLIST

Before modifying any core file:

```
1. Which file does this content belong to?
   → Identity → identity.md
   → Personality/Values → soul.md
   → Operational Rules → agents.md
   → User → user.md
   → Persistent Facts → memory.md
   → Technical Config → tools.md

2. Is it already somewhere else?
   → Check all 6 core files

3. Are language rules clear?
   → User → their native language
   → Agents → Chinese
   → Code → English

4. Does it need backup?
   → YES → Backup first!
```

---

## 7. FILE PATHS

| File | Default Path |
|------|--------------|
| identity.md | `~/.openclaw/workspace/identity.md` |
| soul.md | `~/.openclaw/workspace/soul.md` |
| agents.md | `~/.openclaw/workspace/agents.md` |
| user.md | `~/.openclaw/workspace/user.md` |
| memory.md | `~/.openclaw/workspace/memory.md` |
| tools.md | `~/.openclaw/workspace/tools.md` |
| bootstrap.md | `~/.openclaw/workspace/bootstrap.md` |

---

## 8. CONSTRAINTS

| Constraint | Description |
|------------|-------------|
| **No duplication** | Workspace rules in agents.md only, not soul.md or identity.md |
| **No mixing** | tools.md is technical ONLY — no personality content |
| **No bloating** | memory.md does NOT contain full session logs |
| **Backup first** | Always backup before changing core files |
| **One purpose per file** | Don't mix content types |

---

## 9. ERROR HANDLING

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Content in wrong place | Didn't check distribution rules | Re-read checklist, reassign |
| Duplication | Same content in multiple places | Merge, keep only one |
| Missing language | Didn't check language rules | Add user's native language |
| Data loss | Modification without backup | Restore from backup |

### Security Issues

| Issue | Severity | Action |
|-------|----------|--------|
| Overwriting without backup | HIGH | Always backup first |
| Wrong file modified | MEDIUM | Verify before write |
| Missing language rule | LOW | Add to identity.md |

---

## 10. EDGE CASES

| Case | Treatment |
|------|-----------|
| **File missing** | Create from scratch with correct format |
| **File corrupted** | Restore from backup or recreate |
| **Massive duplication** | Read all files, reorganize by type |
| **New agent setup** | Create all 6 core files + bootstrap.md |
| **Path unclear** | Use default `~/.openclaw/workspace/` |

---

## 11. USAGE COMMANDS

```bash
# List all core files
ls -la ~/.openclaw/workspace/*.md

# Check a specific file
head -20 ~/.openclaw/workspace/identity.md

# Backup before modification
cp ~/.openclaw/workspace/<file>.md ~/.openclaw/workspace/<file>.md.bak

# Count lines in all files
wc -l ~/.openclaw/workspace/*.md
```

---

## 12. TEMPLATE — Empty Core File

### identity.md

```markdown
# IDENTITY.md — [Agent Name]

> Identity = First impression

| Attribute | Value |
|-----------|-------|
| **Name** | [Your name] |
| **Signature** | [Your signature emoji] |
| **Role** | [Your role] |

## Language Rules

- User communication: [Native language]
- Between agents: Chinese
- Code/Technical: English

_In Altum Per [Your Principle]._
[Your name]
```

---

_In Altum Per CoreFiles._
📁 Core Files Management v1.1