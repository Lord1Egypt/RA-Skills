## Description:

Sync and query CalDAV calendars (iCloud, Google, Fastmail, Nextcloud, etc.) using vdirsyncer + khal. Works on Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asleep123](https://clawhub.ai/user/asleep123)

### License/Terms of Use:


## Use Case:

Developers and calendar users use this skill to set up Linux CalDAV synchronization and guide an agent in querying, searching, creating, editing, and deleting calendar events with vdirsyncer and khal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: vdirsyncer and khal can access and modify calendar data.

Mitigation: Install only when that calendar access is acceptable, and review create, edit, and delete commands before execution.

Risk: Provider passwords or app passwords may be stored or fetched locally.

Mitigation: Store credentials carefully, restrict access to password files or stores, and avoid exposing secrets in shared configuration.

Risk: Sync conflict settings can overwrite calendar changes.

Mitigation: Review vdirsyncer conflict_resolution settings before syncing and confirm the intended source of truth.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asleep123/skills/caldav-calendar)
- [iCloud CalDAV endpoint](https://caldav.icloud.com/)
- [Fastmail CalDAV endpoint pattern](https://caldav.fastmail.com/dav/calendars/user/EMAIL/)
- [Nextcloud CalDAV endpoint pattern](https://YOUR.CLOUD/remote.php/dav/calendars/USERNAME/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Linux; requires vdirsyncer and khal.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
