## Description:

查询公司海关贸易产品列表数据，用于获取产品名称的贸易次数、金额、数量和关联HS编码，支持产品组合分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade teams and agents use this skill to query a company's customs trade product list, quantify each product's trade count, amount, quantity, weight, and share, and connect products to HS codes for market analysis and competitor tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed or persisted unsafely in ~/.upkuajing/.env.

Mitigation: Use an environment variable or protected secret store where possible, restrict the key file to owner-only access, and do not print or paste ~/.upkuajing/.env contents.

Risk: The skill can create API keys, query account and balance information, create recharge payment URLs, report errors to the vendor, and run a background version check when API requests are made.

Mitigation: Review before installation and require explicit user confirmation before paid queries, recharge flow, or vendor error reporting.

## Reference(s):

- [公司贸易产品列表 API 参考](artifact/references/customs-company-product-list-api.md)
- [Agent调用Skill异常上报 API 参考](artifact/references/skill-error-report-api.md)
- [跨境魔方官网](https://www.upkuajing.com)
- [跨境魔方开放平台](https://developer.upkuajing.com/)
- [开放平台价格说明](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-company-product-list-zh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and API result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce paginated customs trade product data summaries and guidance for API key setup, pricing checks, recharge flow, and vendor error reporting.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
