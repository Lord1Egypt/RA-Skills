## Description:

Generates daily, weekly, monthly, and yearly reports on agent usage, token consumption, costs, task types, skill use, and automation runs from local data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elisabeth15501](https://clawhub.ai/user/elisabeth15501)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to review local agent usage over a chosen period, including token consumption, costs, task and skill patterns, and automation outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags potentially broad data collection, file writes, and unsafe handling of report content.

Mitigation: Review the selected data sources and output destination before running the skill, and inspect HTML reports before sharing them.

Risk: Report content may be inaccurate, and some token usage or cost figures are estimates.

Mitigation: Check important figures against source records and official billing, especially for sources that estimate tokens locally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elisabeth15501/skills/agent-analytics-report)
- [Adapter and data source guide](docs/ADAPTERS.md)
- [Data source reference](references/data_sources.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML, JSON]

**Output Format:** [Markdown, HTML, or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize locally collected usage for a selected time period; some token values and costs may be estimates.]

## Skill Version(s):

1.9.15 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
