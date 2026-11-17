## Description:

Track, analyze, and report business KPIs with targets, status flags, trend analysis, and root cause prompts using configurable JSON files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:

MIT

## Use Case:

Business operators, founders, and teams use this skill to define KPIs, record metric values, generate weekly or monthly status reports, and identify off-track metrics that need investigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: KPI configuration, history, and reports can contain sensitive business performance data stored in the workspace.

Mitigation: Use the skill only in workspaces where local storage of KPI data is acceptable, and review generated reports before sharing them.

Risk: Scheduled reports or messaging integrations can distribute KPI summaries beyond the local workspace.

Mitigation: Review any cron, Slack, Telegram, or similar automation yourself before enabling it, and use explicit requests when saving data or reports.

## Reference(s):

- [KPI Tracker on ClawHub](https://clawhub.ai/1kalin/skills/afrexai-kpi-tracker)
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration, guidance]

**Output Format:** [Markdown reports, JSON configuration and data files, and concise natural-language analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read kpi-config.json, write kpi-data.json, and optionally save reports under reports/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
