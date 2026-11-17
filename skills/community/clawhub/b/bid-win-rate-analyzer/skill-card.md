## Description:

Analyzes a specific tender against historical procurement and award data to support bid decisions, competitor assessment, pricing, and risk review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

Bid and procurement teams assess whether to pursue a specific tender, compare likely competitors, review historical prices, and identify qualification or disqualification risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis calls may consume paid API credits.

Mitigation: Tell users the expected credit usage before a full analysis and obtain approval before exceeding the planned call budget.

Risk: An API key may be stored locally.

Mitigation: Prefer a user-provided ZLBX_API_KEY and protect any locally stored credentials.

Risk: Auto-registration hashes a device MAC address for account deduplication.

Mitigation: Obtain explicit consent before registration, or use an existing API key to avoid registration.

Risk: Exported reports may include signed links granting access to source material.

Mitigation: Treat HTML reports as sensitive and limit distribution to intended recipients.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhiliaobiaoxun/skills/bid-win-rate-analyzer)
- [知了标讯 skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Analysis workflow](artifact/references/workflow.md)
- [Report template](artifact/references/report-template.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML]

**Output Format:** [Markdown decision report in chat; shareable HTML report for full analyses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a bid recommendation, confidence level, supporting data, and source links.]

## Skill Version(s):

1.0.9 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
