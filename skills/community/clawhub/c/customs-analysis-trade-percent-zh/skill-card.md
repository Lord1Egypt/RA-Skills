## Description:

查询指定 HS 编码下各企业的贸易份额数据，返回按贸易量排名的贸易次数、占比、数量、金额和合作伙伴数量。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

贸易分析师、采购代理和市场研究人员使用该技能识别特定产品的主要交易企业、分析市场集中度、评估供应商竞争格局并发现潜在贸易伙伴。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed or persisted in local configuration.

Mitigation: Set UPKUAJING_API_KEY through a secure environment or secret store and avoid commands that print the .env file.

Risk: Queries can spend funds from a real API account.

Mitigation: Check charges before each query and require explicit user confirmation before paid API calls.

Risk: Error reports may include sensitive business request or response data.

Mitigation: Send only the minimum diagnostic context needed and avoid raw request or response bodies when they contain sensitive data.

Risk: The skill includes account, payment, error-reporting, and update-check behavior beyond the core query.

Mitigation: Review the skill before installation, especially when the configured API account has real spending value.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-analysis-trade-percent-zh)
- [Publisher profile](https://clawhub.ai/user/upkuajing)
- [跨境魔方 homepage](https://www.upkuajing.com)
- [跨境魔方开放平台](https://developer.upkuajing.com/)
- [详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
- [分析报告-贸易占比 API 参考](artifact/references/customs-analysis-trade-percent-api.md)
- [Agent 调用 Skill 异常上报 API 参考](artifact/references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; paid queries return paginated company-level trade-share records with fee and request ID metadata.]

## Skill Version(s):

1.0.1 (source: SKILL.md metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
