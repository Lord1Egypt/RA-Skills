## Description: <br>
查询场外基金（公募基金）的实时估值、净值、基本信息。支持天天基金代码查询。当用户询问基金净值、基金估值、基金涨跌时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pazzilivo](https://clawhub.ai/user/Pazzilivo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up public mutual fund estimates, historical net asset values, and basic fund information by six-digit fund code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried fund codes are sent to public Eastmoney/Tiantian fund API endpoints. <br>
Mitigation: Use the skill only when sharing queried fund codes with those public data services is acceptable. <br>
Risk: The release metadata does not explicitly declare network access. <br>
Mitigation: Review network behavior before deployment and document that the skill contacts public fund-data APIs. <br>
Risk: Real-time fund estimates may be stale outside trading hours or dependent on upstream API availability. <br>
Mitigation: Check timestamps in the returned output and treat fund data as informational rather than investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Pazzilivo/fund-query) <br>
- [Eastmoney fund data source](http://fund.eastmoney.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown-formatted text with fund values, timestamps, and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a six-digit fund code and optionally an estimate, info, or history command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
