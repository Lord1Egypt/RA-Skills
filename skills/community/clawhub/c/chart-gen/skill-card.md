## Description:

Creates charts, dashboards, diagrams, Gantt charts, presentations, reports, and spreadsheet or data analyses through ChartGen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chartgen-ai](https://clawhub.ai/user/chartgen-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit confirmed visualization, report, presentation, and spreadsheet-analysis requests to ChartGen and return summaries, generated artifacts, and edit links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell execution can expose users to command injection if untrusted query text is interpolated into a shell command.

Mitigation: Pass confirmed user text as an argument through a safe process invocation and avoid building shell command strings from untrusted input.

Risk: Changing CHARTGEN_API_URL can send requests, files, and credentials-adjacent workflow data to an untrusted endpoint.

Mitigation: Use the default ChartGen HTTPS endpoint or set CHARTGEN_API_URL only to a trusted HTTPS service.

Risk: Uploaded files and request content are processed by an external ChartGen service.

Mitigation: Use non-sensitive data unless ChartGen's processing and retention practices are trusted for the intended use.

Risk: Downloaded charts, spreadsheets, and presentation artifacts come from an external service.

Mitigation: Treat downloaded artifacts as untrusted files and scan or review them before opening, sharing, or using them in downstream workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chartgen-ai/skills/chart-gen)
- [Publisher Profile](https://clawhub.ai/user/chartgen-ai)
- [ChartGen Chat and API Setup](https://chartgen.ai/chat)
- [Skill Upgrade Procedure](references/upgrade-skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with JSON tool results, local artifact paths, and external edit URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return chart image paths, spreadsheet or PPT download paths, task status JSON, and ChartGen edit URLs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
