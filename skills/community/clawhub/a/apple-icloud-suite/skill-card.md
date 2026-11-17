## Description:

Provides agent guidance and scripts for using Apple iCloud Calendar, Photos, Drive, Find My devices, Reminders, and related status-wall workflows from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help a user inspect and modify iCloud calendars, browse or download iCloud Photos and Drive files, locate Apple devices, manage reminders, and optionally publish personal status into a shared calendar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive iCloud account data, including calendars, photos, Drive files, device location, reminders, and account sessions.

Mitigation: Use local interactive authentication, avoid sharing primary Apple ID passwords in chat, prefer secure keychain storage, and install only when the publisher is trusted with this account access.

Risk: The status-wall workflow can poll device location in the background, send coordinates to AMap for reverse geocoding, and publish personal status to a shared calendar.

Mitigation: Enable the status wall only with explicit consent from every tracked person, confirm the shared calendar audience, and document how to stop the daemon and remove config, log, and session files.

Risk: Calendar deletion and photo download commands can modify user data or copy private media to local storage.

Mitigation: Review matching criteria and target calendars before deletion, use an isolated working directory for downloads, and require user confirmation before running destructive or bulk actions.

## Reference(s):

- [Skill page](https://clawhub.ai/lovensky1992-wk/skills/apple-icloud-suite)
- [Calendar reference](references/calendar.md)
- [Photos reference](references/photos.md)
- [Drive reference](references/drive.md)
- [Find My reference](references/findmy.md)
- [Scripts reference](references/scripts.md)
- [Apple ID account management](https://appleid.apple.com)
- [iCloud CalDAV endpoint](https://caldav.icloud.com/)
- [AMap Web Service API](https://lbs.amap.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-controlled Apple ID authentication, app-specific passwords for CalDAV, and an optional AMap API key for location naming.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
