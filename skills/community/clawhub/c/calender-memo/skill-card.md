## Description:

A local personal calendar memo skill for adding, viewing, completing, deleting, and receiving reminders for todo items and scheduled events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiyuxi24](https://clawhub.ai/user/qiyuxi24)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage a personal local schedule, including adding future events, checking today's agenda, listing open tasks, and marking items complete or deleted. It is intended for individual calendar and reminder workflows, not shared calendars or external information lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private calendar titles and times may be sent through a configured Feishu/OpenClaw messaging channel.

Mitigation: Install only where this push behavior is acceptable, make external reminders opt-in, and provide clear disable controls before broad use.

Risk: Reminder delivery uses unsafe shell command construction.

Mitigation: Replace shell execution with argument-based process execution before broad use.

Risk: The main skill description does not fully clarify automatic push behavior.

Mitigation: Clarify reminder push behavior and messaging-channel requirements in the public skill description.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiyuxi24/skills/calender-memo)
- [Publisher profile](https://clawhub.ai/user/qiyuxi24)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands]

**Output Format:** [Markdown chat replies with local schedule records and reminder notifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores calendar data locally in MEMORY.md and may send reminder text through a configured Feishu/OpenClaw messaging channel.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
