# Fullrun - Task Executor

A script system that automatically executes task checklists with state management and scheduled checking.

## Requirements

- **jq** - Required for install/uninstall scripts
  - macOS: `brew install jq`
  - Linux: `apt install jq` or `yum install jq`

## Quick Start

```bash
# Install in project (run once per project)
./scripts/install.sh

# Start scheduled monitoring (recommended)
./.claude/fullrun/scripts/main.sh start

# Check status
./.claude/fullrun/scripts/main.sh status

# Manually execute tasks
./.claude/fullrun/scripts/main.sh run

# Stop monitoring
./.claude/fullrun/scripts/main.sh stop

# Uninstall
./scripts/uninstall.sh
```

## How It Works

1. System reads tasks from `checklist.md`
2. Checks `.claude-status.txt` to determine if execution is in progress
3. If there are pending tasks and currently idle, starts execution
4. Automatically checks every minute for resume capability
5. Task execution is delegated to Claude Code for intelligent task handling

## Task File Format

Edit `checklist.md` to add your tasks:

```markdown
# Checklist

- [ ] Task 1: Description
- [ ] Task 2: Description
```

The system automatically marks completed tasks as `[x]`.

## Files

| File | Description |
|------|-------------|
| `checklist.md` | Task list |
| `.claude-status.txt` | Execution state (0=idle, 1=running, 2=completed) |
| `.fullrun.log` | Execution log |
| `.claude/settings.local.json` | Project-local Claude configuration |
| `.claude/fullrun/scripts/` | Installed scripts |
| `scripts/main.sh` | Main entry script |

## Use Cases

- Automated build/test task execution
- Resume-capable batch processing
- Scheduled tasks with state recovery
- CI/CD pipeline task management

## Cross-Platform Support

- macOS: Fully supported
- Linux: Fully supported
- Windows: Requires WSL or Git Bash
