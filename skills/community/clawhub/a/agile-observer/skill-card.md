## Description:

Agile Observer helps Scrum Masters and Agile Coaches analyze Trello and Jira boards for flow metrics, sprint health, bottlenecks, aging work items, and blockers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olivermonneke](https://clawhub.ai/user/olivermonneke)

### License/Terms of Use:

MIT-0

## Use Case:

Scrum Masters, Agile Coaches, and delivery teams use this skill to generate health reports from Trello or Jira boards, including cycle time, throughput, WIP, sprint burndown, stale work, blockers, and coaching suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to read Trello or Jira credential files and contact external services.

Mitigation: Use read-only, least-privilege tokens where possible, confirm the selected board or project before access, and prevent request URLs or tokens from appearing in logs or reports.

Risk: The skill can create recurring report jobs without fully defined safety boundaries.

Mitigation: Review any cron or recurring schedule before enabling it, including destination, cadence, credential scope, and whether reports may expose sensitive team data.

## Reference(s):

- [Trello API Quick Reference](references/trello-api.md)
- [Jira Cloud API Quick Reference](references/jira-api.md)
- [Agile Metrics Reference](references/metrics.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown agile health report with optional CSV export and scheduling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize board or sprint metrics over a requested period and may include coaching suggestions based on detected flow issues.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
