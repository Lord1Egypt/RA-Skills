## Description: <br>
A股个股技术分析报告生成工具，支持输入股票代码和股票名称，自动抓取东方财富实时数据并生成结构化技术分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyuqi98](https://clawhub.ai/user/zhangyuqi98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate informational technical-analysis reports for A-share, Hong Kong, or U.S. stocks from public EastMoney market data. The reports summarize price action, market context, fundamentals, events, capital flows, and risk factors without providing investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated stock reports may contain stale, incomplete, or misread market data and could be mistaken for investment advice. <br>
Mitigation: Treat reports as informational technical analysis only, keep the required disclaimer, and independently verify important figures before relying on them. <br>
Risk: The skill contacts EastMoney with the stock codes requested by the user, exposing those lookup interests to an external market-data service. <br>
Mitigation: Use only public stock identifiers and do not provide brokerage credentials, private account details, or other sensitive financial information. <br>
Risk: EastMoney pages or API calls may be unavailable or return limited technical-indicator data. <br>
Mitigation: Use browser snapshot data when API access fails and write '暂无数据' or '无法判断' instead of fabricating missing values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyuqi98/eastmoney-stock-analysis) <br>
- [Report template](references/report-template.md) <br>
- [EastMoney quote page pattern](https://quote.eastmoney.com/sz{代码}.html) <br>
- [EastMoney stock quote API pattern](http://push2.eastmoney.com/api/qt/stock/get?secid=0.{代码}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f170,f171) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown technical-analysis report with cited data fields and an investment-advice disclaimer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a stock code and stock name; may use browser navigation and public EastMoney API calls to gather market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
