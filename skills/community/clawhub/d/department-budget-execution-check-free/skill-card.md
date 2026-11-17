## Description:

部门费用预算执行表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations users use this skill during monthly closing, reconciliation, or inventory-style checks to validate department budget execution tables. It recalculates row arithmetic, checks totals, flags duplicates and blanks, and cites source rows for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Budget execution tables may contain sensitive financial data.

Mitigation: Run the skill only in environments approved for that data and follow the organization's data-handling rules.

Risk: The interface and findings are Chinese-only, which may lead to review mistakes for users who do not read Chinese.

Mitigation: Have a Chinese-reading reviewer confirm the inputs, findings, and remediation steps before operational use.

Risk: The free version intentionally excludes some checks that a full budget review may require.

Mitigation: Review the listed omitted checks and use another control or the full product when those checks are in scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/department-budget-execution-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown-style terminal text or JSON findings with source-line citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on supplied budget-table text; the free version lists checks that are not included.]

## Skill Version(s):

1.0.56 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
