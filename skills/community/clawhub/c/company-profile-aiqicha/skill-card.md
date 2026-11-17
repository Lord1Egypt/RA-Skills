## Description:

Produces company intelligence reports and two-company comparisons using Chinese tender and award records, supplier relationships, competitor overlap, and sourced public information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Business researchers, procurement teams, and sales teams use the skill to assess a Chinese company's tendering history, customers, suppliers, competitors, and sourced public risk signals, or to compare two companies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company queries and limited device-registration data may be sent to the ZLBX service.

Mitigation: Review its data practices before use; require explicit consent before optional auto-registration or supply an existing API key to avoid registration.

Risk: An API key is stored locally and lookups consume paid quota or credits.

Mitigation: Protect the local key, check the projected credit cost before running reports, and approve any additional lookups.

Risk: Contact lookups may disclose phone numbers, and public-risk findings can be misleading without context.

Mitigation: Avoid bulk contact harvesting or unsolicited outreach; cite public sources, distinguish facts from inference, and verify consequential claims.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dragonzu/skills/company-profile-aiqicha)
- [Skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Company intelligence workflow](references/workflow.md)
- [API quick reference](references/api-quick.md)
- [Report templates](references/report-template.md)
- [Account registration and privacy](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML reports]

**Output Format:** [Markdown report in chat with an optional shareable HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-company and two-company reports; figures and public-risk claims should include time ranges and source links.]

## Skill Version(s):

1.0.6 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
