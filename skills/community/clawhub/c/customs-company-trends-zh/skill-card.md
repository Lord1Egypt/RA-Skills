## Description:

调取海关数据获取企业月度贸易趋势明细，按月汇总企业交易频次、出货数量、重量和金额的变动情况，帮助外贸从业者研判企业采购周期和长期进出口走势。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

外贸团队、分析师和供应链经理使用该技能按企业 ID 查询海关企业月度贸易趋势，分析交易次数、出货数量、重量和金额的变化。该技能支持日期、产品、HS 编码、国家、贸易伙伴和港口等筛选条件，用于市场趋势分析、供应商销售监控和贸易流向情报。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential, account, payment, telemetry, and update-check behavior may expose sensitive operational context if used carelessly.

Mitigation: Review the skill before installing, keep the API key in an environment variable or secure secret store, and avoid commands that print `~/.upkuajing/.env`.

Risk: Customs-data lookups are paid API calls and account recharge actions affect billing.

Mitigation: Confirm pricing and obtain explicit user approval before running paid lookup or recharge workflows.

Risk: Error reporting can send diagnostic context to the platform.

Mitigation: Use error reporting only after user confirmation and avoid sending sensitive request or response details unless necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-company-trends-zh)
- [Publisher profile](https://clawhub.ai/user/upkuajing)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer portal](https://developer.upkuajing.com/)
- [Upkuajing API pricing](https://www.upkuajing.com/web/openapi/price.html)
- [公司贸易趋势 API 参考](references/customs-company-trends-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; API lookups may incur charges.]

## Skill Version(s):

1.0.2 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
