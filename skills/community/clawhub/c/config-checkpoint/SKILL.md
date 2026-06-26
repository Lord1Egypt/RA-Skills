---
name: git-version-control
description: |
  Git-based version control for OpenClaw system configuration changes.
  
  Provides two core capabilities:
  (1) SAVE - Create a checkpoint before sensitive operations (git add & commit)
  (2) ROLLBACK - Revert to a previous state if issues occur (git reset)
  
  Use when:
  - Before making sensitive configuration changes
  - Before installing/removing skills
  - Before modifying core files (SOUL.md, AGENTS.md, MEMORY.md, etc.)
  - User requests to undo recent changes
  - System state needs recovery after errors
  
  SECURITY: Always verify .gitignore and scan for sensitive files before SAVE.
  DANGER: Hard reset permanently destroys uncommitted changes.
---

# Git Version Control | OpenClaw Configuration Protection

> Protect your OpenClaw environment with git-based checkpoints and rollback capability.

## ⚠️ Security Notice

**v0.2.0** includes critical safety enhancements:
- Pre-commit sensitive file scanning
- Mandatory .gitignore verification
- Hard reset confirmation with data loss warning
- Safer alternatives (soft/mixed reset)
- Autonomous operation restrictions

## Overview

OpenClaw configuration directory (`~/.openclaw/`) is a git repository. This skill provides safe version control for system configuration changes.

**Protected files include**:
- `workspace/SOUL.md`, `AGENTS.md`, `USER.md`, `IDENTITY.md`
- `workspace/skills/` - installed skills
- `workspace/memory/` - memory files
- `openclaw.json` - main configuration
- `cron/jobs.json` - cron jobs

**Excluded from version control**:
- Session logs (`*.jsonl`, `*.jsonl.lock`)
- SQLite databases (`*.sqlite`)
- Temporary files
- Credentials (sensitive)
- Python cache (`__pycache__/`)

---

## Core Operations

### 1. SAVE - Create Checkpoint

Create a git commit before making sensitive changes. This provides a recovery point.

**⚠️ SAFETY REQUIREMENTS (MUST follow in order)**:

1. **Verify .gitignore exists**
   ```bash
   test -f ~/.openclaw/.gitignore && echo "✓ .gitignore found" || echo "✗ .gitignore MISSING"
   ```
   If missing: **STOP** and create .gitignore first

2. **Scan for sensitive files** (before staging)
   ```bash
   # Check for potential sensitive files in untracked/modified
   cd ~/.openclaw
   git status --short | grep -E '\.(pem|key|token)$|credentials/|secret' && echo "⚠️ SENSITIVE FILES DETECTED"
   ```

3. **Review what will be committed**
   ```bash
   git add -A --dry-run
   git status
   ```
   Confirm no sensitive data before proceeding

4. **Commit with descriptive message**
   ```bash
   git commit -m "checkpoint: {description of pending change}"
   ```

**When to use**:
- Before modifying core configuration files
- Before installing/uninstalling skills
- Before making bulk memory changes
- User explicitly requests a save point

**SAFER ALTERNATIVE - Targeted Add**:

Instead of `git add -A`, use targeted paths to avoid accidental commits:

```bash
# Only add specific configuration files
git add workspace/SOUL.md workspace/AGENTS.md workspace/USER.md

# Or add entire directories with explicit paths
git add workspace/skills/
```

**Implementation**:
```
When user says: "save before..." or "create checkpoint"

1. [REQUIRED] Check .gitignore exists
   - If missing: STOP and warn user

2. [REQUIRED] Scan for sensitive files
   - If detected: STOP and show list
   - Ask user to verify .gitignore

3. Show what will be committed
   git status --short
   
4. Ask user confirmation if autonomous
   "Will commit {count} files. Proceed?"

5. Execute commit
   git add -A  # or targeted paths
   git commit -m "checkpoint: {description}"

6. Report commit hash and file count
```

**Example**:
```
User: "Save before I install a new skill"

Agent:
  1. Checking .gitignore... ✓ Found
  2. Scanning for sensitive files... ✓ None detected
  3. Files to commit:
     M workspace/AGENTS.md
     A workspace/skills/new-skill/SKILL.md
  4. Creating checkpoint...
     $ git add -A
     $ git commit -m "checkpoint: before installing new skill"
  
Output: "✓ Checkpoint created: abc1234 (5 files changed)"
```

---

### 2. ROLLBACK - Restore Previous State

Revert to a previous commit when issues occur.

**⚠️ DANGER: Hard Reset Destroys Data**

`git reset --hard` **permanently deletes** all uncommitted changes. There is NO undo.

**When to use**:
- User reports system issues after recent changes
- User explicitly requests rollback
- Configuration corruption detected
- After a failed skill installation

**Rollback Options** (try in order of safety):

| Option | Command | Safety | Effect |
|--------|---------|--------|--------|
| **Soft reset** | `git reset --soft HEAD~1` | ✅ Safe | Undo commit, keep changes staged |
| **Mixed reset** | `git reset --mixed HEAD~1` | ⚠️ Moderate | Undo commit, keep changes unstaged |
| **Hard reset** | `git reset --hard HEAD~1` | 🔴 Destructive | **Permanently delete** commit + changes |

**Recommended**: Always try **soft reset** first. Only use hard reset if absolutely necessary.

**Implementation**:
```
When user says: "rollback" or "undo last change"

1. Show recent commits
   git log --oneline -10

2. Ask which commit to restore to
   "Restore to which commit?"

3. [REQUIRED for hard reset] Show what will be lost
   git diff --stat {commit-hash}
   git status --short
   
4. [REQUIRED for hard reset] Explicit confirmation
   "⚠️ HARD RESET will permanently delete {count} uncommitted changes:"
   "  - {list of files}"
   "This cannot be undone. Proceed? (yes/no)"

5. Execute rollback
   - Prefer: git reset --soft {commit-hash}
   - If user confirms hard: git reset --hard {commit-hash}

6. Report result
   "✓ Rolled back to commit abc1234"
```

**Example**:
```
User: "Rollback to before the skill installation"

Agent:
  1. Recent commits:
     abc1234 checkpoint: before skill install
     def5678 previous config
     
  2. Restore to abc1234?
  
  3. Checking uncommitted changes...
     M workspace/skills/broken-skill/SKILL.md
     ?? workspace/skills/broken-skill/cache/
     
  4. ⚠️ Hard reset will DELETE these changes permanently. 
     Use soft reset to keep changes unstaged?
     
     [User confirms hard reset]
     
  5. Executing hard reset...
     $ git reset --hard abc1234
     
Output: "✓ Rolled back to 'before skill install' (abc1234)"
```

---

## Helper Operations

### View History

```bash
# Show recent commits
git log --oneline -10

# Show what changed in last commit
git show --stat HEAD

# Compare current state to last commit
git diff HEAD
```

### Check Status

```bash
# See uncommitted changes
git status

# See diff summary
git diff --stat
```

### List Protected Files

Files tracked for version control (in git):
```bash
git ls-files
```

### Verify .gitignore

```bash
# Check if .gitignore exists
test -f ~/.openclaw/.gitignore && echo "✓ .gitignore exists" || echo "✗ MISSING"

# Test if a file would be ignored
git check-ignore -v path/to/file
```

---

## .gitignore Configuration

Ensure `~/.openclaw/.gitignore` excludes volatile/sensitive files:

```gitignore
# Session logs (volatile)
*.jsonl
*.jsonl.lock
*.jsonl.reset.*

# Databases (volatile)
*.sqlite
*.sqlite-journal

# Credentials (sensitive - NEVER commit)
credentials/
*.pem
*.key
*.token

# Temporary files
*.tmp
*.temp
.DS_Store

# Logs
logs/

# Delivery queue
delivery-queue/

# Python cache
__pycache__/
*.pyc
*.pyo

# Skill manager archive
.skill-manager/archive/
```

---

## Decision Tree

```
User requests sensitive operation
        ↓
    Is SAVE needed?
    ┌─────┴─────┐
   Yes          No
    ↓            ↓
 SAVE first   Execute directly
    ↓
[CHECK .gitignore]
    ↓
[SCAN for sensitive files]
    ↓
[CONFIRM if autonomous]
    ↓
Execute operation
    ↓
  Success?
  ┌─────┴─────┐
 Yes          No
  ↓            ↓
 Done      ROLLBACK?
           ┌─────┴─────┐
          Yes          No
           ↓            ↓
     [Try soft reset]  Debug manually
           ↓
      [Hard reset only if confirmed]
```

---

## Integration with Other Skills

| Skill | Integration | Restriction |
|-------|-------------|-------------|
| self-improvement | Record rollback events as learnings | ✅ Safe |
| skill-creator | Auto-SAVE before creating new skills | ⚠️ Require user confirmation |
| healthcheck | Check git status during health checks | ✅ Safe (read-only) |

**⚠️ Autonomous Operation Restrictions**:

When invoked autonomously (by other skills or automated triggers):
- **SAVE**: Require user confirmation unless explicitly whitelisted
- **ROLLBACK**: ALWAYS require user confirmation
- **Hard reset**: NEVER allowed autonomously

---

## Safety Guidelines

### ✅ Best Practices

1. **Always verify .gitignore before SAVE**
   ```bash
   test -f ~/.openclaw/.gitignore || echo "Create .gitignore first!"
   ```

2. **Scan for sensitive files before committing**
   ```bash
   git status --short | grep -E '\.(pem|key|token)$|credentials/'
   ```

3. **Use targeted add instead of -A when possible**
   ```bash
   git add workspace/SOUL.md workspace/AGENTS.md
   ```

4. **Prefer soft/mixed reset over hard reset**
   ```bash
   # Try this first
   git reset --soft HEAD~1
   ```

5. **Always confirm before hard reset**
   - Show what will be lost
   - Require explicit "yes" confirmation

6. **Use descriptive commit messages**
   ```
   checkpoint: before installing news skill
   checkpoint: before modifying SOUL.md persona
   checkpoint: before cron job changes
   ```

### ❌ Avoid

1. **Don't use git add -A blindly**
   - Check what will be staged first
   - Consider targeted paths instead

2. **Don't commit without checking .gitignore**
   - Sensitive files may be exposed
   - Verify exclusions are working

3. **Don't hard reset without confirmation**
   - Changes are permanently lost
   - No undo possible

4. **Don't allow autonomous hard resets**
   - Too risky for automated operations
   - Always require human confirmation

5. **Don't commit session data**
   - Session logs are excluded intentionally
   - Focus on configuration, not runtime data

---

## Quick Reference

| Action | Command | Safety | Alias |
|--------|---------|--------|-------|
| Verify .gitignore | `test -f ~/.openclaw/.gitignore` | ✅ Safe | `check-ignore` |
| Scan sensitive files | `git status \| grep -E '\.(pem\|key)$'` | ✅ Safe | `scan` |
| SAVE checkpoint | `git add -A && git commit -m "..."` | ⚠️ Check first | `save` |
| Soft ROLLBACK | `git reset --soft HEAD~1` | ✅ Safe | `rollback-soft` |
| Hard ROLLBACK | `git reset --hard HEAD~1` | 🔴 Destructive | `rollback-hard` |
| View history | `git log --oneline -10` | ✅ Safe | `history` |
| Check status | `git status` | ✅ Safe | `status` |
| Compare diff | `git diff HEAD` | ✅ Safe | `diff` |

---

## Example Session

```
User: Install a new skill from ClawHub

Agent (internal):
  1. Checking .gitignore... ✓ Found
  2. Scanning for sensitive files... ✓ None detected
  3. SAVE checkpoint first
     $ git add workspace/skills/
     $ git commit -m "checkpoint: before installing {skill-name}"
     ✓ Checkpoint: abc1234

  4. Install skill
     $ clawhub install {skill-name}
     
  5. Verify success
     ✓ Skill installed successfully
     
User: That skill broke something, rollback!

Agent:
  1. Recent commits:
     abc1234 checkpoint: before installing {skill-name}
     def5678 previous state
     
  2. Restore to abc1234?
  
  3. Uncommitted changes:
     M workspace/skills/new-skill/config.json
     
  4. ⚠️ Options:
     - Soft reset: Undo commit, keep changes (safe)
     - Hard reset: Delete commit + changes (destructive)
     
     Which do you prefer?
     
User: Hard reset

Agent:
  5. ⚠️ HARD RESET WARNING:
     This will permanently delete:
     - workspace/skills/new-skill/config.json
     
     This cannot be undone. Type "yes" to confirm.
     
User: yes

Agent:
  6. Executing hard reset...
     $ git reset --hard abc1234
     ✓ Rolled back successfully
```

---

_Last updated: 2026-03-07_
