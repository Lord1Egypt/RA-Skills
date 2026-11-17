## Description:

Search Chewy listings and retrieve product prices, Autoship discounts, ratings, specifications, ingredients, promotions, and size or flavor variants as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Chewy listings and retrieve product details such as one-time and Autoship prices, ratings, specifications, and variants. It supports pet-supply discovery and product comparisons using current API results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product search requests and queries are sent to Scavio, and each API call consumes credits.

Mitigation: Use only necessary calls, account for the 10-credit cost per call, and keep SCAVIO_API_KEY out of source control.

## Reference(s):

- [Chewy search API documentation](https://scavio.dev/docs/chewy-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=chewy-product-data)
- [Chewy product API documentation](https://scavio.dev/docs/chewy-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=chewy-product-data)
- [Scavio Chewy API overview](https://scavio.dev/chewy-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=chewy-product-data)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON product data with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search returns up to 36 products per page; product details cover one product and its variants. Each API call costs 10 credits.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
