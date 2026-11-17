## Description:

Query Foot Locker catalog and release data across 13 markets, including product prices, size availability, nearby stores, reviews, and shopper Q&A.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up Foot Locker releases, products, prices, size availability, nearby US stores, customer reviews, and shopper questions across supported storefronts.

### Deployment Geography for Use:

United States, Canada, United Kingdom, and the 10 additional Foot Locker markets listed in the skill documentation.

## Known Risks and Mitigations:

Risk: Search terms and location details are sent to Scavio, and the security evidence notes a location privacy concern.

Mitigation: Use only the search and location details needed for the lookup, and avoid sharing sensitive information.

Risk: Security inspection coverage is partial, with medium confidence and unresolved local path-like references.

Mitigation: Review the skill before use and keep its API access limited to the documented Foot Locker lookups.

Risk: Product listings and store availability can become stale and do not represent reserved or guaranteed inventory.

Mitigation: Check the listing timestamp, refresh product availability before reporting it, and call a store before traveling.

Risk: The skill requires an API key that could be exposed if placed in source code or shared text.

Mitigation: Keep SCAVIO_API_KEY in an environment variable or secret store and do not commit or disclose it.

## Reference(s):

- [Foot Locker API overview](https://scavio.dev/footlocker-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api)
- [Release calendar documentation](https://scavio.dev/docs/footlocker-releases?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api)
- [Search documentation](https://scavio.dev/docs/footlocker-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api)
- [Product documentation](https://scavio.dev/docs/footlocker-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api)
- [Category documentation](https://scavio.dev/docs/footlocker-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api)
- [Brand documentation](https://scavio.dev/docs/footlocker-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api)
- [Deals documentation](https://scavio.dev/docs/footlocker-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api)
- [Stores documentation](https://scavio.dev/docs/footlocker-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api)
- [Store availability documentation](https://scavio.dev/docs/footlocker-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api)
- [Reviews documentation](https://scavio.dev/docs/footlocker-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api)
- [Questions documentation](https://scavio.dev/docs/footlocker-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Guidance]

**Output Format:** [Structured JSON responses with concise summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each endpoint call costs 1 credit; an SCAVIO_API_KEY is required.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
