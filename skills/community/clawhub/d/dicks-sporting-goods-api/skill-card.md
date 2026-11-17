## Description:

Search Dick’s Sporting Goods products and deals, compare per-size prices, check nearby store stock, and retrieve recent product reviews through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and retail researchers use this skill to find Dick’s products and deals, compare prices by size or color, check nearby store availability, and review recent customer feedback.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: A store availability lookup shares the ZIP code and selected products with Scavio; the security evidence notes that the skill has no privacy warning for this.

Mitigation: Tell the user before a location lookup and make it only when they want a nearby-stock check.

Risk: The security review was partial because local references could not be resolved, so its benign verdict has medium confidence.

Mitigation: Review unresolved references and complete the security checks before relying on the skill.

## Reference(s):

- [Scavio Dick’s product API documentation](https://scavio.dev/docs/dicks-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api)
- [Scavio Dick’s API overview](https://scavio.dev/dicks-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON product, pricing, availability, and review data with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices and availability reflect the time of the API response.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
