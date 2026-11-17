## Description:

Feishu Meeting Reminder helps agents create, view, search, modify, and delete Feishu calendar events with pre-meeting attendee reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramlee77](https://clawhub.ai/user/ramlee77)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users can use this skill to manage Feishu meetings, set attendee reminders before meetings, inspect upcoming meetings, and search or update calendar events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to create, modify, delete, and notify attendees for Feishu calendar events, and the artifact does not document confirmation safeguards for meeting modification or deletion.

Mitigation: Require explicit user confirmation before creating, modifying, deleting, or notifying attendees, and verify event details before destructive calendar actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ramlee77/skills/feishu-meeting-reminder)
- [Publisher profile](https://clawhub.ai/user/ramlee77)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with JSON calendar-action examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ISO 8601/RFC 3339 timestamps, Feishu user_open_id values, attendee lists, reminder offsets, and notification settings.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
