## Description:

定时助手 helps agents convert natural-language scheduling requests into cron-style task commands, templates, and task-management actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation teams use this skill to create, inspect, pause, resume, delete, and optimize scheduled reminders, reports, health checks, and workflow tasks from natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad unrelated activation text may encourage use for translation, generic file processing, or unrelated API work.

Mitigation: Install and invoke the skill only for explicit cron, reminder, or workflow scheduling requests.

Risk: Persistent task mutation commands can pause, resume, delete, or bulk-modify scheduled jobs.

Mitigation: Review generated commands before execution and require confirmation for deletes and bulk actions.

Risk: Natural-language scheduling requests can be ambiguous and may produce the wrong time or recurrence.

Mitigation: Confirm interpreted schedules, time zones, and generated cron-style parameters before creating or changing tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cron-assist)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and structured task summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent scheduling changes; generated commands should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
