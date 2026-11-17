## Description:

查询公司海关贸易HS编码列表数据，返回HS编码、贸易次数、金额、数量、重量和占比，帮助外贸团队分析供应商或采购商的产品组合。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade, sourcing, and market analysis teams use this skill to inspect a company's HS-code trade breakdown and drill into product-category composition for supplier analysis or buyer profiling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid Upkuajing API key and account workflows.

Mitigation: Use an environment variable or protected secret store for UPKUAJING_API_KEY, and confirm paid lookup or recharge actions before execution.

Risk: API key material may be stored in ~/.upkuajing/.env.

Mitigation: Do not print or paste the contents of ~/.upkuajing/.env into an agent transcript.

Risk: Error reports may include business context from failed calls.

Mitigation: Review report contents before submission and avoid including sensitive business data.

Risk: The security verdict is suspicious because the skill handles API keys, billing, telemetry, and automatic version checks.

Mitigation: Review and scan the skill before deployment, especially account, billing, error-reporting, and version-check behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-company-hscode-list-zh)
- [Upkuajing Homepage](https://www.upkuajing.com)
- [Upkuajing Developer Platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [公司贸易HS编码列表 API 参考](references/customs-company-hscode-list-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; lookup calls are paid and paginated with a cursor.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
