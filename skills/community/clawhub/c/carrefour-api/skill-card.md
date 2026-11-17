## Description:

Retrieve structured Carrefour product, price, promotion, nutrition, review, and store information across France, Argentina, Romania, and Belgium through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to retrieve Carrefour product and store information for shopping research, price comparison, promotion tracking, and catalog enrichment.

### Deployment Geography for Use:

France, Argentina, Romania, and Belgium; store lookup and store services are documented for France.

## Known Risks and Mitigations:

Risk: Store lookup may send a user's postal code to Scavio, and the available security review notes there is no privacy notice for this location use.

Mitigation: Tell users when a postal code will be sent to Scavio, and request it only when store-specific information is needed.

## Reference(s):

- [Scavio Carrefour API documentation](https://scavio.dev/docs/carrefour-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api)
- [Scavio Carrefour API overview](https://scavio.dev/carrefour-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON results with brief explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product, price, promotion, nutrition, review, and store data; availability varies by market and endpoint.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
