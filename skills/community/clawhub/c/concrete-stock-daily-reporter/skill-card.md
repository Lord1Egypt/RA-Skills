## Description: <br>
Generates daily custom stock reports with market prices, KDJ indicators, notable signals, and optional Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenhulove333](https://clawhub.ai/user/wenhulove333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce stock watchlist reports from supplied stock codes and names, including price rankings, KDJ values, detailed quotes, attention signals, and daily summary statistics. It can also send the generated report through Feishu when the recipient and command arguments are configured correctly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report sender can deliver a user's stock report to a hard-coded Feishu recipient. <br>
Mitigation: Replace or remove the hard-coded Feishu target, confirm the exact recipient before sending, and avoid enabling scheduled delivery until the recipient and stock arguments are correct. <br>
Risk: Generated reports may expose sensitive investment-interest data. <br>
Mitigation: Treat generated reports and delivery logs as sensitive and share them only with intended recipients. <br>
Risk: Market data retrieval includes an unverified HTTPS configuration and an HTTP endpoint. <br>
Mitigation: Prefer verified HTTPS sources for market data before relying on the skill in a sensitive workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenhulove333/concrete-stock-daily-reporter) <br>
- [Sina Finance market data endpoint](https://hq.sinajs.cn/list={stock_code}) <br>
- [Eastmoney K-line data endpoint](http://push2his.eastmoney.com/api/qt/stock/kline/get?secid={symbol}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&end=20500101&lmt=30) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Plain text stock report with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-supplied stock code and name list; report delivery depends on the OpenClaw CLI and a configured Feishu target.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
