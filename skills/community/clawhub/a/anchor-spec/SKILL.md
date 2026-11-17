---
name: anchor-spec
description: "Tiered project anchors for AI coding agents. Tier a project (T0 zero-anchor / T1 seed card / T2 full anchor), maintain it with a three-layer information model (snapshot README ≤150 lines, append-only EVOLUTION, raw log), and let anchor-doctor automate lifecycle care (cold-storage banners, distillation, archiving). Trigger on: new project / continue / resume / where were we / project anchor / seed card."
user_invocable: true
disable-model-invocation: false
---

# anchor-spec — Project Anchor Executor

You are the anchor system executor. Tier → create/read anchors → restore the project → get to work immediately.
Anchors are an **asset, not a compliance ritual**: things enter, things leave, rot is handled by `anchor-doctor`. Your job is to pick the right tier, write to the right layer, and keep it thin.

All anchors live under one configurable root (default `./anchors/`, change to `docs/` or anywhere):

```
<root>/<project-name>/SEED.md          # T1 seed card (≤10 lines)
<root>/<project-name>/README.md        # T2 project anchor (≤150 lines)
<root>/<project-name>/EVOLUTION.md     # T2 decisions (append-only)
<root>/<project-name>/tasks/*.md       # task anchors (in-flight only)
<root>/INDEX.md                        # the single project overview
```

## Core function

```
Input: user instruction (trigger words)
Path:
1. New project?      → tier it (T0/T1/T2) → T0 just work / T1 create SEED / T2 full anchor
2. Task trigger?     → (T2 only) create_task_anchor(name, complexity)
3. Update trigger?   → locate anchor → update (see invariants)
4. Resume trigger?   → T1: read SEED, go. T2: run the resume funnel
```

## Tiering (first step for any new project — never skip)

| Tier | Criteria | Action | Cost |
|------|----------|--------|------|
| **T0** one-shot | Expected single session | No anchor. Put outputs wherever they belong. Failsafe: >3 output files → force-upgrade to T1 | zero |
| **T1** light | May span sessions, still light | Create `SEED.md` + register in INDEX | 1 min |
| **T2** full | Any of 4 promotion signals, or explicit project kickoff | Full anchor set | 10 min |

**T1→T2 promotion signals** (anchor-doctor's weekly report flags these; you can also judge):
1. Project name appears ≥3 times across sessions (in the raw log)
2. >5 files in the project dir, or parallel tasks need `tasks/`
3. Outputs get referenced by other projects/flows
4. Still active after 2 weeks

Upgrade action: fold SEED content into the README background section → delete SEED.md → build the full set → INDEX updated.

## T1 → create_seed

1. Create `<root>/<project>/`
2. Write `SEED.md`:

```markdown
# <project>

> Goal: {one line}
> Outputs: {path, or "TBD"}
> Next: {verb + object + acceptance criterion}
> YYYY-MM-DD created · updated ×N
```

3. Register one line in INDEX (marked T1)
4. Every touch: overwrite "Next", counter +1. **≤10 lines hard cap** — if it won't fit, that's the T2 signal.

## T2 → create_project_anchor

1. Create `<root>/<project>/` + `tasks/`
2. Write `README.md` with the three-layer structure (template in `references/templates.md`):
   - **Background** (frozen): identity / goal / boundaries. Changes go through EVOLUTION, never edited in place
   - **Status** (overwritten): one-line state / active-task table / next step
   - **Map** (incremental): one line per key file (path + type + purpose + when to read)
   - **Recent news** (rolling window): last 1–3 one-line events, older ones roll off
   - **≤150-line hard cap** — over the cap means content belongs in EVOLUTION or in the bin
3. Update INDEX
4. Optionally create `EVOLUTION.md` (only for real decisions)

## The three-layer invariant (binding on every update)

| Layer | File | Update mode | Invariant |
|-------|------|-------------|-----------|
| L3 snapshot | README.md (≤150) | status overwrite / map incremental / background frozen / news rolling | **carries no history** |
| L2 decisions | EVOLUTION.md | **append-only** | **carries no status** |
| L1 raw log | daily memory/changelog | append-only | — |

- Status sections may be brutally overwritten **because** append-only layers guarantee no history is lost. That is what keeps the anchor thin and fresh forever.
- `tasks/` is short-lived: on completion, distill (the "why" → one EVOLUTION entry) then delete. Only in-flight tasks stay.
- EVOLUTION entries are never rewritten. A bad old decision gets a new entry: "Later we found…".

## New task → create_task_anchor (T2 only)

1. Confirm the project anchor exists (else tier first)
2. Complexity: <30min → minimal / 30min–half-day → standard / longer → detailed (templates in `references/templates.md`)
3. Create `<root>/<project>/tasks/<keyword>.md`, update the README status table and map
4. `next:` must be executable verbatim — verb + object + acceptance criterion (see `references/quality.md`)

## Updating anchors

Must update when: task finished (README status + task distill/delete) · task runs >1h (task anchor becomes checkpoint) · a real decision is made (EVOLUTION append) · a new risk appears (status note) · key files added/removed (map sync) · project event (news window, keep ≤3).

## Restoring a project

**T1**: read SEED.md → do what "Next" says.
**T2 resume funnel**:
1. README status section (30 seconds: where are we / active tasks / next)
2. Map section — pull only the files that matter for the active task
3. EVOLUTION — only if you need *why* something is the way it is
4. Raw-log archaeology — only if detail is still missing

Cold-storage banner present (⚠️)? Verify key facts before trusting the anchor, then remove the banner.

## Shared constraints

- Project-level progress goes in anchors, **not** in global memory files
- README ≤150 lines, SEED ≤10, hard caps
- `tasks/` holds in-flight only — complete → distill → delete
- `INDEX.md` is the single overview; update only on status changes (not on every touch)
- Lifecycle (banners / archiving) is anchor-doctor's job — don't hand-manage banners

## References (load on demand, not upfront)

- `references/templates.md` — SEED card + T2 README + task-anchor templates (3 grades)
- `references/rules.md` — layer invariants, EVOLUTION format, INDEX rules, distillation
- `references/quality.md` — checklists + failure-mode table
- `doctor/anchor-doctor.py` — read-only lifecycle auditor (`survey` mode scans, `doctor` mode proposes fixes, dry-run default)
