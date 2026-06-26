## Description: <br>
Track US congress member and politician stock trades in real-time using the Quiver Quant API, sync trades to a local SQLite database, detect new significant trades above 15K, and send alerts via OpenClaw messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Armax](https://clawhub.ai/user/Armax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to monitor reported US congressional stock trades, keep a local SQLite record, and surface alerts for new buy or sell activity above a configured threshold. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Congress Trades Tracker on ClawHub](https://clawhub.ai/Armax/congress-trades) <br>
- [Quiver Quant](https://www.quiverquant.com/) <br>
- [Quiver Quant Congress Trading API endpoint](https://api.quiverquant.com/beta/live/congresstrading) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local SQLite data, JSON alert history, and a pending text alert file for agent pickup.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
