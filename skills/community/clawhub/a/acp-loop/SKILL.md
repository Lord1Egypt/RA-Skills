---
name: acp-loop
description: Schedule recurring AI agent prompts using intervals or cron expressions. Use when users need to run prompts periodically, automate agent tasks on a schedule, or set up recurring workflows. Triggers on "schedule prompt", "run every", "cron", "recurring", "periodic", "interval", "loop prompt".
---

# acp-loop: Recurring Prompt Scheduler

Schedule AI agent prompts to run at intervals or cron schedules.

## When to Use This Skill

Use this skill when the user:

- Wants to run a prompt repeatedly at fixed intervals
- Needs cron-style scheduling for agent tasks
- Wants to automate recurring AI workflows
- Asks about scheduling, looping, or periodic execution of prompts

## Installation

```bash
npm install -g acp-loop
```

## Quick Start

### Interval Mode

Run prompts at fixed intervals:

```bash
# Every 5 minutes
acp-loop --interval 5m "check logs for errors"

# Every 30 seconds, stop after 10 iterations
acp-loop --interval 30s --max 10 "quick health check"

# Every hour, timeout after 8 hours
acp-loop --interval 1h --timeout 8h "hourly report"
```

### Cron Mode

Run prompts on cron schedules:

```bash
# Daily at 3am
acp-loop --cron "0 3 * * *" "nightly cleanup"

# Every Monday at 9am
acp-loop --cron "0 9 * * 1" "weekly standup summary"

# Every 5 minutes (cron style)
acp-loop --cron "*/5 * * * *" "monitor status"
```

## Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `--interval <duration>` | Fixed interval (30s, 5m, 1h) | `--interval 5m` |
| `--cron <expression>` | Cron expression | `--cron "0 9 * * *"` |
| `--agent <name>` | Agent to use (default: codex) | `--agent claude` |
| `--max <n>` | Max iterations | `--max 10` |
| `--timeout <duration>` | Max total runtime | `--timeout 2h` |
| `--until <string>` | Stop when output contains | `--until "DONE"` |
| `--quiet` | Minimal output | `--quiet` |

## Common Patterns

### Conditional Stop

```bash
# Run until task reports completion
acp-loop --interval 1m --until "All tests passed" "run test suite"
```

### Limited Runs

```bash
# Run exactly 5 times
acp-loop --interval 10s --max 5 "check deployment status"
```

### Time-Boxed Execution

```bash
# Run for max 1 hour
acp-loop --interval 5m --timeout 1h "monitor build"
```

### Daily Scheduled Task

```bash
# Every day at midnight
acp-loop --cron "0 0 * * *" "generate daily report"
```

### Using Different Agents

```bash
# Use Claude instead of Codex
acp-loop --interval 10m --agent claude "review code changes"

# Use Gemini CLI
acp-loop --interval 5m --agent gemini-cli "check status"
```

## Important Notes

1. **Mutually exclusive**: Use either `--interval` OR `--cron`, not both
2. **Cron library**: Uses `croner` (handles laptop sleep/wake better than node-cron)
3. **Stop**: Press Ctrl+C to stop the loop
4. **Agent support**: Works with any ACP-compatible agent (codex, claude, gemini-cli)

## Why acp-loop?

- Claude Code's built-in `/loop` command has bugs
- Works with any ACP-compatible agent, not just Claude
- Proper cron expression support
- Better handling of laptop sleep/wake cycles

## Resources

- GitHub: https://github.com/femto/acp-loop
- npm: https://www.npmjs.com/package/acp-loop
