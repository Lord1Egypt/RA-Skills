## Description:

Ask Data helps agents answer Chinese natural-language questions by reading user-approved Excel files, converting requests into data queries, and returning structured results, visualizations, and insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15028191702](https://clawhub.ai/user/15028191702)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to let an agent inspect Excel workbook structure after user confirmation, translate Chinese data questions into query JSON, execute local tabular analysis, and summarize the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local Excel files selected by the user, and workbook samples or query results may be exposed back to the agent.

Mitigation: Use only with files the user explicitly approves, and avoid workbooks containing sensitive rows when showing sample data or results to the agent would be inappropriate.

Risk: Very large or untrusted workbooks may be slow or may trigger parsing errors during local analysis.

Mitigation: Prefer trusted, reasonably sized workbooks and warn users before processing very large files.

## Reference(s):

- [Data Query Examples](references/query-examples.md)
- [ClawHub skill page](https://clawhub.ai/15028191702/skills/ask-data)
- [Publisher profile](https://clawhub.ai/user/15028191702)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with JSON query specifications and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tabular results, chart recommendations, data insights, and structured JSON returned by helper scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
