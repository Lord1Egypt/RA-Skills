## Description: <br>
Monitors CSGO item prices with the CSQAQ API and provides price alerts, market movement analysis, cross-platform spread reminders, and rental yield calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pricnd](https://clawhub.ai/user/Pricnd) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
CSGO item traders and market watchers use this skill to query item prices, maintain watchlists, receive threshold and volatility alerts, compare marketplace spreads, and generate market summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server release changelog says the core implementation files were removed, so the current artifact may not run as described. <br>
Mitigation: Verify missing package and script files with the publisher before installing or enabling the skill. <br>
Risk: The skill uses CSQAQ API tokens, webhook tokens, scheduled notifications, and retained watchlist data. <br>
Mitigation: Keep tokens out of shared configs, review enabled notification channels and cron jobs before use, and clear stored monitor data when the watchlist is no longer needed. <br>
Risk: Market reports, spread alerts, and rental-yield calculations may be used to inform trading decisions. <br>
Mitigation: Treat outputs as informational, confirm prices and data freshness at the source, and review calculations before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Pricnd/csgo-monitor) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with command examples, configuration snippets, alerts, and market summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include price watchlist status, alert descriptions, market reports, and rental-yield analysis; this release's server changelog states that core implementation files were removed.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
