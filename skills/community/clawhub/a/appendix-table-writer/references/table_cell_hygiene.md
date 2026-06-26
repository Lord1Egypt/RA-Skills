# Table Cell Hygiene

## Purpose

Appendix tables are reader-facing.
They should not expose raw evidence snippets that still sound like paper self-narration.

## Drop or rewrite

- `we propose ...`
- `our extensive evaluation ...`
- `evaluations across ... validate ...`
- `through extensive benchmarking ...`
- `specifically, we introduce ...`
- `building on this foundation, we present ...`
- writer-instruction cells such as `Evaluation mentions include ...` or `When comparing results, anchor ...`
- survey-meta or scope-setting lines that belong in prose, not in a table cell

## Keep

- short result clauses
- benchmark / metric anchors
- compact limitation or risk statements
- row-comparable evidence phrases

## Boundary

The hygiene policy belongs in `assets/table_cell_hygiene.json`.
The script should apply it deterministically and skip unusable cells rather than preserving reader-unfriendly wrappers.
