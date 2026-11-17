## Description:

Produces single-company intelligence reports or two-company comparisons from Chinese procurement records, covering business focus, customers, suppliers, awards, competitors, and sourced public-risk information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, sales, and vendor-review teams use the skill to assess a company's public tender activity and market position, or to compare two companies using sourced records.

### Deployment Geography for Use:

Global (analysis focuses on Chinese procurement data)

## Known Risks and Mitigations:

Risk: The skill reads or stores an API credential in local configuration.

Mitigation: Review access to ~/.zlbx/config.json and keep API keys out of reports and shared conversations.

Risk: Trial registration sends operating-system and CPU details plus a MAC-address hash to the vendor.

Mitigation: Require explicit consent before registration, or use an existing API key to skip it.

Risk: Company queries consume credits and may present billing links.

Mitigation: Confirm the estimated credit cost before a report and verify vendor links before paying.

Risk: Local HTML reports may contain signed vendor access links that remain usable when shared.

Mitigation: Review and limit distribution of exported reports and their embedded links.

## Reference(s):

- [ClawHub release](https://clawhub.ai/dragonzu/skills/company-intel-qichamao)
- [Skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Analysis workflow](references/workflow.md)
- [Report templates](references/report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML reports]

**Output Format:** [Sourced Markdown report with an optional local HTML copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports identify data gaps and may include signed links to company and procurement records.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
