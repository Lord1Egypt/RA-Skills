## Description:

Daily briefing: gathers calendar (gcalcli-calendar), active todos (todo-management), and weather (openmeteo-sh-weather-simple) into a concise summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lstpsche](https://clawhub.ai/user/lstpsche)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use this skill to collect their calendar agenda, active todos, and local weather into a concise daily briefing for mobile chat or scheduled delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefings may expose calendar entries, active todos, and default-location weather in the generated message.

Mitigation: Install only if that data access is acceptable, and use a private delivery channel for scheduled briefings.

Risk: Scheduled delivery can send briefings at an unintended time or destination if cron settings, timezone, channel, or permissions are misconfigured.

Mitigation: Verify the cron schedule, timezone, session mode, delivery channel, and permissions before relying on automated delivery.

Risk: Missing or failing companion skills can produce incomplete briefings.

Mitigation: The skill omits unavailable sections, reports command failures briefly, and instructs the agent not to fabricate data.

## Reference(s):

- [Briefing skill page](https://clawhub.ai/lstpsche/skills/briefing)
- [gcalcli-calendar companion skill](https://clawhub.ai/lstpsche/gcalcli-calendar)
- [todo-management companion skill](https://clawhub.ai/lstpsche/todo-management)
- [openmeteo-sh-weather-simple companion skill](https://clawhub.ai/lstpsche/openmeteo-sh-weather-simple)
- [gcalcli](https://github.com/insanum/gcalcli)
- [openmeteo-sh](https://github.com/lstpsche/openmeteo-sh)
- [Open-Meteo](https://open-meteo.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise mobile-friendly briefing with optional weather, calendar, upcoming, and todo sections.]

## Skill Version(s):

2.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
