# Intermediate Patterns

These patterns harden an agent that already has the basics and now needs to survive recurring operational use.

## 6. Agent Verification Rules

**Failure mode:** The agent reports numbers that were never actually measured.

**Pattern:** No command, no number.

```markdown
### Verification Rule
For every metric you report, include the command you ran.
No command = no number. Never estimate from memory.

✅ "Disk: 868 MB (`du -sh ~/.openclaw | cut -f1`)"
❌ "Disk: ~800 MB"
```

## 7. Working Buffer (Compaction Survival)

**Failure mode:** A long session compacts and the last stretch of important context disappears.

**Pattern:** Use a small buffer file that survives compaction.

```markdown
## Create: memory/working-buffer.md
# Working Buffer — Status: INACTIVE

## Add to SOUL.md:
### Working Buffer
When context is getting long:
1. Append key exchanges to memory/working-buffer.md
2. After compaction: read buffer FIRST, extract context, then clear
```

Suggested thresholds:

| Context % | Action |
|-----------|--------|
| < 70% | Normal |
| 70-84% | Activate buffer |
| 85-94% | Emergency checkpoint |
| 95%+ | Survival mode — save essentials, suggest new session |

### How to estimate context usage

Most agent frameworks do not expose a precise "context %" meter. Practical proxies:
- **Message count:** If the conversation is 30+ exchanges deep, assume 70%+
- **Tool call count:** 15+ tool calls in a session usually means 60-80% context consumed
- **OpenClaw:** Check `/compact` status or compaction warnings in the session log
- **Claude Code:** The status bar shows token usage; watch for the yellow/red zone
- **Rule of thumb:** If you are thinking "this session is getting long" — activate the buffer.
  False positives are cheap; lost context is expensive.

## 8. QA Gates

**Failure mode:** A deliverable reaches a human with the wrong date, broken links, or leaked internal context.

**Pattern:** Match review intensity to output risk.

```markdown
### Gate 0: Verify mechanism changed, not just text
### Gate 1: Internal (workspace files) — auto-pass, lowest risk
### Gate 2: Human-facing (briefings, summaries)
  - Concise, structured, actionable, accurate, scannable in 30 sec
### Gate 3: External (emails, posts, client materials)
  - Gate 2 + recipient-appropriate tone, no internal context leaked,
    no private data, links verified, proofread
```

## 9. Decision Reasoning Logs

**Failure mode:** A non-obvious choice is made, then nobody knows why in the next session.

**Pattern:** Log reasoning when the choice matters.

```markdown
### 🧠 Decision: [what you decided]
- **Context:** [situation]
- **Options:** [what you considered]
- **Chose:** [what and why]
- **Rejected:** [what and why not]

Log when: escalating, choosing tools/agents, suppressing alerts, acting vs asking.
Skip: routine acks, obvious tool choices.
```

## 10. Verify Implementation, Not Intent

**Failure mode:** The agent changes wording and declares success, but the mechanism never changed.

**Pattern:** Verify the real architecture or behavior.

```markdown
### Verify Implementation, Not Intent
1. Identify the architectural components (not just text/config)
2. Change the actual mechanism (not just prompt wording)
3. Verify by observing behavior, not reading config

❌ Changed prompt "check X" to "ALWAYS check X" → still just a prompt
✅ Changed cron type from systemEvent to isolated agentTurn → architectural
```
