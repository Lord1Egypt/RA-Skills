---
name: context-optimizer
description: Context-aware session manager that monitors token usage and automatically extracts key information to create continuation sessions when approaching context limits. Use when: (1) User wants automatic context management, (2) Long-running tasks approach 200k token limit, (3) Need to split large tasks across multiple sessions, (4) Want to preserve continuity when context nears exhaustion.
---

# Context Optimizer

Automatic context management skill that monitors token usage and creates continuation sessions when needed.

## Core Functionality

This skill provides:

1. **Context Monitoring** - Track token usage against 200k max
2. **Threshold Detection** - Trigger at 95% (190k tokens)
3. **Information Extraction** - Extract key decisions, important context, unfinished tasks
4. **Session Continuation** - Create new session with summarized context

## Usage

### Manual Trigger

```bash
# Check current context usage
context-optimizer check

# Force extraction and create continuation
context-optimizer split --threshold 95

# Preview what would be extracted
context-optimizer preview
```

### Automatic Monitoring

Add to your workflow or cron:

```
Every 10 minutes: Run context-optimizer check
```

When context exceeds threshold, the skill will:
1. Analyze conversation history
2. Extract key information (decisions, context, todos)
3. Generate continuation prompt
4. Create new session with extracted context

## Extraction Priority

The optimizer extracts in this order:

1. **Unfinished tasks** - Incomplete actions, pending decisions
2. **Key decisions** - Important choices and their rationale
3. **Critical context** - Information essential to task completion
4. **User preferences** - Explicitly stated preferences and requirements
5. **Recent progress** - What has been accomplished so far

## Output Format

When creating continuation, output:

```markdown
# Session Continuation

## Completed
- [list of finished items]

## In Progress
- [current work items]

## Key Context
- [essential information to preserve]

## Next Steps
- [suggested next actions]

---

## Continuation Prompt
[Prompt to use in new session]
```

## Scripts

- `context_optimizer.py` - Main CLI for context monitoring and splitting
- `session_extractor.py` - Extracts key information from session history

## Integration with OpenClaw

### Automatic Split Logic

To automatically split sessions when context exceeds 95%, integrate with OpenClaw's heartbeat:

1. **Add to HEARTBEAT.md:**
```markdown
## Context Monitor
Every heartbeat: Check session_status
If context > 85%: Log warning
If context > 95%: Run context-optimizer split
```

2. **Create Cron Job:**
Use cron with `sessionTarget: "isolated"` to run context checks independently.

### Tool Integration

The skill uses these OpenClaw tools:
- `session_status` - Get current token/context usage
- `sessions_history` - Fetch conversation for extraction  
- `sessions_spawn` - Create continuation session
- `cron` - Schedule periodic checks
