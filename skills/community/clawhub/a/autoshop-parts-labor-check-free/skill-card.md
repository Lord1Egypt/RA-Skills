## Description:

This skill locally checks Chinese auto-repair work-order tables for parts subtotals, labor fees, order-total reconciliation, duplicate part rows, negative quantities or labor hours, and missing required fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Service advisors, parts managers, and settlement accountants use this skill to check copied repair work-order tables before customer settlement, insurance reconciliation, or key-account reconciliation. It recomputes line and order arithmetic and cites source rows, but it does not decide whether prices are fair or whether work was actually performed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake arithmetic and table-consistency findings for a decision that prices are fair, work was performed, or a refund is owed.

Mitigation: Use the output only as a local consistency check and verify prices, work completion, refunds, and accounting treatment against contracts, DMS records, invoices, and repair evidence.

Risk: Incomplete tables, missing required headers, or placeholder values can prevent reliable conclusions.

Mitigation: Provide the full work-order table with required headers and treat insufficient-input output as no conclusion, not as no issue found.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/autoshop-parts-labor-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable terminal text or JSON with findings, summary, scope, missing-input advice, and source-row citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; insufficient input returns missing fields and advice rather than findings.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
