## Description:

Retrieves current Fashion Nova prices, sale details, per-size availability, product reviews, collections, and similar styles across supported storefronts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to find Fashion Nova products, summarize sale prices and size availability, compare storefront prices in local currencies, and retrieve product reviews for users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send the configured API key to api.scavio.dev.

Mitigation: Use the skill only if you trust Scavio with the key, keep the key in an environment variable or secret store, and avoid exposing it in source files or logs.

## Reference(s):

- [Fashion Nova API documentation](https://scavio.dev/docs/fashionnova-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api)
- [Scavio Fashion Nova API overview](https://scavio.dev/fashionnova-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=fashion-nova-api)
- [ClawHub release page](https://clawhub.ai/scavio-ai/skills/fashion-nova-api)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON data with concise text summaries and explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current storefront snapshots; prices use local currencies and availability can change between requests.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
