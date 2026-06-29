## Description: <br>
A股个股深度分析 uses a five-module framework to collect public A-share data and produce individual-stock analysis across fundamentals, valuation, technical signals, recent news, and buy/sell reference points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flynnliu](https://clawhub.ai/user/flynnliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to generate structured A-share individual-stock reports from public market, financial, analyst-report, news, and technical data. It is intended for informational analysis and valuation discussion, not as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries public Chinese finance sites and web search providers for stocks the user asks about. <br>
Mitigation: Use it only when those lookups are acceptable, and avoid entering non-public portfolio, strategy, or client-sensitive information. <br>
Risk: Generated buy/sell points, valuation ranges, and target prices can be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational analysis, verify the data independently, and make trading decisions outside the skill workflow. <br>
Risk: Market, analyst-report, or financial-statement data may be incomplete or unavailable from public sources. <br>
Mitigation: Mark unavailable fields explicitly and do not infer missing financial data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flynnliu/a-stock-individual-analysis) <br>
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/) <br>
- [Eastmoney data center API](https://datacenter-web.eastmoney.com/api/data/v1/get) <br>
- [Eastmoney report API](https://reportapi.eastmoney.com/report/list) <br>
- [Tonghuashun public stock pages](https://basic.10jqka.com.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables and optional JSON data collection output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a stock code; missing financial or market data should be marked unavailable rather than inferred.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
