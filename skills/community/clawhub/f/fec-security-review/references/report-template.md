# Security review report template

```markdown
# Security Review Report

> Generation time: YYYY-MM-DD HH:mm
> Review tool: frontend-craft

> Review mode: change / targeted / project
> Target scope: paths or PR/commit
> Reviewed: file or module inventory
> Exclusions: paths and reasons
> Unreviewed: remaining files or modules (state none if complete)
> Completion: complete / partial
> Verification: commands, results and reasons for skipped checks

## CRITICAL / HIGH RISK (N items)
- **[File:line number]** Risk description -> Repair suggestions

## HIGH / Medium to high risk (N items)
- ...

## MEDIUM / medium risk (N items)
- ...

## LOW / low risk or recommended (N items)
- ...

## Passed security check
- ...

**Overall security level**: safe / risky / high risk and needs to be repaired
```

After the review is completed, save the report to `reports/security-review-YYYY-MM-DD-HHmmss.md` and inform the user of the report path.

Retain merge recommendations for change review; use risk assessments for targeted and project reviews. For partial reviews, conclusions apply only to reviewed scope and do not establish project-wide approval.
