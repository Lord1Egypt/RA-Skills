## Description:

Calendar and task management via CalDAV protocol. Query, create, edit, and delete calendar events and todos. Free/busy query, multi-account support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gzlicanyi](https://clawhub.ai/user/gzlicanyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage CalDAV calendars and task lists across supported providers, including querying availability, listing calendars, and creating, updating, or deleting events and todos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles reusable calendar credentials and cached private calendar or task data.

Mitigation: Install only for trusted CalDAV servers, prefer provider presets or HTTPS-only custom endpoints, use app-specific passwords where available, and remove cached data and plaintext credentials when no longer needed.

Risk: The skill can create, modify, and delete remote calendar events and todos.

Mitigation: Review requested write operations before execution and use the narrowest suitable account or calendar scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gzlicanyi/skills/caldav-sync)
- [Publisher profile](https://clawhub.ai/user/gzlicanyi)
- [Google App Passwords](https://myaccount.google.com/apppasswords)
- [Related imap-smtp-email skill](https://clawhub.ai/gzlicanyi/imap-smtp-email)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON command output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write remote calendar/task data and local CalDAV configuration or cache files.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
