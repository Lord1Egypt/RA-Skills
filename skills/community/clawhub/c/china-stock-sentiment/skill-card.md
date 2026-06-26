## Description: <br>
Monitors China A-share market sentiment, Baidu hot-search topics, and finance news sentiment to help users create market and stock sentiment reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual investors, investment advisors, and market analysts use this skill to summarize A-share sentiment, inspect stock-specific news tone, and generate markdown sentiment reports for review before making decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may look like investment advice even when based on mock or incomplete market data. <br>
Mitigation: Verify reports against real market sources and treat the output as decision support, not a trading directive. <br>
Risk: The skill relies on an unpinned chained call to `baidu-hot-cn` for hot-search data. <br>
Mitigation: Review the dependent skill before installation and re-check it when its behavior or version changes. <br>
Risk: Locally saved reports can reveal watched stocks, sectors, or investment interests. <br>
Mitigation: Periodically delete local report files and avoid storing sensitive portfolios in generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daimingvip-a11y/china-stock-sentiment) <br>
- [Publisher profile](https://clawhub.ai/user/daimingvip-a11y) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Chinese text, JSON objects, and markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated reports under memory/stock-sentiment/reports when run in report mode.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
