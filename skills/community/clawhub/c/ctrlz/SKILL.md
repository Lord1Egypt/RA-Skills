---
name: ctrlz
description: AI Operation Undo System. When user executes /ctrlZ or says "undo last step", automatically revert all file modifications, installations, etc. from the recent conversation round. Default keeps 1 undo unit, configurable to 3 or 5.
---

# CtrlZ - AI Operation Undo System

## Overview

CtrlZ is a Git-like undo system that records all "create/update/delete" operations performed by AI in each conversation round, allowing users to revert with one command.

## Core Concepts

- **Undo Session**: All operations generated in one conversation round (user request + assistant response)
- **Stack Mechanism**: Default keeps 1 session, configurable to 3/5 sessions
- **Auto Recording**: Automatically backup and record before executing any modifications

## Usage

### User Commands

```
/ctrlZ              # Undo the most recent conversation round
/ctrlZ 3            # Undo the last 3 conversation rounds
/ctrlZ list         # List undoable operation records
/ctrlZ stack 5      # Set stack size to 5 undo units
```

### Natural Language Triggers

- "undo last step"
- "undo"
- "revert recent changes"
- "ctrl+z"

## AI Usage Guide (Important)

### Before each file modification:

**1. Start Session (at conversation beginning)**
```bash
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh start <session_key> "<description>"
```

**2. Record each operation (before modification)**
```bash
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh record <session_id> <type> <path> [metadata]
```

Operation types:
- `file_write` - Write/overwrite file
- `file_edit` - Edit existing file
- `file_delete` - Delete file
- `dir_create` - Create directory
- `exec_install` - Install package/dependency
- `exec_download` - Download file

**3. Execute actual operation**

**4. End Session (automatic at conversation end)**

### Complete Example

```bash
# 1. Start session
SESSION=$(bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh start "Modify config" | jq -r '.session_id')

# 2. Record config.json modification
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh record $SESSION file_edit "/path/to/config.json"

# 3. Execute actual modification
edit /path/to/config.json ...

# 4. Record package installation
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh record $SESSION exec_install "npm:lodash"

# 5. Execute installation
exec "npm install lodash"
```

## Execute Undo

When user says "undo":

```bash
# Undo the most recent 1 session
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh undo

# Undo the last 3 sessions
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh undo 3
```

## Configuration

### View current stack size
```bash
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh get-stack
```

### Modify stack size (how many undo units to keep)
```bash
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh set-stack 5
```

### View statistics
```bash
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh stats
```

### List undoable operations
```bash
bash ~/.openclaw/skills/ctrlz/scripts/ctrlz.sh list
```

## Database Structure

**Location**: `~/.openclaw/skills/ctrlz/undo.db`

**Tables**:
- `undo_sessions` - Each undo unit (conversation round)
- `undo_operations` - Specific operation records
- `settings` - Configuration (stack size, etc.)

**Backup Location**: `~/.openclaw/skills/ctrlz/backups/`

## Important Notes

1. **Package installation cannot be fully auto-undone** - Will show list and manual removal commands
2. **External command effects** - Cannot track side effects of shell commands
3. **Backup space** - Clean up old backups periodically: `ctrlz clear`

## Package Installation Handling

When undoing operations that include package installations:

```
📦 The following package installations cannot be auto-undone:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. npm:lodash
  2. npm:express
  3. pip:requests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 To remove, manually execute:
   npm uninstall lodash
   npm uninstall express
   pip uninstall requests
```

## System Integration

Recommended to auto-start session at conversation begin and auto-cleanup at end. Can add logic to SOUL.md or AGENTS.md.

## Testing

```bash
# Quick demo
bash ~/.openclaw/skills/ctrlz/scripts/demo.sh

# Or run full test cases
bash ~/.openclaw/skills/ctrlz/scripts/test_ctrlz.sh
```
