## Description: <br>
生成A股综合分析报告（深交所/上交所/北交所），包含K线技术指标图表、同行业对比、基本面分析、主营业务构成、技术面评分、催化剂与风险、短线/中线买卖建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bwgao](https://clawhub.ai/user/bwgao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to generate A-share stock analysis reports from a stock name or code, including technical charts, peer comparison, fundamentals, catalysts, risks, and short- and medium-term trading commentary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated buy/sell, target-price, and stop-loss commentary can be mistaken for personalized financial advice. <br>
Mitigation: Treat the report as informational analysis only, verify data freshness and sources, and apply independent judgment before making investment decisions. <br>
Risk: The skill runs Python scripts that fetch public market data and write local report files. <br>
Mitigation: Review the scripts and requested commands before execution, run in an appropriate workspace, and avoid sharing unnecessary credentials. <br>
Risk: Financial data may be incomplete if source fallbacks fail or market data is stale. <br>
Mitigation: Check the generated data package, source notes, and analysis date before relying on the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bwgao/ashare-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/bwgao) <br>
- [Report template](references/report_template.md) <br>
- [Technical scoring reference](references/technical_scoring.md) <br>
- [Peer selection rules](references/peer_selection_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated JSON data, PNG charts, and a standalone HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local report artifacts and may use an optional TUSHARE_TOKEN for financial data access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
