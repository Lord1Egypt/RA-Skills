## Description:

Smart Calendar Assistant for WorkBuddy that manages Claw Calendar calendars and events through the Claw Calendar REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[5twang](https://clawhub.ai/user/5twang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to list calendars, create calendars, list events, and create calendar events with optional reminders through a Claw Calendar account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable API endpoint can receive the user's calendar API key and calendar data.

Mitigation: Set CLAW_CALENDAR_API_URL only to a trusted HTTPS endpoint, and leave it unset to use the default Claw Calendar service.

Risk: Calendar, event, reminder, and subscription-link actions may sync to external devices or accounts.

Mitigation: Review requested calendar changes before execution and treat subscription URLs as sensitive account data.

Risk: The skill requires a calendar API key.

Mitigation: Store the key only in CLAW_CALENDAR_API_KEY, avoid logs or repository commits, and rotate the key if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/5twang/skills/claw-calendar-new-skill)
- [Claw Calendar service](https://claw-calendar.com)
- [Claw Calendar API endpoint](https://claw-calendar.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify calendars and events in the connected Claw Calendar account.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
