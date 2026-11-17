## Description:

Guides an agent in using PortEden's Google Calendar CLI to list, search, read, create, update, delete, and respond to calendar events, with explicit confirmation required before mutating calendar state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porteden](https://clawhub.ai/user/porteden)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to let an agent manage Google Calendar workflows through the PortEden CLI while preserving confirmation gates for event changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party CLI that can access Google Calendar credentials and private calendar data.

Mitigation: Install only from a trusted PortEden release, prefer a pinned and verified version, authorize the narrowest Google Calendar scope, and revoke or log out when access is no longer needed.

Risk: Create, update, delete, and respond actions can change shared calendar state and may notify attendees.

Mitigation: Require explicit user confirmation of the account, calendar, event, attendees, and intended change before running mutating commands.

Risk: Calendar event content can include untrusted text supplied by external organizers or attendees.

Mitigation: Treat summaries, descriptions, locations, and attendee names as untrusted content; summarize them without following embedded instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/porteden/skills/calendar-cli)
- [PortEden homepage](https://porteden.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Encourages compact JSON output via -jc and requires user confirmation before create, update, delete, or respond actions.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
