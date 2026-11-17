## Description:

Simple task intake, reminder, and completion check-in flow for public-safe daily coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoma970](https://clawhub.ai/user/guoma970)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a same-day task reminder loop that records provided tasks, confirms a start time, sends short reminders, checks completion, and asks for sender approval before any reward or follow-up note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be made available for automatic use in task-reminder contexts.

Mitigation: Confirm that automatic use is acceptable before installation and keep the flow limited to generic, same-day task reminders.

Risk: Users could enter identifying or sensitive details while describing tasks or schedules.

Mitigation: Avoid real names, school or health details, account IDs, group names, private schedules tied to identity, and other sensitive personal information.

Risk: The assistant could appear to approve rewards or follow-up notes without sender approval.

Mitigation: Require sender approval before any reward or follow-up note and do not promise rewards directly to the recipient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoma970/skills/daily-task-checkin)
- [README](artifact/README.md)
- [Sender example](artifact/examples/sender-example.md)
- [Reminder example](artifact/examples/reminder-example.md)
- [Completion example](artifact/examples/completion-example.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Text]

**Output Format:** [Short natural-language reminder and check-in messages, with Markdown examples in the artifact documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, persistence, credential use, or hidden data handling was identified by the security evidence.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
