# Maintenance rules (v2)

> Load on demand. Layer invariants + EVOLUTION + INDEX + distillation.

## The three-layer invariant (highest priority)

| Layer | File | Update mode | Invariant |
|-------|------|-------------|-----------|
| L3 snapshot | README.md (≤150 lines) | status overwrite / map incremental / background frozen / news rolling | **carries no history** |
| L2 decisions | EVOLUTION.md | **append-only** | **carries no status** |
| L1 raw log | daily memory / changelog | append-only | — |

- README carries no history — history lives in EVOLUTION. Status may be overwritten *because* append-only layers back it up.
- EVOLUTION carries no status — it only answers "why did we end up here".
- `tasks/` is short-lived: complete → distill → delete. Only in-flight tasks stay.
- "Never delete" applies **only** to EVOLUTION and the raw log.

**History is not forgeable**: EVOLUTION entries are never edited or removed. A wrong old decision gets a new entry ("Later we found…"). Failure records are judgment material for future restores — don't scrub them.

## Distillation (task anchor → EVOLUTION)

Triggered 14 days after `type=final` (anchor-doctor flags candidates; the agent executes):
- Anchor records *why* decisions were made → distill one EVOLUTION entry (what + why + impact) → delete the task file
- Anchor records only *what* happened → delete directly (no retention value)

## EVOLUTION.md

One per T2 project, sibling of README. Records the **decision chain**, not document summaries: what was chosen, why, what it affects. Append on real decisions only ("chose A over B, for a reason") — task completion is not a decision. Never pad it.

```markdown
# <project> — EVOLUTION

> Created: YYYY-MM-DD

## Log

### YYYY-MM-DD: decision title
**What**: ...
**Why**: ...
**Impact**: ...
```

## INDEX.md

The **single** project overview at `<root>/INDEX.md`. Bucketed by activity (🔴 active ≤7d / 🟠 warm ≤30d / 🟡 idle 30d+), one line per project: name, status, current focus, anchor link, tier (T1/T2).
Update **only on status changes** (created / promoted / done / paused / archived) — never on every touch. No task-level detail here.

## Shared constraints

| Constraint | Why |
|------------|-----|
| Project progress goes in anchors, not global memory | keeps global memory from bloating |
| One anchor per project (T1 SEED / T2 README) | projects don't interfere |
| README ≤150 / SEED ≤10 | over the cap = wrong layer or wrong tier |
| tasks/ in-flight only | doctor backstops at 14 days |
| Lifecycle banners/archiving are doctor's job | hand-editing banners drifts from mtime truth |
| Task anchors named by keyword, not timestamp | same task, same file across sessions |
| Tier before you build | T0 just works / T1 seeds / T2 anchors |
