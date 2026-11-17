## Description:

This agent searches Chinese tender and award notices and analyzes bidder, supplier, company, and market data to support vendor-side bid research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

External bidders and suppliers use the agent to find tender and award notices, review competitors and potential partners, and compare procurement or award trends. It presents findings in clear tables or charts to support bid research.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Queries for data can consume paid credits.

Mitigation: Check account credits before broad searches and limit requests to the information needed.

Risk: Optional device-based registration can share a stable MAC-derived identifier.

Mitigation: Use an existing API key to skip registration, or review the consent prompt and decline if you do not want to share the identifier.

Risk: Saved API keys and generated login links can expose account access.

Mitigation: Keep the key and generated login links private.

Risk: The provider's server-side privacy practices are unverified.

Mitigation: Review the provider's privacy terms before sharing information beyond what a query requires.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liu-jiapeng/skills/bidding-yifangbao)
- [Tender search API guidance](artifact/references/api-search.md)
- [Company data API guidance](artifact/references/api-company.md)
- [Market analysis API guidance](artifact/references/api-market.md)
- [Company registry and data interpretation guidance](artifact/references/api-registry.md)
- [Account API guidance](artifact/references/api-account.md)
- [Optional account registration guidance](artifact/references/auto-register.md)
- [Product and skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Tables, Charts]

**Output Format:** [Markdown summaries with tables or charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results and analysis are scoped to the user's requested query; unavailable fields are left unspecified.]

## Skill Version(s):

2.0.8 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
