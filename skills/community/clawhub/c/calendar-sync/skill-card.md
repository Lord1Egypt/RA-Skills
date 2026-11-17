## Description:

Calendar Sync converts structured document date fields such as deadlines, event dates, and periods into Apple Calendar events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkbeomjun-gkgkgk](https://clawhub.ai/user/parkbeomjun-gkgkgk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to turn structured document outputs into calendar reminders for deadlines, meetings, events, and date ranges. It can generate an ICS file for import or, on trusted macOS inputs, attempt direct Apple Calendar registration through AppleScript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional AppleScript path can execute unsafe script content derived from document data.

Mitigation: Use ICS generation by default and allow AppleScript only for trusted input JSON after reviewing the generated events.

Risk: Calendar event notes may sync to Apple or iCloud calendars and expose document summaries, amounts, source paths, IDs, or Notion links.

Mitigation: Redact sensitive note fields before import and confirm the target calendar account before syncing.

Risk: Dependency versions are not pinned in the artifact guidance.

Mitigation: Pin and review the icalendar dependency in the deployment environment before routine use.

## Reference(s):

- [Calendar Sync ClawHub listing](https://clawhub.ai/parkbeomjun-gkgkgk/skills/calendar-sync)
- [Publisher profile](https://clawhub.ai/user/parkbeomjun-gkgkgk)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Code, Guidance, Text]

**Output Format:** [ICS calendar file, AppleScript command path, Markdown/text guidance, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and the icalendar package; direct calendar registration is macOS-specific.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
