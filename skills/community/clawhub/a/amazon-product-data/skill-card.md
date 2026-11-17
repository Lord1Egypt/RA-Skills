## Description:

Helps agents search Amazon products, retrieve ASIN details, and compare seller offers across supported marketplaces through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers, researchers, and developers use this skill to find Amazon listings, inspect product details, and compare seller prices and availability by ASIN.

### Deployment Geography for Use:

Global (22 supported Amazon marketplaces)

## Known Risks and Mitigations:

Risk: Amazon search terms or ASINs and the authorization key are sent to Scavio.

Mitigation: Use the integration only when that data sharing is acceptable; keep the API key in an environment variable or secret store, not source code.

Risk: Pagination or bulk ASIN lookups can consume paid API credits.

Mitigation: Check the remaining credit balance and confirm costs before deep pagination or bulk requests.

Risk: Prices and availability can change, and the offers endpoint may return only the first page of sellers.

Mitigation: Include the retrieval time and product link, and label incomplete seller lists when more pages are reported.

## Reference(s):

- [Amazon API documentation](https://scavio.dev/docs/amazon-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=amazon-product-data)
- [ClawHub skill listing](https://clawhub.ai/scavio-ai/skills/amazon-product-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands]

**Output Format:** [Markdown with product data, JSON examples, or API request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product links and marketplace-specific prices, ratings, availability, and seller offers when returned by the API.]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
