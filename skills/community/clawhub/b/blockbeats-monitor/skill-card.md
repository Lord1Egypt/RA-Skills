## Description:

Monitors BlockBeats news and articles, classifies coverage for specified crypto-market keyword groups, stores results in SQLite, and generates Telegram-ready sentiment reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yugulugulu](https://clawhub.ai/user/yugulugulu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to collect BlockBeats Pro API content, track configured crypto-market keyword groups over rolling 24-hour windows, and produce daily Markdown reports for Telegram delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot tokens can be exposed through the spawned curl command used for report delivery.

Mitigation: Use a least-privileged Telegram bot, protect config.toml, and prefer updating the sender to avoid putting the bot token in child-process command arguments.

Risk: Collected BlockBeats content and generated reports are stored in a local SQLite database.

Mitigation: Store the database in an access-controlled location and delete retained data that is no longer needed.

Risk: Generated reports are sent to the configured Telegram chat.

Mitigation: Confirm the chat_id before use and review report contents before sending.

## Reference(s):

- [BlockBeats Pro API endpoint](https://api-pro.theblockbeats.info)
- [SQLite schema](artifact/references/schema.sql)
- [ClawHub skill page](https://clawhub.ai/yugulugulu/skills/blockbeats-monitor)
- [Publisher profile](https://clawhub.ai/user/yugulugulu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON command status, TOML configuration guidance, and CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores normalized source content and generated report runs in a local SQLite database; can send reports to a configured Telegram chat.]

## Skill Version(s):

0.1.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
