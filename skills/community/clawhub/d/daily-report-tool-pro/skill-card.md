## Description:

日报生成器专业版 helps agents generate Chinese daily reports from dates, highlights, blockers, and team inputs, with support for aggregation, trend analysis, templates, archiving, and workflow configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, and workflow operators use this skill to draft, aggregate, and manage Chinese daily work reports. It is intended for report generation workflows that may connect to repositories, calendars, task systems, files, APIs, and approved notification endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad agent authority across files, commands, APIs, credentials, and external callbacks.

Mitigation: Restrict it to specific repositories, calendars, task systems, output folders, and approved webhook domains before use.

Risk: Shell command, callback, or credential use can create avoidable exposure if enabled broadly.

Mitigation: Avoid enabling Bash or callbacks unless needed, and provide only connector-scoped credentials with clear limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/daily-report-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and structured guidance with inline code, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write report files, produce logs or summaries, and describe API, webhook, or batch-processing configuration when enabled by the user.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
