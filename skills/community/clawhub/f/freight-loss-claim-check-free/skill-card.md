## Description:

货运破损理赔与承运商扣款明细表逐项核对（理赔金额复算、扣款不得超过理赔金额、重复运单与赔付比例超上限、关键字段缺失或负数），每条结论引用原文行号与运单号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, logistics cost, and accounts payable users use this skill during monthly carrier settlement to check freight loss claim and carrier deduction tables. It recomputes row-level claim amounts, flags over-deductions, duplicate waybills, excessive compensation rates, and missing or negative key fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker provides arithmetic and table-consistency assistance, not a complete freight claim, contract, tax, or legal audit.

Mitigation: Use the output as a reconciliation aid and verify final settlement decisions against the contract, source documents, invoices, and accounting records.

Risk: The free version does not perform total-row reconciliation or other withheld checks, despite one runtime disclaimer wording that could imply a broader total-row check.

Mitigation: Review the listed checks_not_run or checks_withheld fields and perform total-row reconciliation separately when it is required.

Risk: Incomplete tables or unrecognized headers prevent meaningful conclusions.

Mitigation: Provide the required freight loss claim table headers and treat insufficient_input responses as no conclusion rather than as no issue found.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/freight-loss-claim-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable text or JSON report with cited line numbers, waybills, findings, summary fields, and omitted checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Node.js checker; insufficient input returns missing fields and does not produce a correctness conclusion.]

## Skill Version(s):

1.0.4 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
