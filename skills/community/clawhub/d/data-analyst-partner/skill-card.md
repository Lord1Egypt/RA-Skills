## Description:

Act as a Grafana-first product and business data analysis partner for an app team.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwqcode](https://clawhub.ai/user/qwqcode)

### License/Terms of Use:

MIT-0

## Use Case:

Product, content, and operations teams use this skill to interpret Grafana dashboard metrics, request dimensional splits, plan SQL-backed follow-up analysis, draft daily reports, and clarify new dashboard requirements before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may surface sensitive dashboard or ClickHouse-backed business metrics if used outside approved analytics contexts.

Mitigation: Install and use it only where the agent already has approved access to the relevant Grafana dashboards, ClickHouse data, and business metrics.

Risk: Ambiguous metric definitions or premature direct SQL use could produce misleading analysis.

Mitigation: Prefer existing Grafana dashboards and panels first, name the data source path used, and call out unclear definitions or caveats before recommending follow-up.

## Reference(s):

- [Daily Report Template](references/daily-report-template.md)
- [New Dashboard Confirmation Checklist](references/dashboard-confirmation.md)
- [Data Analyst Partner on ClawHub](https://clawhub.ai/qwqcode/skills/data-analyst-partner)
- [qwqcode Publisher Profile](https://clawhub.ai/user/qwqcode)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown text with concise conclusions, evidence, observations, caveats, and recommended next checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dashboard requirement summaries, daily report sections, and source-path attribution for dashboard, panel, datasource query, or direct ClickHouse evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
