## Description: <br>
Monitors BlockBeats news and articles, categorizes selected crypto-market keyword groups, stores results in SQLite, and generates Telegram-ready daily sentiment reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yugulugulu](https://clawhub.ai/user/yugulugulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect BlockBeats Pro API items, track predefined crypto-market topics over 24-hour windows, and deliver a Markdown daily report to Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive BlockBeats Pro API and Telegram bot credentials. <br>
Mitigation: Store credentials in the local config file with appropriate file permissions and rotate them if they are exposed. <br>
Risk: Reports can be sent to the wrong Telegram destination if chat_id is misconfigured. <br>
Mitigation: Verify the Telegram chat_id before enabling run-daily or scheduled delivery. <br>
Risk: Fetched content and generated reports may remain in the local SQLite database. <br>
Mitigation: Choose an appropriate storage.db_path and delete or rotate the database according to retention needs. <br>


## Reference(s): <br>
- [BlockBeats Pro API](https://api-pro.theblockbeats.info) <br>
- [SQLite schema](references/schema.sql) <br>
- [Example configuration](config.example.toml) <br>
- [ClawHub skill page](https://clawhub.ai/yugulugulu/blockbeats-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and TOML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-configured BlockBeats Pro API credentials, local SQLite storage, and optional Telegram delivery.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
