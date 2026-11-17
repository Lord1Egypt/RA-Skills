## Description:

调取海关进出口数据获取企业基础贸易统计信息，整理出企业贸易频次、出货数量、货物重量、交易金额以及合作客商总数，帮助外贸从业者评估企业整体交易规模和客户布局情况。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade teams, analysts, and researchers use this skill to query customs company statistics by company ID and role, then assess trade frequency, shipped quantity, weight, amount, activity range, and partner count. It supports supplier screening, buyer verification, and trade intelligence workflows that need a concise company-level trade summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key exposure from local credential handling.

Mitigation: Do not print `~/.upkuajing/.env`; only check whether `UPKUAJING_API_KEY` exists, use a dedicated least-privilege key, and restrict the credential file to owner-only permissions.

Risk: Unintended paid API usage or account recharge actions.

Mitigation: Confirm each paid query or recharge step in a separate user message before execution and use the provider price lookup for current pricing.

Risk: Sensitive business data or secrets may be included in exception reports.

Mitigation: Ask for explicit confirmation before reporting errors and remove raw business data, credentials, and other secrets from report context.

Risk: External calls include API activity, update checks, and platform workflows that should be reviewed before installation.

Mitigation: Review network behavior before deployment and allow only the expected Upkuajing endpoints required for the approved workflow.

## Reference(s):

- [公司贸易基础统计 API 参考](references/customs-company-stats-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)
- [跨境魔方主页](https://www.upkuajing.com)
- [跨境魔方开放平台](https://developer.upkuajing.com/)
- [开放平台价格说明](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; paid customs queries should return request and fee metadata.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
