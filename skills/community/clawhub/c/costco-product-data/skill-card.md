## Description:

Search Costco products and retrieve structured product details, online and warehouse prices, stock status, gas prices, coupons, deals, clearance items, and reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can ask an agent to find Costco products and retrieve current product details, online and warehouse prices, stock status, gas prices, coupons, deals, clearance items, and reviews. The skill returns the API data for comparison, research, or catalog enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends product queries and location details, such as a ZIP code or coordinates, to Scavio.

Mitigation: Use only the location detail needed for the search, and share product queries with Scavio only when comfortable doing so.

## Reference(s):

- [ClawHub release](https://clawhub.ai/scavio-ai/skills/costco-product-data)
- [Costco API overview](https://scavio.dev/costco-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data)
- [Costco search documentation](https://scavio.dev/docs/costco-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data)
- [Costco prices documentation](https://scavio.dev/docs/costco-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data)
- [Costco availability documentation](https://scavio.dev/docs/costco-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data)
- [Costco gas documentation](https://scavio.dev/docs/costco-gas?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data)
- [Costco coupons documentation](https://scavio.dev/docs/costco-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data)
- [Costco clearance documentation](https://scavio.dev/docs/costco-clearance?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=costco-product-data)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON containing Costco product, price, stock, warehouse, gas, coupon, deal, clearance, category, autocomplete, or review data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Data is returned by the skill's API calls for use in the agent's response.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
