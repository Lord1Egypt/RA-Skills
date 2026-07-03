# Sub-agent prompt templates

Launch **Agent A and Agent B in the same message** (two `Agent` tool calls) so
they run concurrently and don't write over each other. Both are read-only —
they report, they don't edit. The main agent applies fixes after both return.

Fill the `{{...}}` slots before sending.

---

## Agent A — Dead-item audit (read-only)

> You are auditing the file `{{FILE_PATH}}` for **dead interactive items**.
>
> Crawl every clickable/interactive element in the file: links, buttons, rows
> with chevrons, tab/segment controls, drawer items, sheet options, settings
> rows, composer controls, overlay actions.
>
> For EACH one, determine whether it actually does something: navigates to a
> defined panel/screen, toggles a real state, opens an overlay, or gives the
> user feedback (toast/inline). 
>
> Report ONLY a structured list of **dead items** — elements that navigate
> nowhere, have no handler, point to an undefined panel, or give no feedback.
> For each: the visible label, its selector/id, and the destination it *should*
> reach. Also list any settings/drawer row whose target panel id is not defined
> in the file. End with a count: "N dead items of M interactive elements."
>
> Do not edit the file. Do not score design. Just the dead-item list.

---

## Agent B — Design eval scorer (read-only)

> You are scoring the file `{{FILE_PATH}}` against the design rubric below.
> {{PASTE references/rubric.md OR THE RELEVANT DIMENSIONS}}
>
> The views to score are: {{VIEW_LIST}}. Treat every detail panel/overlay as
> its own view — do not collapse them.
>
> For EACH view, give a 0–5 score on every rubric dimension with a one-line
> reason, then the view's weighted average. For every sub-score under 5, name
> the SPECIFIC blocker (selector, missing attribute, measured contrast ratio)
> so it's directly fixable.
>
> Open and trace the actual markup/JS — score the file, not its description.
> Flag any real bugs you find (undefined CSS tokens, occluded panels, dead
> chevrons, wrong-shape focus rings, SVG fill recolor misses).
>
> End with: a per-view table (view → score → top blocker), the whole-app score,
> and the 3–5 highest-impact fixes ranked by score lift. Do not edit the file.

---

## Re-score agent (Phase 4 / Phase 5)

Reuse Agent B verbatim, but scope `{{VIEW_LIST}}` to the views you just changed
(Phase 4) or to "the whole app as one experience, including dimension 9 —
cross-view consistency" (Phase 5). **Always a fresh agent** — the agent that
applied the fixes must not grade its own work.

---

## Orchestration notes

- One round = (A ∥ B) → fix → re-score. Cap at 4 rounds/view, 3 whole-app rounds.
- If A and B disagree about whether something is broken, trust the one that
  cites a selector/line over the one that asserts. Verify the disputed item
  yourself before acting.
- After applying fixes, run a static integrity check before re-scoring:
  balanced tags/braces/parens, every referenced panel id defined, every
  settings/drawer row mapped to a real destination.
