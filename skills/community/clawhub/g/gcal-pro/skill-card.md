## Description:

Google Calendar integration for Clawdbot that lets users view, create, edit, delete, and search calendar events, check availability, and generate morning briefs through natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bilalmohamed187-cpu](https://clawhub.ai/user/bilalmohamed187-cpu)

### License/Terms of Use:

Proprietary

## Use Case:

External Clawdbot users use this skill to manage Google Calendar from conversation, including checking schedules and free time, adding or changing events for Pro users, and receiving daily briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write operations can create, change, or delete Google Calendar events even when confirmation is not actually enforced.

Mitigation: Require explicit user approval before running create, quick-add, update, or delete actions, and test first with a non-critical calendar.

Risk: OAuth credential and token files grant access to the user's calendar data.

Mitigation: Keep credential files out of chats, logs, and shared folders; revoke and re-authenticate credentials if they may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bilalmohamed187-cpu/skills/gcal-pro)
- [Google Cloud Project Setup Guide](docs/GOOGLE_CLOUD_SETUP.md)
- [Google Calendar API Quick Reference](references/api-quickref.md)
- [Clawdbot](https://clawd.bot)
- [Google Cloud Console](https://console.cloud.google.com)
- [Google Calendar API](https://www.googleapis.com/calendar/v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown text with inline shell commands and calendar operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google OAuth credentials; Pro tier enables create, update, delete, and morning brief actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
