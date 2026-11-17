## Description:

Search Ashley Furniture and its licensed storefronts for current product prices, sale labels, product details, reviews, deals, and store information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can find Ashley product prices and sale labels, review product details and customer feedback, browse deals, and locate stores. They can track prices over time by saving readings with the market and returned US price-zone context.

### Deployment Geography for Use:

United States for all endpoints; Canada, Mexico, the Philippines, Saudi Arabia, and Türkiye for product search and details.

## Known Risks and Mitigations:

Risk: API requests and store-search coordinates are sent to Scavio, and the security evidence notes a privacy notice concern with some reference checks incomplete.

Mitigation: Review Scavio's privacy information before use and share only location data you are comfortable sending.

## Reference(s):

- [Ashley Furniture API overview](https://scavio.dev/ashley-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api)
- [Ashley search documentation](https://scavio.dev/docs/ashley-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api)
- [Ashley product documentation](https://scavio.dev/docs/ashley-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api)
- [Ashley category documentation](https://scavio.dev/docs/ashley-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api)
- [Ashley deals documentation](https://scavio.dev/docs/ashley-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api)
- [Ashley store locator documentation](https://scavio.dev/docs/ashley-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api)
- [Ashley store details documentation](https://scavio.dev/docs/ashley-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=ashley-furniture-api)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured product, price, review, deal, and store data in JSON, with concise text summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices use the market currency; US results include the returned ZIP code and price zone.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
