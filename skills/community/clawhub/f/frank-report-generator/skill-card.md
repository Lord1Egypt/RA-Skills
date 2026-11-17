## Description:

Automated sales and performance report generator for retail store managers that creates daily, weekly, monthly, and on-demand reports from configured POS/ERP or manual input data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangwei-frank](https://clawhub.ai/user/fangwei-frank)

### License/Terms of Use:

MIT-0

## Use Case:

Store managers and retail operators use this skill to generate scheduled and on-demand sales performance reports, compare KPIs against targets and prior periods, surface anomalies, and receive specific recommended actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive retail business data, including revenue, inventory, anomalies, and staff-performance sections.

Mitigation: Limit report_config data sources to approved POS/ERP connections and treat generated reports as sensitive business data.

Risk: Scheduled delivery can send reports to unintended recipients or channels if configuration is too broad.

Mitigation: Review delivery_channel, recipients, and enabled schedules before installation and whenever report distribution changes.

Risk: Reports generated from partial or missing data can lead to incomplete business decisions.

Mitigation: Clearly mark missing sections, use manual input only when approved, and validate important anomalies against source systems before acting.

## Reference(s):

- [Metric Definitions](references/metric-definitions.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports with tables, KPI summaries, anomaly notes, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports depend on configured POS/ERP data, manual input, delivery channel, recipients, report period, and metric selection.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-03-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
