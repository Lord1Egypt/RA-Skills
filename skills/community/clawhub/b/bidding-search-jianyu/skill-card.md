## Description:

Search tender and award notices, track project opportunities, and analyze companies, suppliers, brands, and historical prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, procurement, and market research teams can use this skill to find tender opportunities, follow project stages, and review company, competitor, brand, and pricing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An account key could be exposed if registration response content redirects the credential flow.

Mitigation: Restrict the acknowledgment flow to the provider endpoint and keep API keys and generated login links private.

Risk: Search terms leave the user's environment, and searches may consume account credits.

Mitigation: Send only queries needed for the request and check credit use before broad searches.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liu-jiapeng/skills/bidding-search-jianyu)
- [Provider skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Bid search API guide](references/api-search.md)
- [Company analysis API guide](references/api-company.md)
- [Market analysis API guide](references/api-market.md)
- [Company registry API guide](references/api-registry.md)
- [Account API guide](references/api-account.md)
- [Credential setup guide](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Concise summaries with Markdown tables or charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results follow the requested filters and available provider data.]

## Skill Version(s):

2.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
