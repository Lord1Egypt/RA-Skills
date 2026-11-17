# Reporting contract

Every Groundcrew report — any output the user may forward, file, or act on later —
follows one skeleton, one verdict scale, and one fact-labeling scheme. Report skills
(`weekly-report`, `audit-report`, `keyword-report`, `competitor-readout`, `geo-report`,
`authority-report`) must use all three; other skills use them whenever they emit a
report-shaped result.

## Skeleton

```markdown
# <Site> — <Report name> — <period or as-of date>

Bottom line: <one sentence>. Verdict: SHIP | FIX | BLOCK | UNDECIDED

## Measured
| metric | value | vs last | label | source | as of |

## What changed
<events in the period; each marked verified (how) or unverified>

## Next 3 actions
<action — owner — effort — expected effect (qualitative, no projections)>

## Evidence
<evidence record paths/ids, proof URLs, job ids>

## Not measured
<what could not be observed and why>
```

Sections stay in this order. Empty sections say why they are empty instead of
disappearing. `## Next 3 actions` may hold fewer than three when fewer are justified;
it never pads.

## Verdicts

- **SHIP** — the reported surface is in acceptable shape; nothing found blocks the next
  planned action.
- **FIX** — specific named defects exist; the report lists them with an owner and the
  next action is repair. FIX, not SHIP, whenever any `critical` finding on the reported
  surface is open.
- **BLOCK** — a veto tripped. Vetoes are absolute: one veto forces BLOCK regardless of
  every other number. Standing vetoes: a claim in the report cannot be traced to
  validated evidence; an evidence record failed doctor validation and was used anyway
  (never do this); the action the report recommends is irreversible or outward-facing
  and lacks owner review.
- **UNDECIDED** — required evidence is missing. Name what is missing and the cheapest
  way to get it. Never guess a verdict to avoid UNDECIDED.

## Fact labels

Every value in `## Measured` carries exactly one label:

- **Measured** — read from a source that passed the Groundcrew evidence contract;
  the row names source and observation time.
- **User-provided** — pasted or imported by the user; reported verbatim with the
  import date. Groundcrew does not silently correct user numbers.
- **Estimated** — a third-party estimate or heuristic; the row names the estimator.
  Estimates never appear without the label and never upgrade to Measured by repetition.

`vs last` compares only values with the same label and the same source; otherwise the
cell stays empty with a note in `## Not measured`. Missing values remain missing —
never zero, never interpolated.
