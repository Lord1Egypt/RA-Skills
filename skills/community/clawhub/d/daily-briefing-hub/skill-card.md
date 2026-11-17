## Description:

All-in-one daily briefing skill that combines calendar events, email highlights, weather, GitHub activity, tasks, and news into a prioritized summary delivered through the user's chosen channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ariktulcha](https://clawhub.ai/user/ariktulcha)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers use this skill to generate morning briefings, daily digests, schedule overviews, inbox summaries, task recaps, developer activity summaries, and end-of-day recaps from configured personal or work sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefings may expose privacy-sensitive calendar, email, task, GitHub, and news context in shared delivery channels.

Mitigation: Configure only intended sources and choose the destination channel deliberately, especially for Slack, Discord, Telegram, or WhatsApp spaces with multiple participants.

Risk: Recurring delivery can repeatedly distribute aggregated personal or work information without manual review.

Mitigation: Review source selections, destination membership, and the first generated briefing before enabling or changing scheduled delivery.

## Reference(s):

- [Daily Briefing Hub on ClawHub](https://clawhub.ai/ariktulcha/skills/daily-briefing-hub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown or plain text briefing with optional JSON cron configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapts sections to available connected sources, omits empty sections, and can include recurring delivery setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
