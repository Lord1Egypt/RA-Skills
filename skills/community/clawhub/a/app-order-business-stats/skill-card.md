## Description: <br>
按时间段和业务版块统计久事体育APP订单关键指标（业务版块、用户数、订单量、支付金额、退款金额、净销售金额）。适用于查询“某段时间内业务版块的订单”相关统计。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaggerliu](https://clawhub.ai/user/jaggerliu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Business and operations users use this skill to query daily app order metrics by business segment for a confirmed time range, including users, order volume, payment amount, refund amount, and net sales. It is intended for authorized reporting against the configured read-only order data source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized users could query private business order data if the skill is installed in an environment with database credentials. <br>
Mitigation: Install only where database access is authorized, intentionally provision the mysql client and JIUSHI_DB_PASSWORD, and restrict who can invoke the skill. <br>
Risk: Broader operational use may need stronger accountability around reporting access. <br>
Mitigation: For wider deployment, consider a scoped reporting API with audit logging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaggerliu/app-order-business-stats) <br>
- [Publisher profile](https://clawhub.ai/user/jaggerliu) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Analysis] <br>
**Output Format:** [Markdown table with supporting SQL or shell command context when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily aggregation only; hourly breakdowns are out of scope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
