# Quality checklists (v2)

> Run before creating or updating any anchor.

## Tiering check (new project)

- [ ] T0: truly one session? More than 3 output files already? (yes → force T1)
- [ ] T1: does it fit in 10 lines? Any of the 4 promotion signals fired? (yes → T2)
- [ ] T2: signal-justified, or explicit kickoff?

## SEED card check (T1, every touch)

- [ ] ≤10 lines? · "Next" executable verbatim? · counter +1, date refreshed? · INDEX line present?

## T2 project anchor check (every update)

- [ ] ≤150 lines? (over = push to EVOLUTION or delete)
- [ ] Status section **overwritten**, not appended?
- [ ] Recent news ≤3 entries?
- [ ] Active-task table matches actual files in tasks/ (no finished stragglers)?
- [ ] Map covers key files — a fresh agent can navigate from it alone?
- [ ] "Next" is project-level direction, not task-level steps?
- [ ] Background edits went through an EVOLUTION entry?
- [ ] Real decision this session → EVOLUTION appended?

## Task anchor check (every update)

- [ ] `time` is now, not task start
- [ ] `inputs` / `outputs` complete (file paths, never empty)
- [ ] `next` executable without reading anything else:
  - ❌ "continue optimizing" · ✅ "chunk-process the CSV in batches ≤10k rows to cap memory"
- [ ] Key decisions record **why** (the only thing worth distilling later)
- [ ] `type=checkpoint` → blockers/risks filled; `type=final` → "none" or empty

## The `next` field — the most important line in any anchor

It's the first thing read on restore. Test: can you start working from `next` alone? Will you know when it's done?

## Failure modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| Vague `next` | resume stalls, no entry point | rewrite: verb + object + acceptance criterion |
| Missing outputs | can't tell if the task really finished | list deliverable paths |
| Decisions without why | nothing to distill at day 14 | add the reason now |
| README bloat | >150 lines | progress → task anchors, decisions → EVOLUTION, chaff → delete |
| Status becomes a diary | every update appends downward | overwrite instead |
| News window drifts | 5, 6, 8 entries… | keep 3, let the rest roll |
| tasks/ graveyard | finished anchors linger | distill & delete; doctor backstops |
| T0 abuse | "one-shot" task spans weeks | >3 files → force T1, backfill SEED |
| History rewritten | old EVOLUTION entries edited | append "Later we found…" instead |
