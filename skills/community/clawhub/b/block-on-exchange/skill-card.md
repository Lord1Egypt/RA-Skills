## Description:

Sync any ICS/iCal calendar to Microsoft Exchange as blocked time slots, with recurring event support, change detection, and privacy-preserving sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blucaru](https://clawhub.ai/user/blucaru)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to mirror personal calendar busy time into a Microsoft Exchange calendar while exposing only blocked time slots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Microsoft Calendars.ReadWrite permission can add, update, or delete events in the connected Exchange calendar.

Mitigation: Grant access only for the intended account and calendar, and review the configured Microsoft application before syncing.

Risk: The ICS feed URL and Microsoft token cache are sensitive local secrets.

Mitigation: Keep ~/.calintegration private, preserve restricted file permissions, and avoid sharing environment files, token files, or logs.

Risk: Optional launchd syncing runs automatically every five minutes on macOS.

Mitigation: Load the LaunchAgent only when background sync is desired, and unload it before changing credentials or calendar scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blucaru/skills/block-on-exchange)
- [Blucaru publisher profile](https://clawhub.ai/user/blucaru)
- [Project homepage](https://github.com/Blucaru/CalIn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
