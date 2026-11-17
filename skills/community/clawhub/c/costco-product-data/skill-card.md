## Description:

Guides agents in using Scavio's Costco API to find products, compare online and warehouse prices, check stock and gas prices, and retrieve coupons, deals, clearance items, and reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers, analysts, and developers use the skill to look up Costco products and warehouse availability, compare prices, and track promotions using Scavio's API.

### Deployment Geography for Use:

Global; available Costco data and features vary by country, and coupons are US only.

## Known Risks and Mitigations:

Risk: Costco lookup inputs, including location and item identifiers, are sent to a third-party provider.

Mitigation: Use Scavio only when sharing the requested lookup inputs is acceptable.

Risk: The API key may be exposed if copied into shared outputs or configuration files.

Mitigation: Store SCAVIO_API_KEY in environment or secret storage and do not include it in responses.

Risk: Broad pagination or multi-warehouse requests can consume paid API credits.

Mitigation: Check expected credit use before running large or repeated lookups.

Risk: Optional SDK or MCP packages add third-party software dependencies.

Mitigation: Review those packages separately before installation.

## Reference(s):

- [Scavio Costco search documentation](https://scavio.dev/docs/costco-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data)
- [Scavio Costco prices documentation](https://scavio.dev/docs/costco-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data)
- [Scavio Costco availability documentation](https://scavio.dev/docs/costco-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance and structured JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses include item, price, availability, or promotion data depending on the endpoint.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
