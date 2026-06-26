## Description: <br>
Tracks Bitcoin prices from CoinGecko, manages local price alerts, and prints alert notifications for command-line use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siemen90](https://clawhub.ai/user/siemen90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and crypto users use this skill to check BTC prices in USD, CNY, and SGD, create local threshold alerts, and review notifications for triggered alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls CoinGecko for Bitcoin prices and may fall back to cached local price data after network or rate-limit failures. <br>
Mitigation: Treat cached prices as stale until refreshed and configure polling intervals to respect CoinGecko rate limits. <br>
Risk: Alert names, thresholds, and cached prices are stored in local JSON files. <br>
Mitigation: Avoid sensitive alert names and keep the skill directory permissions appropriate for the deployment environment. <br>
Risk: If Telegram or OpenClaw Gateway notification delivery is enabled, alert names, prices, and trigger text may leave the local environment. <br>
Mitigation: Use non-sensitive alert labels and confirm the Telegram bot, channel, and gateway configuration before enabling notifications. <br>


## Reference(s): <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [CoinGecko API](https://www.coingecko.com/en/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Command-line text with local JSON alert and price cache files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CoinGecko network requests and stores alerts and cached prices in local JSON files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
