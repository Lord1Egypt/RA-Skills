## Description:

Extracts calendar events and deadlines from email, presents candidates for review, and creates or updates calendar entries with duplicate detection, tracking, reminders, and undo support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a2mus](https://clawhub.ai/user/a2mus)

### License/Terms of Use:

MIT

## Use Case:

External users and personal or work productivity agents use this skill to turn event invitations, forwarded emails, and deadline emails into reviewed calendar entries and reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires broad access to read Gmail content and create, update, or delete calendar events.

Mitigation: Install only for accounts and calendars where that access is acceptable, and review the configured Gmail account, calendar ID, attendee settings, and provider setup before use.

Risk: Direct inbox scanning, heartbeat integration, auto-disposition, and calendar reply processing can repeatedly inspect email and mutate mailbox state.

Mitigation: Prefer forwarded-email mode for narrower scope, and review or disable direct scanning, heartbeat checks, mark-read/archive behavior, and automatic calendar-reply disposition before deployment.

Risk: The authoritative security scan reports a command-injection bug in event tracking validation.

Mitigation: Fix the event tracking validation path before running validation workflows on untrusted or shared state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/a2mus/skills/doro-email-to-calendar)
- [Setup Guide](SETUP.md)
- [Bootstrap Guide](BOOT.md)
- [CLI Reference](references/gog-commands.md)
- [Extraction Patterns](references/extraction-patterns.md)
- [Workflow Example](references/workflow-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash commands and JSON configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update calendar events, mark or archive emails, write local JSON tracking records, and send deadline notification emails when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact package.json and changelog also contain 1.13.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
