## Description:

Steuert Deskbird ueber Telegram mit sicherem Auth-Handling, Discovery und Parkplatz-Status/Reservierung.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geby85](https://clawhub.ai/user/geby85)

### License/Terms of Use:


## Use Case:

Employees or workplace operations users can ask an OpenClaw agent to check Deskbird availability, summarize bookable resources, and optionally create or update a recurring cron session for parking monitoring or booking. The skill is intended for cautious Deskbird automation with explicit reauthentication handling before API actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles raw Deskbird session credentials and can store credentials for recurring use.

Mitigation: Review the credential flow before installation, avoid sending live Authorization headers, cookies, or refresh tokens through Telegram when possible, and restrict the env file to owner-only permissions.

Risk: Broad request replay and probe tooling can send stored credentials outside Deskbird if misused.

Mitigation: Do not use probe or replay with stored credentials or untrusted capture files; keep safe mode enabled and limit API calls to the documented Deskbird workflows.

Risk: Automated cron runs can perform parking bookings if rules are too broad.

Mitigation: Keep booking rules narrow, require discovery before booking, use dry-run checks where available, and stop cron runs cleanly when reauthentication is required.

## Reference(s):

- [Cron Session Prompt Template](references/cron-session-template.md)
- [Deskbird-Automator ClawHub Release](https://clawhub.ai/geby85/skills/deskbird-automator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status summaries with inline shell commands and JSON-capable CLI outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs normally include auth status, checked dates or zones, availability findings, and whether a booking was made or skipped.]

## Skill Version(s):

1.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
