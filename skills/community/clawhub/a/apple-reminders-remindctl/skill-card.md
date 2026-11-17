## Description:

Manage Apple Reminders via the remindctl CLI. Use for time-anchored or place-anchored tracking that doesn't belong on the calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luisbueno](https://clawhub.ai/user/luisbueno)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to create, review, edit, and complete Apple Reminders through remindctl for time-based, recurring, and location-based tasks that should not be calendar events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write to Apple Reminders through remindctl after Reminders Automation access is granted.

Mitigation: Review requested reminder changes before execution and keep the documented non-interactive JSON command pattern for auditable results.

Risk: Selected reminder details may be copied into an Open Brain store when they are treated as durable context.

Mitigation: Require explicit confirmation before secondary storage of sensitive reminder details, especially health-related or location-related items.

Risk: Editing or completing reminders by unstable indexes could affect the wrong item.

Mitigation: Use stable reminder ID prefixes for edits and completion, and rerun JSON reads when an ID prefix is ambiguous.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and human-readable summaries parsed from JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses non-interactive remindctl commands with JSON output; can change the user's iCloud Reminders when executed by an authorized agent.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
