## Description: <br>
LongPort Quant Trader integrates LongPort brokerage automation with oversold and momentum trading strategies, Feishu notifications, performance tracking, scheduled monitoring, and stop-gain/stop-loss handling for Hong Kong and U.S. equities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fxm1618-gmail](https://clawhub.ai/user/fxm1618-gmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, personal investors, and quantitative-trading enthusiasts use this skill to configure and run Python scripts for LongPort-based market scanning, automated trading, backtesting, and Feishu trade notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes scripts that can submit live LongPort broker orders. <br>
Mitigation: Review each trading script, use a paper account first, and keep live credentials out of the runtime until order behavior and limits are understood. <br>
Risk: Automated monitoring loops and scheduled execution can repeatedly trade without active supervision. <br>
Mitigation: Disable or remove auto-trade loops and crontab scheduling until strategy thresholds, position sizing, and stop rules have been validated. <br>
Risk: Credential, account, Feishu app secret, and open_id handling is not clearly controlled. <br>
Mitigation: Replace all credentials, account IDs, Feishu app secrets, and open_id values before use, then store required secrets only in a controlled environment. <br>
Risk: Backtest and performance examples may be mistaken for real validation. <br>
Mitigation: Treat the included performance claims as illustrative and require independent paper-trading and review before any live deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fxm1618-gmail/fxm1618-longport-quant-trader) <br>
- [LongPort OpenAPI](https://open.longportapp.com) <br>
- [LongPort OpenAPI account setup](https://open.longportapp.com/account) <br>
- [LongPort OpenAPI documentation](https://open.longportapp.com/docs) <br>
- [LongPort app](https://www.longportapp.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python code, shell commands, JSON configuration, and console reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and LongPort API environment variables; optional Feishu notification credentials are described by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
