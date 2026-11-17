## Description:

Helps agents manage Cal.com scheduling, bookings, event types, availability, and webhooks through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to check availability, manage Cal.com events and bookings, and set up scheduling automations with their authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write actions can change bookings, availability, and event settings.

Mitigation: Start with read-only requests and obtain explicit user approval before each write or new connection.

Risk: Webhooks, triggers, and hosted functions can persistently forward attendee and meeting data.

Mitigation: Review OAuth scopes and confirm each automation, recipient URL, and shared data with the user; remove unneeded flows.

## Reference(s):

- [Cal.com skill release](https://clawhub.ai/byungkyu/skills/cal-com)
- [Maton](https://maton.ai)
- [Cal.com API documentation](https://cal.com/docs/api-reference/v2/introduction)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with shell commands, code, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can change live scheduling data or create ongoing automations.]

## Skill Version(s):

1.2.7 (source: ClawHub release metadata; skill frontmatter says 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
