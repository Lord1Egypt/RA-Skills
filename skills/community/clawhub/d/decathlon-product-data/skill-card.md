## Description:

Decathlon product data as structured JSON - product search and full item detail with pricing, ratings, images and variants across 7 country domains (FR, ES, IT, IN, UK, PT, international). 2 endpoints, 2 credits each.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product data teams can search Decathlon stores and retrieve product details to compare prices, enrich catalogs, and inspect availability, ratings, images, and variants across the supported country domains.

### Deployment Geography for Use:

France, Spain, Italy, India, the United Kingdom, Portugal, and Decathlon's international domain

## Known Risks and Mitigations:

Risk: Search terms, product identifiers, and API authentication are sent to Scavio; requests consume credits.

Mitigation: Avoid sensitive search terms, keep SCAVIO_API_KEY in an environment variable or secret store, and monitor credit usage.

## Reference(s):

- [Decathlon API overview](https://scavio.dev/decathlon-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=decathlon-product-data)
- [Decathlon search documentation](https://scavio.dev/docs/decathlon-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=decathlon-product-data)
- [Decathlon product documentation](https://scavio.dev/docs/decathlon-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=decathlon-product-data)
- [ClawHub skill listing](https://clawhub.ai/scavio-ai/skills/decathlon-product-data)

## Skill Output:

**Output Type(s):** [JSON data, Guidance]

**Output Format:** [Structured JSON product search results and product details, with usage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices use local currency cents; each API endpoint request consumes 2 credits.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
