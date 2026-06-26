# Rolling Baseline

Monthly and quarterly reports are not isolated outputs.

When writing a later cycle, always use the previous same-node report as a baseline.

## Rules

### Monthly rolling

When writing `2026-02`, first read the final report and section cards from `2026-01`.

Use them to answer:

- what was the previous month's judgment
- what commitments were made for the next month
- which risks were already known
- which items should now be checked for continuity or closure

### Quarterly rolling

When writing a quarter report, read:

- all monthly reports in the quarter
- the latest previous quarter report if it exists

## Required baseline note

Each later-cycle folder should include a baseline note in `00_intake.yaml` or a short markdown note that records:

- previous report path
- carry-over issues
- carry-over priorities
- changes in light status

## Continuity checks

Before drafting the new report, compare against the previous report:

1. Which `🟡` items turned `🟢`
2. Which `🟡` items stayed `🟡`
3. Which items worsened to `🔴`
4. Which promised next steps were actually executed

## Writing rule

Do not rewrite each month from zero.

The new report should be:

- grounded in current evidence
- checked against the previous cycle's commitments
- explicit about what changed
