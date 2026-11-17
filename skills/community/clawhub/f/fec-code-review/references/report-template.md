# Code review report template

```markdown
# Code review report

> Generation time: YYYY-MM-DD HH:mm
> Review tool: frontend-craft

> Review mode: change / targeted / project
> Target scope: paths or PR/commit
> Reviewed: file or module inventory
> Exclusions: paths and reasons
> Unreviewed: remaining files or modules (state none if complete)
> Completion: complete / partial
> Verification: commands, results and reasons for skipped checks

## CRITICAL / Must be modified (N items)
- **[File:line number]** Problem description -> Suggested modifications

## HIGH / Suggested optimization (N items)
- ...

## MEDIUM / Optional optimization items (N items)
- ...

## LOW / Observation items (N items)
- ...

## Good things done
- ...

## Risk Level: Low / Medium / High

**Conclusion**: Change review: merge recommendation; targeted/project review: Low / Medium / High risk and blocking findings
```

After the review is completed, save the report to `reports/code-review-YYYY-MM-DD-HHmmss.md` and inform the user of the report path.

Retain merge recommendations for change review; use risk assessments for targeted and project reviews. For partial reviews, conclusions apply only to reviewed scope and do not establish project-wide approval.
