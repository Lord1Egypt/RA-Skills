## Description:

应收对账表逐项核对（逐行算术、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。触发词包括 应收对账表核对、应收对账表对不上。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, warehouse, and operations staff use this skill at month-end close, reconciliation, payroll, or inventory checkpoints to check AR aging tables for arithmetic mismatches, total-row inconsistencies, duplicate customers, and missing values. It returns findings with source line references and withholds conclusions when the provided table is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receivables tables may contain sensitive business information.

Mitigation: Run the checker only on files you intend the local tool to read and avoid supplying unnecessary customer or transaction details.

Risk: The free version documents withheld checks and out-of-scope judgments, including credit-balance prompts, over-collection detection, long-aged balance ratio checks, and accounting, audit, tax, or legal opinions.

Mitigation: Treat the output as arithmetic reconciliation support, review the listed checks not run, and use separate accounting review for business judgments outside the tool scope.

Risk: Insufficient or unrecognized table input can prevent reliable conclusions.

Mitigation: Provide an AR aging table with recognizable headers and customer detail rows; when the tool reports insufficient input, supply the missing fields instead of treating the absence of findings as clearance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ar-aging-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Console text or JSON findings with source line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings list executed checks, checks not run, missing-input guidance, and summary counts.]

## Skill Version(s):

1.0.58 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
