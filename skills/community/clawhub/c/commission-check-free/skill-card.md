## Description:

提成计算表逐项核对（逐行算术、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。触发词包括 提成计算表核对、提成计算表对不上。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashiering, warehouse, and operations staff use this skill during monthly settlement, payroll, reconciliation, or inventory close to check sales commission tables for arithmetic mismatches, duplicate people, blanks, and total-row inconsistencies. It reports missing input instead of asserting a clean result when the table cannot be checked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker verifies arithmetic consistency and table completeness, not whether a commission policy is legally, contractually, or commercially correct.

Mitigation: Have a qualified human compare findings with the governing commission policy, contract terms, and payroll process before acting.

Risk: Users may run the tool on the wrong or unintended local file.

Mitigation: Pass only explicitly selected commission-table files and review the cited line numbers before using the result.

Risk: The free edition intentionally omits some checks, including tiered commission recalculation and commission-rate range validation.

Mitigation: Review the listed omitted checks and use a broader workflow when those controls are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/commission-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON from a local Node.js checker, typically summarized by the agent in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; insufficient input returns missing requirements instead of a clean conclusion.]

## Skill Version(s):

1.1.54 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
