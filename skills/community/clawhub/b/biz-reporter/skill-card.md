## Description:

Biz Reporter helps agents pull business metrics from analytics, revenue, social, CRM, and custom data sources into daily KPI snapshots, weekly marketing reports, monthly business reviews, and ad-hoc business intelligence summaries with trend detection and anomaly alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ariktulcha](https://clawhub.ai/user/ariktulcha)

### License/Terms of Use:


## Use Case:

Business owners, operators, marketers, and growth teams use this skill to gather authorized metrics from tools such as GA4, Search Console, Stripe, social platforms, HubSpot, Airtable, spreadsheets, and CSV files, then generate recurring or ad-hoc business reports. It is suited for KPI snapshots, marketing performance reviews, revenue summaries, search and social reporting, sales pipeline summaries, and natural-language questions about business performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may access sensitive business metrics from analytics, revenue, CRM, social, spreadsheet, or custom data sources.

Mitigation: Connect only authorized accounts, scope credentials to the reports needed, and configure credentials through secure environment variables.

Risk: Scheduled or external report delivery could send confidential metrics to the wrong destination.

Mitigation: Confirm cron schedules and verify Slack, email, Notion, or Discord destinations before enabling automated delivery.

Risk: Reports may include more data sources than a team needs for a particular workflow.

Mitigation: Limit connected sources and generated report sections to the intended business use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ariktulcha/skills/biz-reporter)
- [Publisher profile](https://clawhub.ai/user/ariktulcha)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, chat responses, delivery instructions, and scheduling or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include daily, weekly, monthly, or custom report structures and delivery guidance for Slack, email, Notion, Discord, or workspace files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
