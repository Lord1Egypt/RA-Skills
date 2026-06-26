# PPA Report Guide

When summarizing reports, extract only the most decision-useful metrics first.

## Synthesis Stage

Look for:

- Top module recognized
- Cell count
- Inferred sequential elements (flip-flops, latches)
- Obvious warning categories

## Backend Stage

Look for:

- Latest run ID
- Whether final GDS was generated
- Timing slack / WNS (Worst Negative Slack) if available
- Area-related summary
- Major DRC/LVS blockers if present

## Summary Format

Prefer the following structure:

- `status`: PASS / FAIL / PARTIAL
- `artifacts`: Key file paths
- `metrics`: Small JSON-like block with key numbers
- `blockers`: Short bullet list of issues
- `next_step`: One recommended action
