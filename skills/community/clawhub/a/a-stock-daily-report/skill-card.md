## Description: <br>
A股每日简报自动生成系统。抓取东方财富实时数据，生成包含大盘指数、热门板块、资金动向等完整信息的日报报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zsxink](https://clawhub.ai/user/zsxink) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate A-share market daily reports from Eastmoney data, including index summaries, sector movement, funding direction, risk notes, and optional JSON output for downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report can contain incomplete or unavailable market data when Eastmoney endpoints are unavailable, especially outside trading windows. <br>
Mitigation: Check the generated data failure warnings and rerun during the documented post-close window before using the report operationally. <br>
Risk: The report includes market strategy and sector attention guidance that may be unsuitable as standalone financial advice. <br>
Mitigation: Review the generated report with independent market analysis and do not treat the output as an instruction to trade. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zsxink/a-stock-daily-report) <br>
- [Eastmoney quote site](http://quote.eastmoney.com/) <br>
- [Eastmoney sector API](http://push2.eastmoney.com/api/qt/clist/get) <br>
- [Eastmoney index API](http://push2.eastmoney.com/api/qt/stock/get) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report by default, or structured JSON when invoked with the json or --json argument.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Node.js built-in modules and writes to standard output; users may redirect output to a local report file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
