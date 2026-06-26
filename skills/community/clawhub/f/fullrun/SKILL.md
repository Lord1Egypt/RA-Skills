---
name: fullrun
description: Automatically execute tasks from checklist.md with state management and scheduled checking
trigger: When user says "start execution", "run tasks", "execute checklist" or similar commands
---

# Fullrun Skill

## Overview

This skill implements a task execution system with the following features:

1. **State Management**: Uses `.claude-status.txt` file to track execution state
   - `0` = Idle, ready to execute (or file doesn't exist)
   - `1` = Claude is currently executing tasks
   - `2` = All tasks completed, monitoring should exit

2. **Task List**: Reads pending tasks from `checklist.md`

3. **Scripts**: Executable scripts in the `scripts/` directory

## Requirements

- **jq** - Required for install/uninstall scripts
  - macOS: `brew install jq`
  - Linux: `apt install jq` or `yum install jq`

## File Structure

```
project/
├── SKILL.md                  # This skill definition file
├── checklist.md              # Task list file (create in your project)
├── .claude-status.txt        # Execution state file (auto-generated)
├── .fullrun.log              # Execution log (auto-generated)
├── .monitor.pid              # Monitor process PID (auto-generated)
├── .claude/
│   └── fullrun/
│       └── scripts/          # Installed scripts (auto-generated)
│           ├── main.sh       # Main entry point
│           ├── fullrun.sh    # Task execution script
│           └── cron-manager.sh # Cron job management script
└── scripts/
    ├── main.sh               # Main entry point (source)
    ├── fullrun.sh            # Task execution script (source)
    ├── cron-manager.sh       # Cron job management script (source)
    ├── install.sh            # Installation script
    └── uninstall.sh          # Uninstallation script
```

## Usage

### Installation (run once per project)

The installer creates project-local configuration in `./.claude/` - no global settings are modified.

```bash
# In your project directory, run:
./scripts/install.sh
```

**What the installer does:**
1. Creates `.claude/` directory in your project
2. Copies scripts to `.claude/fullrun/scripts/`
3. Creates or updates `.claude/settings.local.json` with:
   - Permission rule for project scripts
   - SessionStart hook for auto-monitoring

**Scope:** Configuration is project-local only. Other projects are not affected.

### Uninstall

```bash
./scripts/uninstall.sh
```

This removes:
- The `.claude/fullrun/` directory
- Fullrun permission rule from `.claude/settings.local.json`
- Fullrun hook from SessionStart (preserves other hooks)
- `.claude/settings.local.json` if it becomes empty

### Start scheduled monitoring (recommended)
```bash
./.claude/fullrun/scripts/main.sh start
```

### Manually execute tasks
```bash
./.claude/fullrun/scripts/main.sh run
```

### Check status
```bash
./.claude/fullrun/scripts/main.sh status
```

### Stop monitoring
```bash
./.claude/fullrun/scripts/main.sh stop
```

## Execution Rules

1. If `.claude-status.txt` does not exist or contains `0`, start executing unfinished tasks from `checklist.md`
2. When executing tasks, set `.claude-status.txt` to `1`
3. When all tasks are completed, set `.claude-status.txt` to `2`
4. Scheduled task checks every 1 minute:
   - If status = `0` or file doesn't exist + pending tasks = start execution
   - If status = `1` = Claude is running, continue waiting
   - If status = `2` = All tasks completed, exit monitoring
5. Monitoring automatically exits when all tasks are completed (status=2)

## Task Marking Format

In `checklist.md`, tasks use the following format:
- `[ ]` indicates incomplete
- `[x]` indicates completed

Example:
```markdown
# Checklist

- [ ] Task 1: Complete a feature
- [ ] Task 2: Write tests
- [x] Task 3: Completed task
```

## Notes

- Scheduled monitoring is session-level, stops when the current terminal session ends
- For persistent monitoring, use system cron or launchd
- The SessionStart hook checks for `checklist.md` in the current working directory at runtime
- Configuration is project-local via `.claude/settings.local.json`

## Security Notes

**What this skill accesses:**
- Reads `checklist.md` in your current project directory
- Creates/reads `.claude-status.txt` in your current project directory
- Writes execution log to `.fullrun.log`
- Does NOT access the internet
- Does NOT request or transmit credentials

**What the installer modifies:**
- `.claude/settings.local.json` - Project-local settings (gitignored)
- `.claude/fullrun/scripts/` - Project-local scripts

**Persistence:**
- The SessionStart hook runs at the start of each Claude Code session in this project
- It only starts monitoring if `checklist.md` exists and no execution is in progress
- Uninstall removes all modifications in the project

## How Task Execution Works

1. The shell scripts (`fullrun.sh`, `cron-manager.sh`) handle:
   - State management (`.claude-status.txt`)
   - Task queue management (reading `checklist.md`)
   - Logging (`.fullrun.log`)
   - Marking tasks as complete

2. **Task execution is delegated to Claude Code**:
   - When a task is started, it outputs the task description
   - Claude Code reads the task and executes the appropriate commands
   - This design allows for complex, multi-step tasks that require AI reasoning

## Cross-Platform Compatibility

- **macOS**: Fully supported
- **Linux**: Fully supported
- **Windows**: Requires WSL or Git Bash

The scripts use `awk` for text processing to ensure consistent behavior across all platforms.
