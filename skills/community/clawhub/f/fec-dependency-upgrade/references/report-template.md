# Diagnostic report template

```markdown
# Front-end diagnostic report

> Generation time: YYYY-MM-DD HH:mm
> Question type: build/runtime/ui/api
> Scope of influence: page, feature, user group or environment

## Problem description

- Phenomenon reported or observed by users
- First appearance time, environment, branch or version

## Reproduction path

1. Operation steps or trigger commands
2. Desired results
3. Actual results

## Evidence collected

- log/stderr/console stack
- Screenshot, DOM, style, network request or trace
- Related configurations, dependency versions, environment variables or status snapshots

## Hypothesis and Verification

| Hypothesis | Verification Method | Results |
| --- | --- | --- |
| Because X, causes Y | Verified by Z | Confirmed / Falsified / Pending |

## Root cause

- Final confirmed root cause
- Why the existing evidence supports this conclusion

## Fix content

- Modified files and behavior
- Why this is a minimal effective fix

## Verification results

- Executed command, manual path or browser verification
- Observed results after fix

## Residual risk

- Uncovered borders
- Areas of possible return

## Next step

- Requires user decisions, follow-up tasks or monitoring items
```

After the diagnosis is completed, save the report to `reports/debug-YYYY-MM-DD-HHmmss.md` and inform the user of the report path.
