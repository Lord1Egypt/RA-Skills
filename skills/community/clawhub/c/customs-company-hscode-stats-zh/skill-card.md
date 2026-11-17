## Description:

查询公司海关贸易HS编码维度统计数据，用于分析HS编码分布、贸易量分解和月度贸易趋势。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade, sourcing, logistics, and supply-chain teams use this skill to inspect a company's customs trade composition by HS code, including monthly trade trends and product category concentration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages an Upkuajing API key and its documentation includes a command that can display the local .env file.

Mitigation: Do not expose the key in agent transcripts; store it with restrictive local permissions or a secret manager and rotate it if disclosure is suspected.

Risk: Normal trade-statistics queries are paid API calls, and helper scripts can create recharge-payment URLs.

Mitigation: Confirm pricing and obtain explicit user approval before running billable queries or payment-related actions.

Risk: Confirmed error reports may send request context and response details to the platform.

Mitigation: Submit reports only after user confirmation and avoid including secrets or unnecessary sensitive business data in the report context.

Risk: The shared request helper performs a version check against the Upkuajing service and writes a local version cache.

Mitigation: Review this network behavior and local cache creation before deploying the skill in restricted environments.

## Reference(s):

- [公司贸易HS编码维度统计 API 参考](references/customs-company-hscode-stats-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-company-hscode-stats-zh)
- [Upkuajing](https://www.upkuajing.com)
- [Upkuajing Developer Platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON API results from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; billable query calls require explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
