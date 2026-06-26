## Description: <br>
Monitor CamelCamelCamel price drop alerts via RSS and send Telegram notifications when items go on sale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jgramajo4](https://clawhub.ai/user/jgramajo4) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to configure an agent-managed scheduled check of their personal CamelCamelCamel RSS feed and receive Telegram-formatted price-drop alerts for Amazon products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A personal CamelCamelCamel RSS URL can reveal a user's tracked products if shared or reused. <br>
Mitigation: Use only the user's own feed URL and keep it private. <br>
Risk: Clearing or corrupting the local alert cache can cause duplicate Telegram notifications. <br>
Mitigation: Treat cache removal as a reset operation and expect existing feed items to alert again afterward. <br>
Risk: A stale scheduled job can continue checking the feed after the user stops using the monitor. <br>
Mitigation: Confirm the cron schedule and Telegram destination during setup, and remove the cron job and cache when decommissioning. <br>


## Reference(s): <br>
- [CamelCamelCamel Alerts Setup Guide](references/SETUP.md) <br>
- [CamelCamelCamel](https://camelcamelcamel.com/) <br>
- [ClawHub Skill Release](https://clawhub.ai/jgramajo4/camelcamelcamel-alerts) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples; runtime scripts emit JSON alerts and pipe-delimited notification records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local JSON cache to suppress duplicate alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
