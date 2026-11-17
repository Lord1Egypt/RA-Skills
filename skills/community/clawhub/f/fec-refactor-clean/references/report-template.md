# Refactor cleaning report template

```markdown
# Refactor cleanup report

> Generation time: YYYY-MM-DD HH:mm
> Cleanup scope: File/Module/Dependency/Route/Style

## Baseline verification

| Command | Status before cleaning | Status after cleaning | Remarks |
| --- | --- | --- | --- |
| `npm run lint` | failed/passed/didn’t run | failed/passed/didn’t run | ... |

## Candidates and evidence

| Candidates | Evidence | Risk Classification |
| --- | --- | --- |
| `path/to/file.ts` | Tool output / rg search / type checking | SAFE / CAUTION / DANGER / UPGRADE |

## Cleaned items

- Deleted or modified files, exports, styles, dependencies or configurations
-Evidence corresponding to each cleanup

## Skip reason

- Why is the CAUTION / DANGER item not automatically processed?
- Content that requires manual confirmation, runtime verification, or specialized processes

## Verification command

- lint, type-check, test, build or manual verification performed
- Summary of key outputs

## Residual risk

- Dynamic references, runtime templates, plug-in metadata or external entry risks
- Recommend subsequent cleaning or dependency upgrades
```

After cleaning is completed, save the report to `reports/refactor-clean-YYYY-MM-DD-HHmmss.md` and inform the user of the report path.
