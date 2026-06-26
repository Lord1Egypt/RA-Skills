## Description: <br>
实时盯盘工具，帮助上班族工作时间查询股票、贵金属价格走势并推送到指定频道 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual investors can use this skill to look up stock, index, futures, precious-metal, and commodity market snapshots during work hours and receive concise Chinese market reports in a configured channel. It is informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reports that the skill is preconfigured to send reports to a specific WeChat recipient that may not belong to the installer. <br>
Mitigation: Replace the embedded WeChat target with the installer's own user-scoped destination and require confirmation before each send. <br>
Risk: Market data may be delayed or unavailable, and generated summaries could be mistaken for financial advice. <br>
Mitigation: Present results as informational snapshots, keep the non-advisory warning, and verify critical prices against the cited market-data source before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/finance-watch) <br>
- [Stock code reference](artifact/stock_codes.md) <br>
- [Futures code reference](artifact/futures_codes.md) <br>
- [Eastmoney market quotes](https://quote.eastmoney.com/) <br>
- [Trading Economics commodities](https://zh.tradingeconomics.com/commodities) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style Chinese market reports with optional shell commands for data retrieval and channel delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include current price, change, range, volume where available, timestamp, brief analysis, and a non-advisory posture.] <br>

## Skill Version(s): <br>
1.6.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
