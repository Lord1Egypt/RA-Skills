## Description: <br>
BTC/ETH AI Trader generates BTC and ETH technical-analysis reports with opening suggestions and optional multi-platform notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thanatosmoe](https://clawhub.ai/user/thanatosmoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, crypto analysts, and operators use this skill to fetch BTC/ETH market data, generate technical-analysis reports with entry, target, stop-loss, and risk-reward values, and optionally push those reports to configured messaging channels. It is intended for informational market analysis and notifications, not automated trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated market analysis and opening suggestions may be mistaken for investment advice. <br>
Mitigation: Use reports as informational analysis only, review recommendations before acting, and preserve the skill's risk disclaimer. <br>
Risk: Messaging credentials or webhook URLs in config.json could expose notification channels if shared. <br>
Mitigation: Keep config.json private and use dedicated low-privilege bots or webhooks for configured channels. <br>
Risk: Recurring scheduled reports can repeatedly contact market-data APIs and configured messaging services. <br>
Mitigation: Add the cron schedule only when recurring automated reports are intended and monitor the configured channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thanatosmoe/btc-eth-ai-signal) <br>
- [Publisher profile](https://clawhub.ai/user/thanatosmoe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown trading-analysis report with optional messaging-channel notifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured messaging credentials; report text may be truncated by Telegram, Discord, and WeCom push adapters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
