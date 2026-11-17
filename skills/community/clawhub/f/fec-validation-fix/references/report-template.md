# Verify repair report template

```markdown
# Verify repair report

> Generation time: YYYY-MM-DD HH:mm
> Verification scope: lint/type-check/test/build/CI

## Command status table

| Command | Initial state | Repaired state | Remarks |
| --- | --- | --- | --- |
| `npm run type-check` | failed/passed/didn’t run | failed/passed/didn’t run | ... |

## Failure summary

- Errors that occur earliest and cascade
- Affected files, error types and critical logs
- Whether it is CI exclusive, test environment, dependent version or flaky issue

## Root cause

- Confirmed root cause
- Output, logs, or reproduction evidence to support the conclusion

## Fix content

- Modified files and behavior
- Why the failure was not circumvented by turning off rules, removing assertions, or reducing type safety

## Verification results

- Command to re-execute
- Summary of command output
- Are there still failed items?

## Residual risk

- Uncovered verification commands
- Issues that still require user decision-making or external environment confirmation
```

After the verification fix is completed, save the report to `reports/validation-fix-YYYY-MM-DD-HHmmss.md` and inform the user of the report path.
