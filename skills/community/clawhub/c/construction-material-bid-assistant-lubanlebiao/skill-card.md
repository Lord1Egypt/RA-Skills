## Description:

施工建材采招助手-鲁班乐标，当查询词包含建材、钢材、管材、机械或特定建筑材料型号时调用，必须调用价格趋势查询和Top品牌接口，输出建材历史单价和主要供应商名单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thuanlynham-stack](https://clawhub.ai/user/thuanlynham-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Construction procurement professionals can use this skill to review bidding activity for building materials and compare historical awarded prices, leading brands, and suppliers.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Automatic registration can use a MAC hash that consistently identifies a device.

Mitigation: Prefer a user-supplied API key; otherwise review the device information requested and give consent before registration.

Risk: Search terms are sent to the service provider, and successful queries may consume paid credits.

Mitigation: Send only the terms needed for the requested analysis and check account credits before paid queries.

Risk: Saved API keys and automatic-login links can expose account access if shared.

Mitigation: Keep API keys and login links private.

## Reference(s):

- [Bid search and query guidance](references/api-search.md)
- [Company information and analysis guidance](references/api-company.md)
- [Market, brand, and price trend guidance](references/api-market.md)
- [Business registry data definitions and interpretation limits](references/api-registry.md)
- [Account and consumption guidance](references/api-account.md)
- [API key registration guidance](references/auto-register.md)
- [Skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Chinese-language summaries and Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize bidding records, historical unit prices, brands, and suppliers with relevant query conditions and data caveats.]

## Skill Version(s):

1.0.11 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
