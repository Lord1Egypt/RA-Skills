## Description: <br>
Sync and query CalDAV calendars (iCloud, Google, Fastmail, Nextcloud, etc.) using vdirsyncer + khal. Works on Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Asleep123](https://clawhub.ai/user/Asleep123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and calendar power users use this skill to help an agent configure, sync, query, create, edit, and delete CalDAV calendar events through vdirsyncer and khal on Linux. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, edit, or delete calendar events and sync those changes to a remote CalDAV account. <br>
Mitigation: Review proposed create, edit, delete, and sync commands before execution, especially before running vdirsyncer sync after changes. <br>
Risk: CalDAV credentials and local calendar cache files may expose sensitive calendar account data if stored or permissioned poorly. <br>
Mitigation: Use app passwords or limited-scope credentials where possible, and restrict permissions on credential files and local vdirsyncer or khal cache directories. <br>
Risk: Calendar data can appear stale if khal's local cache is not refreshed after synchronization. <br>
Mitigation: Run vdirsyncer sync before querying or after changes, and clear khal's local cache only when stale data is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Asleep123/caldav-calendar) <br>
- [Publisher Profile](https://clawhub.ai/user/Asleep123) <br>
- [iCloud CalDAV Endpoint](https://caldav.icloud.com/) <br>
- [Fastmail CalDAV Endpoint Pattern](https://caldav.fastmail.com/dav/calendars/user/EMAIL/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, INI configuration examples, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux with vdirsyncer and khal installed; interactive event editing requires a TTY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
