## Description:

Calendar Manager helps an agent read schedules, create or update calendar events, set reminders, find free time, and summarize upcoming events through calendar tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackeven02](https://clawhub.ai/user/jackeven02)

### License/Terms of Use:


## Use Case:

Users and agent operators use this skill to inspect calendars, add or adjust events, create reminders, and summarize upcoming schedule items across supported calendar tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar access and event changes can expose or alter sensitive schedule information.

Mitigation: Grant calendar access only in environments where that exposure is acceptable, and require explicit approval before every event creation, modification, deletion, or reminder email.

Risk: Email-derived scheduling workflows can convert untrusted or misleading messages into calendar events.

Mitigation: Avoid automatic event creation from untrusted emails and have the user confirm the event details before writing to a calendar.

Risk: Persistent reminder or scheduled-task examples can continue running after the user no longer expects them.

Mitigation: Create scheduled tasks only after user approval and provide a clear way to inspect and remove them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackeven02/skills/calendar-manager)
- [Calendar management reference resources](artifact/references/resources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose calendar reads, event changes, reminders, and scheduling workflows that require user approval before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
