## Description:

gcal-pro integrates Google Calendar so agents can view schedules, search calendars, find availability, and, with Pro access, create, update, delete events and generate morning briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bilalmohamed187-cpu](https://clawhub.ai/user/bilalmohamed187-cpu)

### License/Terms of Use:

Proprietary

## Use Case:

External ClawHub and Clawdbot users use this skill to let an agent inspect Google Calendar schedules, answer availability questions, and prepare calendar summaries. Users with Pro access can also ask the agent to create, update, or delete calendar events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pro write operations can change or delete Google Calendar events without reliable confirmation enforcement.

Mitigation: Avoid create, update, and delete operations until confirmation handling is fixed and reviewed; require explicit user confirmation before any calendar mutation.

Risk: The skill requires Google Calendar OAuth credentials and stores local access tokens.

Mitigation: Keep client_secret.json and token.json private, do not print or share them, and store them only in the configured local directory with restrictive permissions.

Risk: Installing dependencies without review can introduce supply-chain risk.

Mitigation: Install dependencies in an isolated environment and use reviewed or pinned package versions before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bilalmohamed187-cpu/skills/gcal-pro-calendar)
- [Google Cloud Project Setup Guide](artifact/docs/GOOGLE_CLOUD_SETUP.md)
- [Google Calendar API Quick Reference](artifact/references/api-quickref.md)
- [Google Calendar API](https://www.googleapis.com/calendar/v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and structured calendar summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Google OAuth credentials; Pro write actions can create, update, or delete calendar events.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
