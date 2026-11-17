## Description:

Daily morning briefing for emails, calendar events, tasks, and weather in one summary, on demand or on a schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual users use this skill to have an agent collect unread email, today's calendar events, pending tasks, and local weather into a concise daily briefing. The skill can be run on demand or scheduled and delivered to a configured channel or local file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefings can include private email, calendar, task, and location information.

Mitigation: Limit configured inboxes, calendars, task lists, and weather locations to the sources the user intends the agent to access.

Risk: Sending summaries to Telegram or Discord may expose personal information outside local storage.

Mitigation: Prefer local file output for sensitive briefings, or use external delivery channels only after confirming the recipient channel and access controls.

Risk: Cron or scheduler setup can run the briefing at unintended times.

Mitigation: Review the schedule, timezone, and command before enabling recurring runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ceobotson-bot/skills/doctorclaw-morning-briefing)
- [DoctorClaw website](https://www.doctorclaw.ceo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing text with optional scheduler and delivery-channel setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-selected email, calendar, task, weather, and delivery-channel information.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
