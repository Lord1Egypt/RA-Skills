## Description:

Morning Briefing generates and sends scheduled morning project progress briefings from memory logs, WPS calendar events, and related project status sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangwanxia](https://clawhub.ai/user/wangwanxia)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and project operators use this skill to receive a daily 09:00 Asia/Shanghai briefing or request a current project status summary assembled from approved memory logs, WPS calendar entries, Ezone cards, and pressure-test status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring unattended delivery can expose memory, log, calendar, or project status information to an unintended audience.

Mitigation: Bind an explicit recipient, confirm the schedule, limit inputs to approved briefing sections, and document how to disable or remove the cron task.

Risk: Briefings may include sensitive operational details from project logs or calendar entries.

Mitigation: Apply redaction rules before sending and restrict the skill to approved data sources.

Risk: Calendar access failures or weakly scoped delivery routes can produce incomplete or misdirected briefings.

Mitigation: Validate routing before deployment and make optional calendar failures visible in operational review when completeness matters.

## Reference(s):

- [Morning Briefing Skill Page](https://clawhub.ai/wangwanxia/skills/daily-briefing-wps)
- [Morning Briefing Template](references/template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefing text with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed briefing structure for greeting, project progress, pending items, and calendar events.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
