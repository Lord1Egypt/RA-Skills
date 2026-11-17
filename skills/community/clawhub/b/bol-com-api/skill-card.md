## Description:

bol.com API for bol.com competitor prices and marketplace data in the Netherlands and Belgium (EUR; storefronts nl-nl, be-nl, be-fr) - one product by product id, link or EAN with the buy box (price, seller, reference price and its type, delivery promise), offer counts and the cheapest new, fastest new, second-hand and refurbished offers; the 10 lowest-priced offers on one product with price, condition, shipping cost, delivery date and seller rating, plus counts for all its offers; keyword search, category, brand, seller and campaign listings with filters and sorts; seller profiles with rating out of 10, sub-ratings and EU trader data; today's deals and bol promotions such as Black Friday lists. 9 endpoints, 2 credits each (product by EAN 4). No price history, no review paging beyond the first 10.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketplace teams use this skill to retrieve bol.com product, offer, seller, search, promotion, and deal data for competitor price monitoring across the Netherlands and Belgium.

### Deployment Geography for Use:

Netherlands and Belgium

## Known Risks and Mitigations:

Risk: Requests send query details and SCAVIO_API_KEY to api.scavio.dev.

Mitigation: Use the service only for queries you are comfortable sharing with Scavio, and keep the key in environment configuration rather than shared logs.

Risk: The security scan is partial because two local path-like references could not be resolved.

Mitigation: Review the unresolved references and treat the clean verdict as limited to the evidence scanned.

## Reference(s):

- [Scavio bol.com API overview](https://scavio.dev/bolcom-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api)
- [Scavio bol.com endpoint documentation](https://scavio.dev/docs/bolcom-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api)
- [Scavio API rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON with concise explanatory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current marketplace data; no price history or review paging beyond the first 10 reviews.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
