## Description:

Automated data reporting and dashboard generation that helps agents connect to databases, APIs, spreadsheets, and storage, then generate scheduled reports, dashboards, charts, alerts, and delivery instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuczy](https://clawhub.ai/user/fuczy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business teams use this skill to design automated business reporting workflows that pull data from operational systems, create PDF, PowerPoint, Excel, dashboard, and alert outputs, and distribute reports through email, Slack, Teams, or webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle sensitive business, financial, customer, and operational data from many sources.

Mitigation: Use least-privilege, preferably read-only credentials and restrict each connector to only the data needed for the intended report.

Risk: Example workflows distribute reports through email, Slack, Teams, webhooks, and public dashboard URLs.

Mitigation: Review every destination before scheduling or sending reports, and avoid public URLs for confidential outputs unless access controls are added.

Risk: Completed configuration files may contain credentials, service-account paths, webhook URLs, or report recipients.

Mitigation: Keep generated configuration and credential files out of source control and store secrets in an approved secret manager.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fuczy/skills/clawd-data-reporter)
- [Skill Homepage](https://clawhub.com/skills/data-reporter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated report definitions, data-source configuration, scheduled workflow commands, delivery channels, dashboards, alerts, and exported files such as PDF, PowerPoint, Excel, and Google Sheets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
