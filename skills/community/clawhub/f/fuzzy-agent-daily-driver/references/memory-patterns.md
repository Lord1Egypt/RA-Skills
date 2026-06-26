# Memory Patterns — How to Remember Everything

## The Two-Tier Memory System

OpenClaw agents have no persistent memory between sessions. Files are the only continuity.

### Tier 1: Daily Notes (`memory/YYYY-MM-DD.md`)
Raw log of what happened today. Create automatically at session start if missing.

```markdown
# YYYY-MM-DD

## Session: Morning setup

### What happened
- Fixed the gateway auth issue
- Published two skills to ClawHub

### Decisions made
- Using Tailscale for peer agent collaboration
- HeartMuLa for local music generation

### Follow-ups
- [ ] Check PyTorch CUDA install tomorrow
- [ ] Review ghostty DND schedule
```

### Tier 2: MEMORY.md — Curated Long-Term Memory
Distilled from daily notes. Only in **main session** (direct chat). Never load in group chats.

```markdown
## Key Decisions
- Tailscale VPN for peer collaboration (no VPS needed)
- Python 3.11.9 for PyTorch CUDA compatibility

## People & Preferences
- User: South Africa (GMT+2), prefers concise replies
- Discord for urgent comms, webchat for detailed work

## Projects
- 90-day skill challenge: Day 2, 4 skills published
- HeartMuLa setup: CUDA working, STT server on port 8899
```

---

## Memory Recall Flow

```
Session Start
    │
    ▼
memory_search({ query: "what was I working on last?" })
    │
    ├─ Low confidence → memory_get(MEMORY.md) + recent daily notes
    │
    └─ High confidence → Pull relevant lines, continue where you left off
```

---

## When to Update Memory

| Situation | File to Update |
|-----------|---------------|
| Made a decision | `memory/YYYY-MM-DD.md` + distill to `MEMORY.md` |
| Learned something new | `memory/YYYY-MM-DD.md` |
| Completed a project milestone | `MEMORY.md` |
| User mentioned a preference | `USER.md` + `memory/YYYY-MM-DD.md` |
| Installed/configured something | `TOOLS.md` |
| End of session | Always update today's daily note |

---

## Common Mistakes

1. **"Mental notes"** — if it's not in a file, it doesn't exist after restart
2. **Writing everything** — MEMORY.md is curated, not a stream of consciousness  
3. **Forgetting to update** — after a good session, spend 2 min filing
4. **Loading MEMORY.md in group chats** — privacy risk, and not needed

---

## The memory_search Trick

The semantic search isn't perfect. Be specific:

```javascript
// Bad — too vague
memory_search({ query: "work" })

// Good — specific context
memory_search({ query: "PyTorch CUDA RTX 4060 installation decisions" })
memory_search({ query: "Tailscale peer agent setup choices" })
```
