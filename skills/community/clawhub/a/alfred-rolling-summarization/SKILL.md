# Auto-Summarization Skill

Proactive context management to prevent overflow and improve session quality.

## Problem
- OpenClaw compaction triggers on context overflow (reactive)
- Compaction timeout (60s internal) causes fallback to pre-compaction state
- Tool loops (research with web_fetch) generate massive context without stopping
- No control over WHAT is preserved during compaction

## Solution: Rolling Summarization

### How It Works
Every N turns, create a concise summary of recent work and update SESSION-STATE.md. This keeps the session lean while preserving important context.

### Trigger Thresholds
| Condition | Action |
|-----------|--------|
| Every 15 turns | Create rolling summary |
| After 10 consecutive tool calls | Force summary (tool loop guard) |
| Context >70% estimated | Proactive summary + flush to memory |

### Rolling Summary Format
Update SESSION-STATE.md with a condensed view:

```markdown
## Rolling Summary (as of HH:MM)
- Completed: [what was done]
- In progress: [what's being worked on]
- Decisions: [key decisions made]
- Blockers: [anything blocking]
- Next: [what to do next]
```

### Integration with Existing Stack
1. **Hindsight auto-retain** captures important facts before summary
2. **SESSION-STATE.md** stores the rolling summary (always in context via bootstrap)
3. **Daily notes** get the detailed version at end of session
4. **Working buffer** becomes unnecessary if rolling summary works well

### Anti-Patterns
- ❌ Don't summarize every turn (adds latency, wastes LLM calls)
- ❌ Don't duplicate Hindsight content (it already retains facts)
- ❌ Don't include routine operations (heartbeat checks, status pings)
- ✅ DO summarize: decisions, blockers, task progress, user preferences
- ✅ DO keep it under 200 chars per section

### Prompt Addition (add to agents that need it)
```
After completing a task or every 15 turns:
1. Read SESSION-STATE.md
2. Update the Rolling Summary section with current state
3. Keep it concise (under 500 chars total)
4. This prevents context overflow and preserves continuity
```

## Metrics
| Metric | Before | After (target) |
|--------|--------|----------------|
| Context overflow/week | 1-2 | ~0 |
| Compaction timeout rate | ~50% | <20% |
| Context lost per session | High | Low |
| Additional LLM cost | $0 | ~$0.02/week |

## Version
1.0.0 — Initial implementation
