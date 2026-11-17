## Description:

Microsoft 365 / Outlook CLI for calendar and email. Use when managing Outlook calendar (view, create, update, delete events, find meeting times, respond to invitations), sending/reading emails, or searching for people/rooms in the organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foeken](https://clawhub.ai/user/foeken)

### License/Terms of Use:


## Use Case:

Employees and agents use this skill to manage Microsoft 365 Outlook mail, calendars, invitations, meeting times, people, and rooms through the Clippy CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate with authenticated access to Microsoft 365 mailbox and calendar data.

Mitigation: Use a dedicated or contained profile where possible and install only after reviewing the selected release.

Risk: The skill can propose actions that send mail, reply or forward messages, delete events, move mail, or download attachments.

Mitigation: Require explicit user confirmation before executing actions that modify mailbox or calendar state or retrieve attachments.

Risk: Persistent keepalive can extend authenticated browser access beyond a single task.

Mitigation: Avoid persistent keepalive unless it is needed and monitor the session health file when keepalive is enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foeken/skills/clippy)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clippy binary and an authenticated Microsoft 365 browser session.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
