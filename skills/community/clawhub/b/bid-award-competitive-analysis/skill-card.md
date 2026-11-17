## Description:

Analyzes company bidding awards, customers, suppliers, competitors, and public risk signals in single-company or two-company reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement and business teams use this skill to investigate a company's bidding track record and competitive position, or compare two companies using bid records and cited public information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Report queries consume account credits.

Mitigation: Disclose estimated credits before analysis and ask before exceeding the query budget.

Risk: Optional first-use registration sends a hashed MAC-derived device identifier.

Mitigation: Request consent before registration, or configure ZLBX_API_KEY to skip device-feature collection.

Risk: The API key is stored locally and reports can be shared.

Mitigation: Protect the local credential and review reports and their links before sharing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhiliaobiaoxun/skills/bid-award-competitive-analysis)
- [Analysis workflow](artifact/references/workflow.md)
- [API quick reference](artifact/references/api-quick.md)
- [Report template](artifact/references/report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML report]

**Output Format:** [Conversational report with optional shareable HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-company or two-company comparison with cited findings and stated data gaps.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
