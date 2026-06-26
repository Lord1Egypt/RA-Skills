---
name: context-cleaner
description: "Automatically compress large contexts and clean up expired sessions, sub-agents, and temporary files."
---

# Context Cleaner Skill

Automatically manage session context size by compressing large contexts and cleaning up expired sessions, sub-agents, and temporary files.

## Quick Reference

| Situation | Action |
|-----------|------|
| Session exceeds size limit | Compress early messages |
| Sub-agent idle > 30min | Terminate automatically |
| Old sessions (> 7 days) | Archive or delete |
| Large context (> 10K tokens) | Summarize and compress |

## Setup

No special setup required. The skill automatically:

1. **Monitors session sizes** - Checks if current session context is growing too large
2. **Terminates idle sub-agents** - Stops sub-agents that haven't been used recently
3. **Archives old sessions** - Moves completed sessions to archive
4. **Compresses context** - Replaces verbose message chains with summaries

## Usage

### Automatic Operation

The skill runs automatically during heartbeat checks when context size exceeds thresholds.

### Manual Trigger

Request cleanup anytime:

```
"Clean up context now"
"Remove expired sessions"
"Compress my context"
```

### API Call

Use `sessions_list` and `subagents` tools internally. The skill orchestrates:

1. List all sessions
2. Check sub-agent status
3. Terminate idle sub-agents
4. Compress large contexts
5. Archive old sessions

## Operation Logic

### Context Compression

When a session's context exceeds thresholds:

1. **Identify compressible regions** - Early messages, completed task steps
2. **Generate summaries** - Create concise summaries of message chains
3. **Replace verbose content** - Keep only essential information
4. **Preserve key context** - Maintain user preferences, decisions, ongoing tasks

### Session Cleanup

Expired session criteria:

- **Idle time**: No activity for 7+ days
- **Completed tasks**: Sessions that finished long ago
- **Orphaned sessions**: No associated work

### Sub-Agent Management

Termination criteria:

- **Idle**: No messages sent/received for 30+ minutes
- **Failed tasks**: Sub-agents that encountered repeated errors
- **Manual request**: User explicitly requests cleanup

## Best Practices

1. **Preserve working sessions** - Never clean active sessions
2. **Keep recent history** - Maintain last 24-48 hours of messages
3. **Archive not delete** - Move to archive before deleting
4. **Respect user context** - Don't clean sessions with pending tasks
5. **Notify before major cleanup** - Warn before deleting important sessions

## Integration Points

### Heartbeat Integration

Add to `HEARTBEAT.md`:

```markdown
## 上下文管理
- [ ] 检查会话大小
- [ ] 清理过期子代理
- [ ] 压缩过大上下文
```

### Cron Integration

Schedule regular cleanup:

```bash
# Weekly full cleanup
cron add -name "weekly-context-clean" -schedule "0 3 * * 0" -payload "Compress contexts and clean expired sessions"
```

## Compression Strategies

### Message Chaining

Convert:
```
User: Ask question
Model: Answer with detailed explanation
User: Follow-up
Model: More details
```

To:
```
User: Ask question
Model: ✅ Answered with 4-point explanation
User: Follow-up
Model: Continued discussion
```

### Context Summarization

Summarize long conversation threads:

- **Key decisions**: User preferences, important conclusions
- **Task progress**: Completed items, pending actions
- **Context notes**: Relevant background information

### Session Archiving

Archive strategy:

1. **Check completion status** - Is session finished?
2. **Verify no active work** - No pending tasks
3. **Check age** - Created more than 7 days ago?
4. **Move to archive** - Session archive directory
5. **Update metadata** - Record completion details

## File Structure

```
workspace/
├── .archive/          # Archived sessions
│   ├── 2026-04/
│   │   ├── session-uuid-1/
│   │   └── session-uuid-2/
│   └── 2026-05/
├── .cache/            # Temporary compression data
└── .cleanup/          # Cleanup logs and reports
    └── cleanup-report.md
```

## Safety Checks

Before any cleanup operation:

1. **Verify session status** - Not actively being used
2. **Check pending tasks** - No incomplete operations
3. **User preferences** - Respect "keep forever" flags
4. **Recent activity** - Last message within threshold
5. **Archive option** - Offer archive before delete

## Example Outputs

### Cleanup Report

```markdown
## Context Cleanup Report

**Time**: 2026-04-17 10:43
**Operations**:
- ✅ Compressed 3 large contexts (saved 15K tokens)
- ✅ Terminated 2 idle sub-agents
- ✅ Archived 1 old session (30 days)
- ⚠️ Skipped 1 active session (pending task)

**Impact**:
- Context size: Reduced by 25%
- Free tokens: ~50K available
- Active sessions: 5 (unchanged)
```

## Related Skills

- **self-improvement**: Log learnings about context management
- **taskflow**: Manage multi-step cleanup tasks
- **memory**: Keep important context in long-term memory

---

**Note**: This skill works alongside existing OpenClaw tools without requiring special permissions.
