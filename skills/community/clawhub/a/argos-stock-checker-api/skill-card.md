## Description:

Checks Argos UK product availability, prices, stores, reviews and related product information through Scavio's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can query Argos UK stock near a postcode, delivery availability, prices, stores, product details, reviews and related catalog data, then use the returned information to answer shopping research questions.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: Requests can send UK postcodes, product identifiers and search queries to Scavio; the security evidence notes that the skill lacks a privacy disclosure.

Mitigation: Before use, review Scavio's data handling and avoid sending location or query information you do not want shared.

Risk: The security analysis is partial because it could not resolve two local path references.

Mitigation: Review the referenced source files and complete a full scan before relying on the security assessment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/argos-stock-checker-api)
- [Scavio Argos API overview](https://scavio.dev/argos-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api)
- [Store stock documentation](https://scavio.dev/docs/argos-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api)
- [Search documentation](https://scavio.dev/docs/argos-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api)
- [Product documentation](https://scavio.dev/docs/argos-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api)
- [Stores documentation](https://scavio.dev/docs/argos-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api)
- [Reviews documentation](https://scavio.dev/docs/argos-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api)
- [Questions documentation](https://scavio.dev/docs/argos-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api)
- [Categories documentation](https://scavio.dev/docs/argos-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api)
- [Category documentation](https://scavio.dev/docs/argos-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api)
- [Deals documentation](https://scavio.dev/docs/argos-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api)
- [Suggestions documentation](https://scavio.dev/docs/argos-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=argos-stock-checker-api)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON data with concise natural-language answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dated live reads; Argos UK only and prices in GBP. Stock is reported as availability states, not unit counts.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
