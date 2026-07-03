---
name: design-eval-loop
description: |
  Use when an existing UI artifact needs to be iterated to a verified 5/5 design score. Enumerate every view, run independent dead-item and design-rubric audits, apply fixes, then re-score with fresh reviewers until every view and the whole app pass. Designed for Enterprise Crew/OpenClaw operators finishing prototypes without false 5/5 claims.
triggers:
  - "design eval"
  - "score it till 5/5"
  - "loop till 5/5"
  - "design eval loop"
  - "rate every page"
  - "no dead links"
  - "no dead items"
  - "audit every view"
  - "polish to 5/5"
version: 1.0.0-ec.1
author: Book / Enterprise Crew
license: MIT
source: open-design/skills/design-eval-loop
metadata:
  hermes:
    tags: [design, qa, ui, evaluation, openclaw, enterprise-crew]
    related_skills: [browser-testing-with-devtools, dogfood, manual-human-qa, publish-skill]
od:
  mode: utility
---

# Design Eval Loop

Drive an existing UI artifact to a **verified 5/5** on a current design rubric.
The engine is a per-view loop: **enumerate → audit + score (parallel sub-agents)
→ fix → re-score**, repeated until every view passes, then once more for the
whole app. It is a finishing pass — the artifact must already exist.

This skill exists to stop two failure modes: shipping **dead controls** (links
and buttons that go nowhere) and claiming a **false 5/5** without evidence.

## EC public-safety note

This skill is safe to publish as a generic workflow. Do not include private product names, customer data, internal screenshots, private URLs, or local filesystem paths in public scorecards. For public release, run the publish-skill sanitizer before sending the bundle to GitHub, SuperAda, or ClawHub.

## When to use

- "Score this and keep improving until it's 5/5 on the design eval."
- "Make sure every page is linked — no dead items."
- "Run sub-agents over every view and rate them till they pass."

Not for: building the artifact from scratch (build it first), or a one-line
visual tweak (just make the edit).

## Inputs to lock before looping

1. **Target file(s)** — which artifact(s). If multiple builds exist, confirm
   whether the loop runs on one or all of them; they are separate files and
   each needs its own pass.
2. **View inventory** — the full list of distinct views/screens/panels/overlays.
   Derive it from the file, don't guess. State the count aloud (e.g. "20 views").
3. **Rubric** — default to `references/rubric.md`. Honor any dimension the user
   names explicitly (e.g. "2026 best practices", "WCAG AA").
4. **Pass bar** — default **5.0/5 per view, then 5.0/5 whole-app**. The user may
   relax it (e.g. "≥4.5 is fine").

## The loop

Plan it with TodoWrite first — one todo per phase, plus the iteration cap.

### Phase 1 — Enumerate
List every view and every interactive element. A view is any distinct
surface: home, drawer, sheet, overlay, settings list, and **each** detail
panel. Detail panels are views too — don't fold them into one line.

### Phase 2 — Audit + score in parallel
For each round, spawn **two sub-agents at once** (one message, two `Agent`
tool calls) so they don't collide on the file:

- **Agent A — Dead-item audit.** Crawl every clickable element; report any that
  navigate nowhere, have no handler, or give no feedback. Output: a list of
  dead items with selector + expected destination.
- **Agent B — Design eval.** Score every view against `references/rubric.md`,
  0–5 per dimension, with a one-line reason per sub-score and the specific
  blocker keeping each view under the bar.

Use the prompt templates in `references/sub-agent-prompts.md` verbatim; they
force structured, file-grounded output instead of vibes.

### Phase 3 — Fix
Apply the highest-impact findings first: real bugs (undefined tokens, occluded
panels, wrong z-index), then dead items, then the lowest-scoring rubric
dimensions. Fix in the canonical file. After edits, run a static integrity
check (balanced tags/braces/parens, every panel defined, every row mapped).

### Phase 4 — Re-score
Re-run Agent B (a fresh agent — don't trust the fixer's self-report) on the
changed views. Record the delta in a scorecard. Repeat Phases 2–4 per view
until it hits the bar.

### Phase 5 — Whole-app pass
Once every view passes individually, score the **whole app** as one experience
(cross-view consistency, shared theme, navigation coherence, no orphan
surfaces). Iterate until the whole-app score hits the bar.

## Convergence and escape hatches

- **Iteration cap:** max **4 rounds per view** and **3 whole-app rounds**. If a
  view won't reach the bar within the cap, stop and report the exact remaining
  blocker — do not loop on cosmetics.
- **Honesty gate (non-negotiable):** never claim 5/5 without a fresh scoring
  agent confirming it. If the real ceiling is structural (e.g. native-control
  rewrite, focus-trap) and out of scope, say so and report the true score
  rather than rounding up. A reported 4.6 with a named gap beats a fabricated 5.
- **User break:** the user can stop the loop at any round; report current state.

## Output each round

Emit a compact scorecard table (view → before → after) plus an
`<od-card type="verify-scorecard">` covering the dead-item and rubric checks.
End with: which views pass, which don't, the named blocker for any that don't,
and the next round's target.

## Hard rules

- **Parallel, not serial:** Agent A and Agent B launch in the same message.
- **Re-score with a fresh agent:** the agent that fixed the code does not grade
  its own work.
- **Every link opens somewhere:** zero dead items is a P0, not a nice-to-have.
- **Detail panels count as views.** A 5/5 on the shell with unscored panels is
  not a 5/5.
- **One canonical file is the source of truth** — edits land there, not in chat.

## References

- `references/rubric.md` — the scoring dimensions, weights, and 5/5 bar.
- `references/sub-agent-prompts.md` — paste-ready prompts for Agent A and Agent B.
