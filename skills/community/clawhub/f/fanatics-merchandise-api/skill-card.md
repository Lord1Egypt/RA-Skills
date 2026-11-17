## Description:

Find Fanatics merchandise across supported storefronts, compare prices and availability, and retrieve product details and customer reviews as structured data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shopping and product research agents use this skill to find licensed Fanatics merchandise, compare current prices across supported storefronts, check size availability and delivery estimates, and review customer feedback.

### Deployment Geography for Use:

Global: United States, United Kingdom, Germany, France, Spain, Italy, Japan, and Canada, plus US league shops.

## Known Risks and Mitigations:

Risk: The skill sends requests to an external service using SCAVIO_API_KEY, and the security assessment advises using that service only if trusted.

Mitigation: Keep the key in an environment variable or secret store, and use the service only if its handling of requests and credentials is acceptable.

Risk: Prices and size availability can change after the data is retrieved.

Mitigation: Check the product endpoint before reporting a current price or size, and include the data timestamp.

Risk: Fanatics reviews are pooled across a product style and can refer to different items.

Mitigation: Check each review's product ID and title before attributing its text to a specific item.

Risk: The skill documentation notes that Fanatics terms restrict automated extraction for commercial purposes.

Mitigation: Review and follow Fanatics' terms for the intended use; do not use the skill for checkout or resale automation.

## Reference(s):

- [Fanatics API overview](https://scavio.dev/fanatics-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api)
- [Fanatics search documentation](https://scavio.dev/docs/fanatics-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api)
- [Fanatics product documentation](https://scavio.dev/docs/fanatics-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api)
- [Fanatics browse documentation](https://scavio.dev/docs/fanatics-browse?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api)
- [Fanatics deals documentation](https://scavio.dev/docs/fanatics-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api)
- [Fanatics reviews documentation](https://scavio.dev/docs/fanatics-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=fanatics-merchandise-api)

## Skill Output:

**Output Type(s):** [JSON, Product and pricing data, Availability and delivery information, Customer review data]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Five operations; each API call costs one credit. Price and availability results include source timestamps and can change.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
