## Description:

Monitors regulatory changes across SEC, FDA, FINRA, and GDPR and helps generate compliance tracking, policy updates, audit trails, and notifications for financial and healthcare organizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, legal, risk, and operations teams use this skill to track regulatory changes, assess likely business impact, draft policy updates, and route compliance action items. It is aimed at financial services and healthcare workflows that need audit-ready monitoring across multiple regulatory sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects sensitive compliance workflows to external services, including AI analysis and team notifications.

Mitigation: Use dedicated least-privilege API keys and webhooks, and avoid sending confidential customer data or legal strategy into prompts unless approved.

Risk: Generated regulatory interpretations, policy updates, task creation, notifications, or audit evidence may be incomplete or incorrect.

Mitigation: Require qualified human review before external notifications, task creation, policy publication, or audit evidence release.

Risk: Regulatory monitoring can have latency and may miss time-sensitive obligations.

Mitigation: Use official agency alerts and counsel-reviewed compliance processes in parallel for deadline-sensitive matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/complianceradar-ai-monitor)
- [ComplianceRadar documentation](https://github.com/ncreighton/empire-skills/wiki/ComplianceRadar)
- [SEC EDGAR access](https://www.sec.gov/cgi-bin/browse-edgar)
- [openFDA](https://open.fda.gov/)
- [FDA API status](https://api.fda.gov/status.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, policy drafts, checklists, tabular logs, configuration snippets, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured regulatory API keys, an OpenAI API key, Slack webhook access, curl, and jq; compliance-sensitive outputs should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
