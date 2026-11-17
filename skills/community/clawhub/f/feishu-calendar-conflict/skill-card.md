## Description:

Detects Feishu calendar scheduling conflicts before meetings by checking attendee free/busy status and suggesting available time slots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramlee77](https://clawhub.ai/user/ramlee77)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and scheduling assistants use this skill to check Feishu attendee availability, identify conflicts, and propose open meeting windows before creating calendar events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query coworkers' Feishu free/busy information and describes meeting creation without clear consent or scoping safeguards.

Mitigation: Use it only for legitimate scheduling, confirm the requested attendees and time range before querying multiple calendars, and require explicit user confirmation before creating a meeting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ramlee77/skills/feishu-calendar-conflict)

## Skill Output:

**Output Type(s):** [guidance, API Calls, configuration]

**Output Format:** [Markdown guidance with JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference ISO 8601/RFC 3339 time ranges, Feishu user open IDs, busy slots, free slots, and conflict warnings.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
