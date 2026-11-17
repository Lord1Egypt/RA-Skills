## Description:

电商财务月度自查包（免费版） is a local ecommerce finance reconciliation checker for platform settlement, promotion subsidy reconciliation, and live-commerce commission and slot-fee settlement tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations teams use this skill during monthly ecommerce close, reconciliation, and payout review to check arithmetic, totals, duplicates, missing values, and source-line evidence in segmented ecommerce finance tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic and table-consistency findings as accounting, audit, tax, banking, or contract advice.

Mitigation: Use the skill as a reconciliation aid only and route material findings through qualified finance, audit, tax, banking, or contract reviewers before decisions are made.

Risk: Broad trigger words could run the skill on unsuitable or incomplete ecommerce finance material.

Mitigation: Invoke the skill explicitly and provide segmented source tables with headers; when material is insufficient, rely on the missing-input report rather than drawing a conclusion.

Risk: The free version intentionally omits some checks, including refund and payment settlement checks, advertising rebate checks, and specific paid-scope validations.

Mitigation: Review the reported scope and omitted checks before acting on the output, and use additional review for withheld or out-of-scope reconciliation areas.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ecommerce-monthly-selfcheck-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON finding report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include check scope, omitted checks, severity counts, line references, evidence text, and insufficient-input messages when the supplied material cannot support a conclusion.]

## Skill Version(s):

1.0.53 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
