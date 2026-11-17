## Description:

Finds expiring procurement contracts and related pre-tender opportunities, then ranks them by urgency, value, and fit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and business-development teams use this skill to identify upcoming contract renewals, incumbent suppliers, planned projects, and procurement intentions, then prioritize follow-up opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opportunity scans can consume account credits.

Mitigation: Review the estimated credit cost before starting and approve additional calls before exceeding the stated budget.

Risk: An API key may be stored persistently in a local configuration file.

Mitigation: Protect the local credentials file and avoid sharing API keys in chat or reports.

Risk: Trial registration sends a hashed MAC-derived device identifier to the service.

Mitigation: Only proceed after explicit consent, or supply an existing API key to skip registration.

Risk: Generated reports and chat output can include signed access links.

Mitigation: Share reports and links only with trusted recipients; do not forward signed links publicly.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/expiring-contract-renewal-finder)
- [Workflow and ranking rules](artifact/references/workflow.md)
- [API quick reference](artifact/references/api-quick.md)
- [Report template](artifact/references/report-template.md)
- [Account registration and credentials](artifact/references/auto-register.md)
- [Zhiliaobiaoxun skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Markdown, HTML files, Guidance]

**Output Format:** [Ranked Markdown opportunity list with an HTML report in full-scan mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links, priority rationale, and suggested follow-up actions.]

## Skill Version(s):

1.0.8 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
