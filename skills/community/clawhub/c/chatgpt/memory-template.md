# Memory Template - ChatGPT

Create `~/chatgpt/memory.md` with this structure:

```markdown
# ChatGPT Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Workflow Defaults
<!-- Preferred surfaces: standard chat, Temporary Chat, Projects, GPTs -->
<!-- Preferred prompt packet size, draft depth, and revision style -->

## Privacy Boundaries
<!-- Data categories that should avoid remembered chats or uploads -->
<!-- Rules for when to prefer Temporary Chat -->

## Active Patterns
<!-- Prompt packet shapes, QA checklists, and pass order that work repeatedly -->
<!-- Durable custom instruction patterns that are actually helpful -->

## Failure Modes
<!-- Repeated problems: too generic, ignores constraints, stale context, hallucinations -->
<!-- Best fixes that worked -->

## Notes
<!-- Stable observations worth reusing -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Default learning state | Keep refining ChatGPT workflow defaults from active use |
| `complete` | Stable workflow established | Reuse defaults unless the user changes them |
| `paused` | User wants fewer setup questions | Ask only when a critical ChatGPT choice is missing |
| `never_ask` | User rejected setup prompts | Stop prompting and work from the task only |

## Integration Values

| Value | Meaning |
|-------|---------|
| `pending` | Activation preference not confirmed |
| `done` | Activation preference confirmed |
| `declined` | User wants manual activation only |

## Key Principles

- Store only patterns that improve future ChatGPT sessions.
- Keep notes operational and short.
- Save workflow boundaries, not raw user content.
- Update `last` whenever memory changes.
