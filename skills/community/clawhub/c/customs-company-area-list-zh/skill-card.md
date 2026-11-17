## Description:

查询公司海关贸易区域列表数据，返回国家或地区级贸易次数、金额、数量、重量和占比，用于公司贸易市场分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade teams and market analysts use this skill to inspect a company's trade distribution by country or region, including transaction count, amount, quantity, weight, and market share. It supports market entry analysis, customer distribution research, and regional customs trade intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a real paid customs-data API and account operations tied to an API key.

Mitigation: Review the skill before installing, use it only if you trust Upkuajing with submitted company-trade queries, and require explicit user confirmation before paid queries or recharge/payment URL creation.

Risk: The documented key-check flow can expose the API key if an agent prints the contents of ~/.upkuajing/.env.

Mitigation: Verify key presence without printing the key value, restrict permissions on ~/.upkuajing and its .env file, and treat the API key as a secret.

## Reference(s):

- [公司贸易区域列表 API 参考](references/customs-company-area-list-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)
- [跨境魔方](https://www.upkuajing.com)
- [跨境魔方开放平台](https://developer.upkuajing.com/)
- [跨境魔方开放平台价格说明](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; paid API calls require user confirmation before execution.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
