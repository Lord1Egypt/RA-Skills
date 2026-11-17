## Description:

Email To Calendar helps an agent find meetings, appointments, RSVPs, and deadlines in Gmail messages, present them for confirmation, and create or update Google Calendar events through a configured Google Calendar tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonimelisma](https://clawhub.ai/user/tonimelisma)

### License/Terms of Use:

MIT

## Use Case:

Individuals, families, and teams use this skill to turn email invitations, appointments, RSVP requests, and deadlines into reviewed Google Calendar entries without manually copying event details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports persistent heartbeat behavior that can continue scanning and modifying email after setup.

Mitigation: Install only if recurring inbox checks are intended; review HEARTBEAT.md and remove the Email Scanning or Pending Calendar Invites sections to disable that behavior.

Risk: The skill can read Gmail, modify Gmail labels, manage Google Calendar events, send optional deadline emails, and write local tracking logs.

Mitigation: Use a dedicated or least-privileged Google account and review the selected calendar, email mode, attendees, and deadline notification settings before use.

Risk: Default email handling can mark processed messages as read, archive them, and auto-process calendar reply notifications.

Mitigation: Set email_handling.mark_read, email_handling.archive, or email_handling.auto_dispose_calendar_replies to false when those automatic actions are not desired.

## Reference(s):

- [Setup Guide](SETUP.md)
- [CLI Reference](references/gog-commands.md)
- [Extraction Patterns](references/extraction-patterns.md)
- [Workflow Example](references/workflow-example.md)
- [gog CLI](https://github.com/tonimelisma/gogcli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured event summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before calendar creation or updates; can write local tracking, pending invite, activity, and changelog JSON through its scripts.]

## Skill Version(s):

1.13.3 (source: SKILL.md frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
