## Description:

Calendar Skills intelligent calendar assistant interacts with Claw Calendar (claw-calendar.com) through REST APIs to manage calendars and events, reading credentials from environment variables and supporting calendar creation, event creation, and schedule queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[5twang](https://clawhub.ai/user/5twang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Claw Calendar calendars and events from an agent, including listing calendars, creating calendars, listing events by date range, adding reminders, and receiving .ics subscription links for mobile calendar apps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Claw Calendar API key and calendar data are sent to the configured API URL.

Mitigation: Keep CLAW_CALENDAR_API_URL unset unless using a trusted custom deployment, avoid plaintext or untrusted endpoints, and store CLAW_CALENDAR_API_KEY only in the environment.

Risk: Incorrect calendar IDs, event dates, reminders, or subscription links could create misleading calendar entries.

Mitigation: Review generated commands and API results before relying on new calendars, events, or .ics subscription links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/5twang/skills/claw-calendar-v2)
- [Claw Calendar](https://claw-calendar.com)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CLAW_CALENDAR_API_KEY and optionally CLAW_CALENDAR_API_URL; API responses may include calendar IDs, event IDs, colors, reminder settings, and .ics subscription URLs.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
