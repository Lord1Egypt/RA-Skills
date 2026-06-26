# Context Optimizer Cron Template

Use this template to set up automatic context monitoring.

## Option 1: Heartbeat-based Monitoring (Recommended)

Add to `HEARTBEAT.md`:

```markdown
# Heartbeat Tasks

## Context Check (every heartbeat)
Run: Check if context usage exceeds 85%

When triggered:
1. Get session status via session_status
2. Parse context percentage
3. If > 85%, log warning
4. If > 95%, prepare for session split
```

## Option 2: Cron Job

Create a cron job to check context every 10 minutes:

```bash
# Context monitor cron job
# Runs every 10 minutes
```

See the main SKILL.md for the complete workflow.

## Context Usage Warning Signs

- Token count approaching 170k (85%)
- Increasing frequency of "summarizing" or "compactions"
- Slower response times

## Before Continuation

When creating a new session:
1. Extract all unfinished tasks
2. Note key decisions made
3. List important files being worked on
4. Summarize recent progress
5. Create new session with continuation prompt
