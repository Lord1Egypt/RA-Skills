# DREAMS.md — Memory Consolidation & Standing Insights

OpenClaw's memory engine writes scheduled consolidation runs into this file and into `memory/.dreams/`. The "dreaming" feature is configured under `plugins.entries.memory-core.config.dreaming` in `openclaw.json`. This file is **indexed** by the built-in memory engine (FTS5 + vector), so anything written here is searchable via `memory_search`.

> **What goes here:** Distilled, durable insights synthesized from daily logs and MEMORY.md. Patterns that survived a consolidation pass. Long-arc observations about the human you serve.
>
> **What does NOT go here:** Raw daily activity (that's `memory/YYYY-MM-DD.md`), permanent facts (that's `MEMORY.md`), or operating rules (that's `AGENTS.md`).

---

## How DREAMS Get Here

1. **Scheduled dreaming.** OpenClaw periodically runs an isolated consolidation pass (configurable cadence). It reviews recent daily logs and writes a synthesis to this file plus a detailed record under `memory/.dreams/<timestamp>.md`.
2. **Manual dream.** The user can say `dream` in chat — the agent runs a one-shot consolidation against the last N days and appends here.
3. **Promotion.** If a dream survives 3+ consolidation passes (i.e., the pattern keeps recurring), it gets promoted to `MEMORY.md` and removed here.

---

## Format

Each consolidation appends a section like this — never edit prior sections, only append:

```
## Dream — [YYYY-MM-DD HH:MM]
**Source window:** [date range scanned]
**Source files:** [N] daily logs

### Patterns observed
- [Pattern 1 — what kept showing up]
- [Pattern 2]
- [Pattern 3]

### Decisions that stuck
- [Decision + the outcome we saw afterward]

### Open questions
- [Things still unresolved across the window]

### Promotion candidates
- [Insight] — appeared in [N] consolidations. Consider promoting to MEMORY.md.
```

---

*Part of AI Persona OS by Jeff J Hunter — https://os.aipersonamethod.com*
