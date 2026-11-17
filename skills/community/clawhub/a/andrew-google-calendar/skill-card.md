## Description:

Andrew Google Calendar helps an agent use OAuth-authorized Google Calendar API access to list calendars and create, update, move, or delete calendar events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibluewind](https://clawhub.ai/user/ibluewind)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to connect an agent to Google Calendar for event lookup and calendar event management. It is suited for workflows where full Google Calendar read/write OAuth access is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses full Google Calendar read/write access.

Mitigation: Use it only with Google accounts where broad calendar access is acceptable, and review requested calendar changes before execution.

Risk: The OAuth token is persisted with pickle-based storage.

Mitigation: Avoid running the skill until token storage is changed to a safer serialized format and existing token files are protected or rotated.

Risk: Calendar delete and move operations can change user data without built-in confirmation.

Mitigation: Require explicit user confirmation and a target event preview before destructive or cross-calendar operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ibluewind/skills/andrew-google-calendar)
- [Google Calendar OAuth scope](https://www.googleapis.com/auth/calendar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with Python examples and shell command snippets; runtime helpers return Google Calendar API event and calendar objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Google OAuth client secret and stores a local OAuth token for Calendar API access.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
