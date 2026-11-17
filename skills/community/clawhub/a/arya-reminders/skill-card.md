## Description:

Arya Reminders creates one-shot, Spanish natural-language reminders for the America/Bogota timezone, emits cron job JSON, and records reminders in markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staratheris](https://clawhub.ai/user/staratheris)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to turn Spanish reminder requests into scheduled one-time reminders, with a local markdown record of reminder timing and content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder text may be sent to an unintended Telegram destination if the configured chat target is not verified.

Mitigation: Verify the Telegram destination before use, configure the intended chat explicitly, and remove or fail closed on any hard-coded default before broad distribution.

Risk: Reminder content may persist in scheduled cron jobs and a local reminder log.

Mitigation: Avoid sensitive reminder text unless persistence is acceptable, and review scheduled jobs plus memory/reminders.md for retention and cleanup.

Risk: The skill creates persistent scheduled agent actions that may run after the original conversation context has changed.

Mitigation: Review each generated cron job request before adding it and disable stale or incorrect jobs promptly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/staratheris/skills/arya-reminders)
- [Publisher profile](https://clawhub.ai/user/staratheris)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Markdown, Guidance]

**Output Format:** [JSON cron job request with shell command usage and markdown reminder-log guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Timezone defaults to America/Bogota; normal use schedules a one-shot reminder and records it in memory/reminders.md.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
