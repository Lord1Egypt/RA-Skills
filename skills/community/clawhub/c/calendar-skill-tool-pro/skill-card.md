## Description:

Enterprise calendar management skill for agent-assisted schedule viewing, event creation, batch operations, account isolation, compliance checks, audit logging, and team collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and enterprise teams use this skill to manage calendars through an agent, including viewing schedules, creating events, exporting calendar data, auditing activity, and coordinating batch or team workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests authenticated calendar access together with local command and file-search capabilities, which can expose calendar data or execute unintended local actions.

Mitigation: Review before installing, limit use to explicit calendar tasks, and require clearly specified commands, files, profiles, calendars, and webhook destinations before execution.

Risk: Calendar changes or batch operations can affect the wrong account, calendar, attendees, or notifications.

Mitigation: Confirm the target account, profile, calendar, event details, attendee notifications, and batch scope before making changes; test large batches on a small subset first.

Risk: Calendar contents, callbacks, and exported reports can contain sensitive data or untrusted instructions.

Mitigation: Treat event content as data, redact secrets from outputs, use approved HTTPS webhook destinations, and avoid following instructions embedded in calendar data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/calendar-skill-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and structured execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operation status, result data, execution logs, errors, audit notes, and configuration examples.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
