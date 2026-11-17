## Description:

农产品收购发票与进项抵扣核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and accounting teams use this skill during month-end closing, reconciliation, or inventory checks to verify agricultural purchase invoice input deduction tables. It performs deterministic table checks and cites source rows, but it does not decide the applicable tax policy.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may treat deterministic table findings as tax advice.

Mitigation: Use the skill as a table consistency checker only; consult a tax professional or competent tax authority for policy and filing decisions.

Risk: The free release does not run the complete set of checks described as outside this package.

Mitigation: Review the reported withheld and out-of-scope checks before relying on the output for reconciliation or filing preparation.

Risk: Agricultural purchase invoice deduction tables can contain sensitive business data.

Mitigation: Run the checker locally as described and avoid sharing input files outside approved internal workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/agri-purchase-invoice-deduction-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON result objects with cited findings from the local Node.js checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs the bundled free checks locally and reports withheld and out-of-scope checks when relevant.]

## Skill Version(s):

1.0.61 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
