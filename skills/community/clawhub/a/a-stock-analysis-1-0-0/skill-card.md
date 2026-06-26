## Description: <br>
Provides real-time China A-share quotes, intraday volume analysis, trading-signal summaries, and local portfolio profit-and-loss management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanchanghua](https://clawhub.ai/user/zhanchanghua) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query Shanghai, Shenzhen, and Beijing Stock Exchange A-share prices, inspect intraday volume concentration, and manage local portfolio holdings and P&L from command-line scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried stock symbols are sent to Sina Finance when fetching market data. <br>
Mitigation: Use the skill only when you are comfortable disclosing the queried symbols to that external data source. <br>
Risk: Portfolio holdings are stored locally in plaintext. <br>
Mitigation: Avoid storing sensitive position details unless local file permissions and device access are acceptable for the use case. <br>
Risk: The remove command changes the local portfolio file without an undo mechanism. <br>
Mitigation: Confirm the stock code and intended action before add, update, or remove operations, and keep backups if the portfolio file is important. <br>


## Reference(s): <br>
- [A Stock Analysis 1.0.0 ClawHub Page](https://clawhub.ai/zhanchanghua/a-stock-analysis-1-0-0) <br>
- [Publisher Profile](https://clawhub.ai/user/zhanchanghua) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>
- [Sina Realtime Quote Endpoint](https://hq.sinajs.cn/list=) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files] <br>
**Output Format:** [Terminal text and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Portfolio commands can create or modify a local plaintext portfolio file at ~/.clawdbot/skills/a-stock-analysis/portfolio.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
