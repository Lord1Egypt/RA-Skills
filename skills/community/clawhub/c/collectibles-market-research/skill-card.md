## Description:

Researches public trading-card and sports-collectible markets through the Crawlora API — card identity, PSA certification and price-guide evidence, live listings, auctions, sold items, and market trends. Use when the user wants a sourced collector or buying brief, not authentication, appraisal guarantees, or a purchase action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Collectors and buyers use the skill to assemble sourced briefs about card identity, PSA reference data, public listings, auctions, sold items, and market trends. It helps compare evidence while keeping asking prices, bids, realized prices, and guide values distinct.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill requires a Crawlora API key and sends requests to api.crawlora.net.

Mitigation: Provide a Crawlora key only when using the skill, and review the helper and its documented route scope before running it.

Risk: The security review was partial because a local reference could not be resolved, leaving some evidence incomplete.

Mitigation: Treat results as bounded public-data evidence, retain source URLs, and avoid claims of guaranteed value or authenticity.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [Crawlora API](https://api.crawlora.net/api/v1)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, API Calls]

**Output Format:** [Sourced collector or buying brief in Markdown, with source URLs and observed evidence; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence counts and observed ranges where available; distinguish guide values, active asks, bids, and sold prices. Public data only; no purchase, bid, authentication, or grading action.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
