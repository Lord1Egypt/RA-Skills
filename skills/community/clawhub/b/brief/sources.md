# Sources — From Raw Pile to Brief Material

Triage discipline for user-provided material. The user grants the sources (SKILL.md Rule 1); this file governs what you do with them.

## Extraction Workflow

1. Name the decision first (SKILL.md Rule 2). No decision named, no extraction — you cannot tag relevance against nothing.
2. One pass over the material, tagging lines: **D** (changes the decision), **C** (context that changes how D is read), **N** (noise). Do not write brief prose during this pass.
3. Second pass over D-lines only: attach a comparator and as-of date to every number; note provenance per line.
4. Build the brief from D-lines; admit C-lines only if they pass the SCQA test (`templates.md`); N never enters, however interesting.

## Triage by Source Type

| Source | Play |
|--------|------|
| Long report | Exec summary + conclusions first, then mine tables and headings; body prose last, only for D-line verification |
| Email or chat thread | Read newest-to-oldest until the state stops changing; the thread's chronology is the argument's history, not the story to tell |
| Meeting transcript | Extract decisions, owners, and dates only; discussion that led nowhere is N by definition |
| Dashboard / data export | Take only numbers that have a comparator available; every figure gets an as-of timestamp |
| Doc pile | Order by recency; newest wins conflicts unless an older source is more authoritative (signed contract beats chat message) |
| Prior briefs in a series | Diff against the latest edition; only the delta is material (`recurring.md`) |
| Verbal download from the user | Read back the D-lines you captured before writing — verbal sources have the highest misquote rate |

## Conflicting Sources

- Never average. "$1.3M" from a $1.2M report and a $1.4M dashboard is a number nobody reported.
- Present both with provenance and, when known, the reason: "Finance: $1.2M; dashboard: $1.4M — finance is net of refunds."
- Unresolvable conflict = itself a key point when the decision hangs on the number: "Revenue is between $1.2M and $1.4M depending on refund treatment; either way above the $1.0M covenant."
- Authority order when you must pick one: audited/signed > official report > live dashboard > chat/verbal. Say which you picked and why.

## Gaps

- Name what's missing and its cost to the decision: "No churn data — the renewal recommendation is half-blind." Silent scope-narrowing is the failure mode: the reader assumes coverage you didn't have.
- A gap the user can fill cheaply → ask once, before writing. A gap nobody can fill by the deadline → flag it in caveats and proceed.
- Distinguish "not in my sources" from "does not exist" — write the one you actually know.

## Staleness

- Every extracted number carries its as-of date into the brief (Output Gates).
- Stale beyond the decision horizon (deciding next quarter's budget on data from two quarters back) → flag prominently or drop; a flagged stale number beats a fresh-looking one.

## Quote vs Paraphrase

- Quote verbatim when exact words carry weight: commitments, legal language, pricing, anything the reader may need to cite onward.
- Paraphrase everything else — quotes are expensive lines.
- Never quote-mine: a quote that reverses meaning without its surrounding sentence is fabrication with extra steps.

## Confidentiality Screen

- Check the **Exclusions** preference area (SKILL.md Configuration) before extraction: excluded topics and metrics never enter the brief, even as context.
- Mixed-sensitivity material with an external or wide audience → produce the shareable version and tell the user what was withheld and why, so they can override.

## Provenance Line

Every brief closes with its sources: `Sources: Q3 board deck, #eng-status thread through Tue, finance export (as of Jul 21).` One line; it is what lets the reader challenge you precisely instead of vaguely.
