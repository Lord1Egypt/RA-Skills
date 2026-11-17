# Templates (v2)

> Load on demand. SEED card + T2 three-layer README + task anchors in 3 grades.

## SEED card (T1)

```markdown
# <project>

> Goal: {one line — what this project is}
> Outputs: {path, or "TBD"}
> Next: {verb + object + acceptance criterion}
> YYYY-MM-DD created · updated ×N
```

Rules: **≤10 lines hard cap** (overflow = T2 signal) · every touch overwrites "Next", counter +1 · no tasks/ dir · one INDEX line (T1).
Upgrade to T2: fold goal/outputs into README background → delete SEED.md → build the full set.

## T2 project anchor (README.md, three-layer)

```markdown
# <project> — anchor

> Status: active / done / paused | Tier: T2 | Last update: YYYY-MM-DD

## Background (frozen)
[What this is / goal / boundaries, 30–80 words. Changes go through EVOLUTION.md, never edited here.]

## Status (overwritten)
- One-line state: {where the project is right now}
- Active tasks:
  | Task | Anchor | Status |
  |------|--------|--------|
  | Task A | tasks/keyword-a.md | 🔄 |
- Next: {project-level direction, not task-level steps}

## Map (incremental index)
> A fresh agent reads this to know how the files are used.

| Path | Type | Purpose | When to read |
|------|------|---------|--------------|
| tasks/ | dir | in-flight task anchors | on resume |
| report.md | file | core deliverable | first |

## Recent news (rolling window, keep ≤3)
- YYYY-MM-DD: {one-line event}
```

Maintenance: **≤150-line hard cap** (over = push to EVOLUTION or delete) · status section is **overwritten**, never appended · news rolls at 3 · background edits require an EVOLUTION entry first.

## Task anchor — minimal (<30 min)

```markdown
---
time: YYYY-MM-DD HH:MM
type: final
inputs: [request]
outputs: [files]
next: [next step or "done"]
---
## Note
[One line: what was done]
```

## Task anchor — standard (30 min – half day)

```markdown
---
time: YYYY-MM-DD HH:MM
type: checkpoint | final
inputs: [...]
outputs: [...]
next: [executable next step or "done"]
---
## Deliverables
- `path/to/file` — what it is
## Key decisions
- chose X because Y
## Blockers / risks
- [none / open items]
```

## Task anchor — detailed (half day+)

Adds below the standard frontmatter:

```markdown
## Progress
### Done
### In flight (with %)
### Not started
## Technical notes (optional)
```

**Endgame reminder**: `type=final` anchors are distilled within 14 days then **deleted** — write the *why* in Key decisions now, or there will be nothing worth distilling later. Anchors that only record *what* happened get deleted without distillation.
