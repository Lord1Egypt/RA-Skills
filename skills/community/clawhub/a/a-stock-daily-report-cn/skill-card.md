## Description: <br>
获取 A 股市场日报，包括大盘指数、热门板块和龙头股。使用东方财富 API，无需 API Key。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchaoqun](https://clawhub.ai/user/chenchaoqun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to generate a daily Chinese A-share market report covering major indices, leading sectors, sector leaders, and short market commentary from public Eastmoney data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public HTTP requests to Eastmoney and depends on the Python requests package. <br>
Mitigation: Install and run it only in environments where outbound requests to Eastmoney and the requests dependency are acceptable. <br>
Risk: Market reports can be stale outside Chinese A-share trading hours or misleading if treated as investment advice. <br>
Mitigation: Use the report as reference market information, check the report timestamp and trading session, and verify important financial conclusions elsewhere. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenchaoqun/a-stock-daily-report-cn) <br>
- [Eastmoney stock quote endpoint](http://push2.eastmoney.com/api/qt/stock/get) <br>
- [Eastmoney sector list endpoint](http://push2.eastmoney.com/api/qt/clist/get) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown-style plain text report with shell and Python usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires public HTTP access to Eastmoney and the Python requests package; market data is reference information and not investment advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md version note) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
