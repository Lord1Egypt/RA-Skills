# Context Auto-Split - Automatic continuation when context exceeds 95%

## Current Context Status

```
Context: {context_used}/{max_context} ({percentage}%)
```

## Trigger Condition

When context > 190,000 tokens (95% of 200k):

## Automatic Extraction Process

### Step 1: Analyze Current Session

1. Get full session history: `sessions_history(limit: 100)`
2. Get session status: `session_status`

### Step 2: Extract Key Information

Extract in priority order:

1. **Unfinished Tasks** - Search for TODO, FIXME, pending, in progress
2. **Key Decisions** - "decided to", "chose to", "going with"
3. **Critical Context** - Config, errors, important URLs
4. **User Preferences** - "prefer", "like", "want", "need"
5. **File Paths** - Working files, recent edits

### Step 3: Generate Continuation Prompt

```markdown
# Session Continuation

## Completed
- [what was finished]

## In Progress  
- [current work]

## Key Decisions
- [important choices made]

## Important Files
- [files being worked on]

## Continuation
[What to do next]
```

### Step 4: Create New Session

Use `sessions_spawn` with:
- `task`: The continuation prompt
- `mode`: "run" for one-shot or "session" for persistent
- `runtime`: "subagent" or "acp"

## Manual Commands

- `context-optimizer check` - Check current usage
- `context-optimizer split` - Force split at threshold
- `context-optimizer preview` - Preview extraction

## Example: Heartbeat Integration

In HEARTBEAT.md:

```markdown
## Context Check
1. Run: session_status
2. If context > 85%: Note warning
3. If context > 95%: Trigger split
```

## Example: Cron Job

```json
{
  "name": "context-monitor",
  "schedule": {"kind": "every", "everyMs": 600000},
  "payload": {
    "kind": "agentTurn",
    "message": "Run context-optimizer check. If context > 95%, extract and create continuation session."
  },
  "sessionTarget": "isolated"
}
```
