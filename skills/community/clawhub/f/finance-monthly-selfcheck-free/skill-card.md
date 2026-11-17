## Description:

分段财务核对材料逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文，并只执行免费版声明的检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and cashiering teams use this skill during monthly close, reconciliation, and inventory checkpoints to check segmented finance tables before downstream review. It performs deterministic arithmetic, cross-total, duplicate, and blank-value checks for the free-tier sections and reports missing materials when input is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-rely on a clean result as a full accounting, tax, audit, reimbursement approval, or filing conclusion.

Mitigation: Use the output only for the listed table-format checks and route accounting, tax, audit, approval, and filing decisions through the appropriate professional process.

Risk: The free tier omits some checks, so unrun sections can remain unchecked even when executed checks pass.

Mitigation: Review the reported checks_not_run or withheld-check list before relying on the result, especially for cash inventory difference and invoice receipt/issue/balance checks.

Risk: Insufficient or incorrectly segmented input can prevent checks from running.

Mitigation: Provide the required section headers, complete table headers, and table rows; treat missing-material output as no conclusion rather than a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/finance-monthly-selfcheck-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [analysis, json, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON containing executed checks, omitted checks, findings, missing-input messages, and source-cited results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against user-provided finance table text; insufficient input returns missing-material guidance instead of a clean conclusion.]

## Skill Version(s):

1.0.51 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
