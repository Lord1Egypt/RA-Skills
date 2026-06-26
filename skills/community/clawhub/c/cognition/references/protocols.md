# Cognition — Protocol Blocks for AGENTS.md

Copy-paste these into your AGENTS.md.

---

## Memory Protocol

```markdown
## Memory Protocol
- Before answering questions about past work: search memory first
- Before starting non-trivial work: check today's daily log and relevant durable files
- When you learn something important: write it to the appropriate file immediately
- When corrected on a mistake: update the durable record and log the lesson
- When context is getting large or a session is ending: summarize to `memory/YYYY-MM-DD.md`

### Importance Tagging
Tag significant moments in daily logs for consolidation priority:
- `[REPLAY_PRIORITY: HIGH]` — corrections, policy changes, explicit decisions, new procedures
- `[REPLAY_PRIORITY: MEDIUM]` — new facts, project milestones, config changes
- default / low — routine operations

### Broadcast Note
Treat broadcast as a protocol, not a separate subsystem:
- new preference → durable knowledge (`MEMORY.md` or `memory/bank/*.md`)
- new commitment → `memory/FUTURE_INTENTS.md`
- novel solution → `memory/procedures/`
- correction → fix the durable record + note the lesson
- failed retrieval → `memory/meta/gap_tracker.json`
```

---

## Retrieval Protocol

```markdown
## Retrieval Protocol
Before doing non-trivial work:
1. Search for the topic in memory first
2. Follow links from `memory/bank/cross-references.md` if you use the cross-reference overlay
3. Load the specific file or chunk you need
4. If retrieval fails, log the miss in `memory/meta/gap_tracker.json`
5. Then proceed with the task
```

---

## Procedure Promotion Note

```markdown
### Procedure Maturity States
- New procedures start as `draft`
- Promote to `reviewed` after human review or 3 successful executions
- Promote to `trusted` only after repeated reliable use with no unresolved caveats
```
