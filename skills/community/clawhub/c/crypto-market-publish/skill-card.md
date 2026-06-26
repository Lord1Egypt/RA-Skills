## Description: <br>
Comprehensive cryptocurrency market monitoring and economic data analysis for tracking crypto prices, market sentiment, economic data releases, and economic indicator impacts on crypto markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KJjjj0](https://clawhub.ai/user/KJjjj0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and crypto operators use this skill to monitor major cryptocurrency prices, generate market reports, review economic calendar events, and update actual economic values for bullish or bearish impact analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual setup can overwrite or reset local crypto workspace data. <br>
Mitigation: Install into a dedicated crypto workspace, back up existing ~/.openclaw/workspace/crypto data first, and avoid reset commands unless clearing saved economic data is intentional. <br>
Risk: Hard-coded /root/.openclaw paths can cause reliability or local import risks when using custom install locations. <br>
Mitigation: Review or fix hard-coded paths before relying on custom paths, and run the skill from the intended isolated workspace. <br>
Risk: Cron entries enable recurring background monitoring and log writes. <br>
Mitigation: Add cron jobs only when recurring monitoring is intended, and review the schedule and log paths before enabling them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/KJjjj0/crypto-market-publish) <br>
- [Installation guide](INSTALL.md) <br>
- [Quick reference](references/quick-reference.md) <br>
- [Economic data types](references/data-types.md) <br>
- [Usage examples](references/usage-examples.md) <br>
- [CoinGecko markets API](https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids}&order=market_cap_desc&sparkline=true&price_change_percentage=1h,24h,7d,30d) <br>
- [CoinGecko global API](https://api.coingecko.com/api/v3/global) <br>
- [Binance 24hr ticker API](https://api.binance.com/api/v3/ticker/24hr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and local JSON data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local actual-value data and log files in the configured crypto workspace.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
