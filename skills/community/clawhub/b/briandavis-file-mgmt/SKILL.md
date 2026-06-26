# File Management Skill

_A battle-tested approach to keeping your AI agent workspace organized and maintainable._

## Overview

This skill documents the file management system developed through real-world use of OpenClaw. It covers workspace structure, naming conventions, dead file detection, and cleanup practices.

## When to Use This Skill

- Onboarding a new agent or setting up a fresh workspace
- Performing periodic workspace audits
- Before making significant changes to workspace structure
- When workspace feels cluttered or disorganized

## Core Principles

### 1. Every File Has a Purpose
- **Active files**: Scripts, configs, and data in use by cron jobs or agents
- **Reference files**: Documentation, strategies, and notes
- **Archived files**: Old versions, completed project artifacts
- **Dead files**: Abandoned scripts, old experiments, unused utilities

### 2. Structure Mirrors Function
```
workspace/
├── memory/          # Daily session logs and working context
├── skills/           # Installed skill directories
├── project-1/        # Project-specific directories
├── project-2/
├── ACTIVE.md         # Currently running projects & priorities
├── DREAMS.md         # Background processing notes
└── ARCHIVED/         # Completed or abandoned projects
```

### 3. Naming Conventions
- **Scripts**: Use `.sh` for bash, `.py` for Python, `.js` for JavaScript
- **Logs**: End with `.log`
- **Configs**: End with `.json`, `.yaml`, or `.md`
- **Daily notes**: `memory/YYYY-MM-DD.md` format

### 4. Audit Regularly
Run workspace audits monthly or after major changes. Use the audit script to identify:
- Dead files (no references from active crons or scripts)
- Large files consuming storage
- Outdated documentation

## Quick Audit Commands

```bash
# Find files not referenced by any cron or script
grep -r "filename" ~/path/to/workspace/ --include="*.sh" --include="*.py" --include="*.js"

# Find recently modified files
find ~/path/to/workspace -type f -mtime -7

# Check disk usage by directory
du -sh ~/path/to/workspace/*/
```

## Cleanup Best Practices

1. **Never delete immediately** — use `trash` instead of `rm`
2. **Document before deleting** — note what a file did in memory first
3. **Verify before cleanup** — confirm no active references
4. **Commit before major cleanup** — create a revert point

## Full Documentation

See `FILE-MANAGEMENT.md` for the complete reference implementation, including:
- Directory structure explainer
- Active vs archived file definitions
- Dead file detection criteria
- Example cleanup checklists
