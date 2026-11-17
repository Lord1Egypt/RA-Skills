## Description:

Produces single-company or side-by-side due-diligence reports using procurement awards, customer relationships, competitor activity, and sourced public-risk information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, procurement teams, and potential business partners use this skill to assess a company's operating activity and customer concentration through public bidding records, or compare two companies before a transaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic account creation collects a hashed device identifier.

Mitigation: Use your own ZLBX_API_KEY to skip registration, or review the requested device data and consent before creating an account.

Risk: Persistent API credentials and contact phone data may be exposed if shared inappropriately.

Mitigation: Protect local credentials, do not include API keys in reports, and limit access to contact information.

Risk: Shareable HTML reports may contain signed access links to source records.

Mitigation: Review embedded links and recipients before distributing a report.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhiliaobiaoxun/skills/bidding-due-diligence)
- [Skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Due-diligence workflow](artifact/references/workflow.md)
- [API quick reference](artifact/references/api-quick.md)
- [Report templates](artifact/references/report-template.md)
- [Account registration guidance](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML report]

**Output Format:** [Markdown report and optional shareable HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-company or two-company comparison; findings cite source records and identify data gaps.]

## Skill Version(s):

1.0.6 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
