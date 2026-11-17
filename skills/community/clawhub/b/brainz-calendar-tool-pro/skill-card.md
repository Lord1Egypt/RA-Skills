## Description:

Google 日历专业版 helps agents manage calendar workflows, including multi-calendar synchronization, meeting scheduling, conflict detection, team availability analysis, and batch recurring-event operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and enterprise teams use this skill to have an agent inspect, create, export, and coordinate calendar events across scheduling workflows. It is aimed at calendar operations that benefit from natural-language assistance, batch handling, and team availability analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad agent routing and command execution capabilities beyond tightly scoped calendar use.

Mitigation: Narrow activation to calendar tasks and require confirmation before running shell commands or making calendar changes.

Risk: Calendar creates, deletes, batch edits, exports, and attendee notifications can affect other people or expose scheduling data.

Mitigation: Require user confirmation for creates, deletes, batch changes, exports, and attendee notifications before execution.

Risk: Webhook and external calendar service configuration can send data to untrusted destinations.

Mitigation: Configure only trusted HTTPS webhook destinations and trusted calendar services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/brainz-calendar-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose calendar reads, writes, exports, batch changes, and webhook configuration that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
