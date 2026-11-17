## Description:

A股个股技术分析报告生成工具。当用户请求生成股票技术分析报告、查询A股个股行情、分析个股走势时触发。支持输入股票代码和股票名称，自动抓取东方财富实时数据并生成结构化技术分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyuqi98](https://clawhub.ai/user/zhangyuqi98)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to generate Chinese-language technical analysis reports for A-share stocks from a stock code and name. The report summarizes market data, trend context, valuation and risk signals, and explicitly states that it is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some market data URLs use insecure HTTP, which could affect report accuracy if responses are intercepted or altered.

Mitigation: Verify important numbers against an independent market data source before relying on the report.

Risk: Generated stock analysis may be mistaken for investment advice.

Mitigation: Keep the required disclaimer and treat the report as informational technical analysis only.

Risk: Eastmoney data fetching can be unstable or incomplete.

Mitigation: Use browser snapshot data when API calls fail and mark unavailable technical indicators or fields as "暂无数据" or "无法判断".

## Reference(s):

- [Report Template](references/report-template.md)
- [Eastmoney Quote Page](https://quote.eastmoney.com/sz{代码}.html)
- [Eastmoney Stock Quote API](http://push2.eastmoney.com/api/qt/stock/get?secid=0.{代码}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f170,f171)
- [ClawHub Skill Page](https://clawhub.ai/zhangyuqi98/skills/a-stock-technical-analysis)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown technical analysis report with structured sections and an investment-advice disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Eastmoney market data when reachable; missing or unavailable data should be marked as unavailable rather than fabricated.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
