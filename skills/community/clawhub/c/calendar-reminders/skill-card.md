## Description:

Provides a config-driven wrapper around gcalcli with optional CalDAV integration to generate JSON reminder plans for one-shot OpenClaw reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adorostkar](https://clawhub.ai/user/adorostkar)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to read Google Calendar and optional CalDAV events, plan upcoming reminders, and pass the resulting schedule to cron or an agent workflow that creates one-shot OpenClaw reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar integrations can expose calendar data and OAuth sessions through gcalcli or khal.

Mitigation: Install only when calendar access is acceptable, keep OAuth/session material private, and review reminder JSON before sharing because it can include calendar titles, IDs, labels, and reminder times.

Risk: Configured external binaries or scheduler wiring could execute untrusted commands if paths or cron jobs are not reviewed.

Mitigation: Use trusted, preferably absolute binary paths, keep scheduler commands as argv lists, and review any cron job before enabling it.

## Reference(s):

- [openclaw-calendar.example.json](references/openclaw-calendar.example.json)
- [ClawHub skill page](https://clawhub.ai/adorostkar/skills/calendar-reminders)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON reminder plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reminder plans include calendar labels, event IDs, reminder times, messages, and skipped-event counts.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
