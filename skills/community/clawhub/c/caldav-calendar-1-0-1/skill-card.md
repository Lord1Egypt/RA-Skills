## Description: <br>
Sync and query CalDAV calendars (iCloud, Google, Fastmail, Nextcloud, etc.) using vdirsyncer + khal on Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BIGDONUTS0](https://clawhub.ai/user/BIGDONUTS0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and calendar users use this skill to configure vdirsyncer and khal, sync CalDAV calendars locally, and view, search, create, edit, or delete events from an agent-assisted workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help create, edit, or delete calendar events after a CalDAV account is configured. <br>
Mitigation: Review create, edit, and delete actions before syncing changes back to the provider. <br>
Risk: Calendar credentials may be stored in a local password file for vdirsyncer. <br>
Mitigation: Use provider app passwords or limited-scope credentials and protect the local password file. <br>
Risk: Deleting the khal cache can remove local cached calendar data used for troubleshooting stale results. <br>
Mitigation: Treat cache deletion as a troubleshooting step and sync again after clearing stale local data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/BIGDONUTS0/caldav-calendar-1-0-1) <br>
- [iCloud CalDAV endpoint](https://caldav.icloud.com/) <br>
- [Fastmail CalDAV endpoint](https://caldav.fastmail.com/dav/calendars/user/EMAIL/) <br>
- [Nextcloud CalDAV endpoint pattern](https://YOUR.CLOUD/remote.php/dav/calendars/USERNAME/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and ini code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Linux package requirements for vdirsyncer and khal.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
