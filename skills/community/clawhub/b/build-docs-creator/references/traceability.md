# Reference: `04-traceability-matrix.md`

Style: RTM (Requirements Traceability Matrix) — a standard development-handoff artifact (IEEE 1012-adjacent). It links every requirement to where it's addressed in design and interfaces, so a dev team can see coverage at a glance and reviewers can spot orphaned requirements (specified, never built) and orphaned features (built, never specified).

This document is what elevates the package from "a pile of docs" to "a traceable spec." It is assembled last, because it references identifiers created in the requirements, design, and interface documents.

## Purpose

For each requirement, answer: where is this addressed in the design, and which interface(s) implement it? And in reverse: is anything built or designed that no requirement covers?

## Required content

### 1. Coverage Matrix
A table keyed by requirement ID. One row per `FR-`/`NFR-`.

```
| Req ID | Requirement (short) | Design section | Interface(s) | Status |
|--------|---------------------|----------------|--------------|--------|
| FR-1 | Customer lookup by phone | §5 Interfaces & Integrations | customer-lookup.html | Built |
| FR-2 | Export report to PDF | — | — | Specified, not built |
| NFR-3 | SOC 2 audit logging | §2 Tech Stack (Auth) | — | Open — provider undecided |
```

Status vocabulary (use exactly these):
- **Built** — a requirement with corresponding design coverage and at least one implementing interface
- **Designed, not built** — design addresses it, no interface yet
- **Specified, not built** — requirement exists, no design or interface coverage
- **Open** — coverage blocked by an unresolved decision (cross-reference the relevant Open Question)

### 2. Orphaned Features (reverse trace)
A short list of anything found in the built interfaces or design that has **no corresponding requirement**. Each such item should also have produced a *derived* requirement back in `01-requirements.md` (tagged "derived from built interface"); list them here so the gap between original spec and built product is explicit in one place. This is the primary reconciliation output for the ChatGPT-import pipeline.

### 3. Coverage Summary
Two or three lines of plain numbers: how many requirements are Built vs. Specified-not-built vs. Open, and how many orphaned features were found. This gives a dev lead an instant read on how build-ready the package is.

## Standards for this section

- **Every `FR-`/`NFR-` in `01-requirements.md` appears exactly once** in the coverage matrix — no requirement silently dropped.
- **Interface filenames must match** actual files in `03-interfaces/html/`, and design sections must match real sections in `02-design.md`. Don't cite documents that don't contain the referenced content.
- **Don't fabricate coverage.** If a requirement has no implementing interface, the cell is "—" and the status reflects that. A matrix that shows everything "Built" when half of it wasn't is worse than useless — it hides the exact gaps this document exists to reveal.
- Keep it a table plus two short lists. This is a reference grid, not prose.
