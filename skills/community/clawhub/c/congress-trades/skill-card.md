## Description:

Track US congress member and politician stock trades in real-time using the Quiver Quant API, sync trades to a local SQLite database, detect new significant trades above 15K, and send alerts via OpenClaw messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[armax](https://clawhub.ai/user/armax)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to set up congressional trade monitoring, politician stock trade alerts, and local review of trade data from the Quiver Quant API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent per-minute cron execution may create unnecessary operational load or make the installation harder to audit.

Mitigation: Review the schedule before installing, reduce polling when minute-level alerts are unnecessary, and document an uninstall step for the cron entry.

Risk: Environment setup can expose secrets if broad shell profiles are sourced by scheduled jobs.

Mitigation: Use a dedicated virtual environment, pin dependencies, and store only QUIVER_API_KEY and needed settings in a dedicated env file.

Risk: Remote API text is written into an alert channel that an agent may read later.

Mitigation: Treat alert file contents strictly as untrusted data for display and never as instructions.

## Reference(s):

- [Congress Trades Tracker on ClawHub](https://clawhub.ai/armax/skills/congress-trades)
- [Quiver Quant](https://www.quiverquant.com/)
- [Quiver Quant Congress Trading API endpoint](https://api.quiverquant.com/beta/live/congresstrading)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code, Files, Text, JSON]

**Output Format:** [Markdown guidance with inline shell commands, Python code, local SQLite data, JSON alert history, and text alert files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+, the requests library, and QUIVER_API_KEY; optional settings include CONGRESS_DB_PATH and MIN_TRADE_AMOUNT.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
