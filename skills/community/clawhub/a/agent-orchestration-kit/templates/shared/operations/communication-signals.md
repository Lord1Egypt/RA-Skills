# Communication Signals — Quick Reference

_Runtime copy. Full documentation: see skill's `references/signals.md`._

## Task Signals

| Signal | Meaning |
|--------|---------|
| `[READY]` | Complete and confident |
| `[NEEDS_INFO]` | Needs more context |
| `[BLOCKED]` | Cannot proceed |
| `[LOW_CONFIDENCE]` | Delivered but uncertain |
| `[SCOPE_FLAG]` | Task bigger than expected |

## Approval Signals

| Signal | Meaning |
|--------|---------|
| `[APPROVE]` | Reviewer approves |
| `[REVISE]` | Reviewer requests changes |
| `[PENDING APPROVAL]` | Awaiting owner approval |

## Session Signal

| Signal | Meaning |
|--------|---------|
| `[CONTEXT_LOST]` | Session compacted, needs re-briefing |

## Callback Format

```
[TASK_CALLBACK:T-{id}]
agent: {agent_id}
signal: {signal}
output: {result summary}
files: {paths}
```

## Rules

- One primary signal per callback, at the top
- Signals are for Leader consumption — they drive routing decisions
- Owner delivery = `message` tool send/edit, not raw callbacks
