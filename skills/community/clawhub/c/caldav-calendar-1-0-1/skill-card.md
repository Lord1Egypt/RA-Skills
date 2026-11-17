## Description:

Sync and query CalDAV calendars (iCloud, Google, Fastmail, Nextcloud, etc.) using vdirsyncer + khal. Works on Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigdonuts0](https://clawhub.ai/user/bigdonuts0)

### License/Terms of Use:


## Use Case:

Developers and calendar users on Linux use this skill to set up vdirsyncer and khal for syncing, querying, creating, editing, and deleting CalDAV calendar events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example setup can store a CalDAV password in a local password file.

Mitigation: Use a revocable app-specific password, restrict the file to the user account, keep it out of backups and source control, and revoke or rotate it if exposed.

Risk: The skill can help an agent read, create, edit, delete, and sync calendar events.

Mitigation: Review proposed calendar changes before syncing them to the remote calendar service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigdonuts0/skills/caldav-calendar-1-0-1)
- [iCloud CalDAV endpoint](https://caldav.icloud.com/)
- [Fastmail CalDAV endpoint example](https://caldav.fastmail.com/dav/calendars/user/EMAIL/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux with vdirsyncer and khal installed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
