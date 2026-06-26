## Description: <br>
Summarizes A-share market closing performance, including major indices, hot sectors, leading stocks, new-high stocks, and a brief market review using Eastmoney public APIs without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchaoqun](https://clawhub.ai/user/chenchaoqun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill after the A-share market close to generate an informational daily market recap from public Eastmoney data. It is suitable for market review and strategy discussion, not for real-time trading decisions or individualized investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and imports the Python requests package and makes outbound HTTP requests to Eastmoney public endpoints. <br>
Mitigation: Review the dependency and permit Eastmoney network access only in environments where outbound market-data requests are acceptable. <br>
Risk: The generated market review may be mistaken for investment advice or used as the sole basis for trading decisions. <br>
Mitigation: Treat the report as informational market commentary and verify data and decisions with appropriate financial review processes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenchaoqun/a-stock-market-review) <br>
- [Eastmoney quote API](http://push2.eastmoney.com/api/qt) <br>
- [Eastmoney stock quote endpoint](http://push2.eastmoney.com/api/qt/stock/get) <br>
- [Eastmoney list endpoint](http://push2.eastmoney.com/api/qt/clist/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Plain text or Markdown-style market report with inline tables and section headings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report content depends on live Eastmoney responses and the user environment's network access.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
