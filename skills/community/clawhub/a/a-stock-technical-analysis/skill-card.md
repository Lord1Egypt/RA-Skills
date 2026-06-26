## Description: <br>
A股个股技术分析报告生成工具，当用户请求生成股票技术分析报告、查询A股个股行情、分析个股走势时，支持输入股票代码和股票名称，抓取东方财富公开行情数据并生成结构化技术分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyuqi98](https://clawhub.ai/user/zhangyuqi98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to gather public stock-market data for A-share, Hong Kong, or US equities and draft a structured technical-analysis report. The report is informational and should not be treated as personalized investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public market data can be unavailable, delayed, incomplete, or tied to the wrong symbol. <br>
Mitigation: Confirm the stock symbol and data source before relying on the report, and mark missing data as unavailable rather than inventing values. <br>
Risk: Generated technical analysis can be mistaken for personalized investment advice. <br>
Mitigation: Treat the report as informational only and keep the required disclaimer that the content does not constitute investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyuqi98/a-stock-technical-analysis) <br>
- [Report template](references/report-template.md) <br>
- [Eastmoney stock quote page](https://quote.eastmoney.com/sz{代码}.html) <br>
- [Eastmoney stock quote API](http://push2.eastmoney.com/api/qt/stock/get?secid=0.{代码}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f170,f171) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown technical-analysis report with supporting browser and API commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses explicit unavailable-data wording when data is missing and requires an investment-advice disclaimer.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
