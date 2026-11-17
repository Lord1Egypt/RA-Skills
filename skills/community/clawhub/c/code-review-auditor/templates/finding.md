# Finding Template

```markdown
## [<ID>] <Title>

- Category: <bugs|security|architecture|code-smells|patterns|anti-patterns|performance|observability|testing>
- Location: `<path>:<start>-<end>`
- Severity: <Critical|High|Medium|Low|Info>
- Confidence: <High|Medium|Low>
- Effort: <XS|S|M|L|XL>
- Priority: <P0|P1|P2|P3>
- Refactorability Score: <0-100 or N/A>

### Description
<What is wrong or risky.>

### Evidence
<Specific code/config/test evidence. Quote only the minimum needed.>

### Impact
<How this can fail, be exploited, slow down, or increase maintenance risk.>

### Recommendation
<Smallest responsible change.>

### Suggested Example
<Short code sketch, test idea, architecture sketch, or refactoring outline.>

### Possible False Positive
<What condition would make this finding not applicable.>
```
