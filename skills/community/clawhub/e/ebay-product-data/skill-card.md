## Description:

Search live eBay listings with price, condition, bids, units sold and watchers, read a listing in full, and look up a seller's profile card as structured JSON. 3 endpoints, 1 credit each. Sold-listing search is currently unavailable (eBay now requires a signed-in account for it).

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research live eBay offers, inspect listing details, review seller profiles, and compare asking prices using available demand signals. It does not provide completed-sale history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches and requested listing or seller identifiers are sent to Scavio, a third-party API provider.

Mitigation: Send only the search terms and identifiers needed for the request, and account for the provider's handling of that data.

Risk: API requests consume credits, and continued use may incur charges.

Mitigation: Store a Scavio-specific key in an environment variable or secret store, and check credit usage before running repeated lookups.

Risk: Live asking prices may be mistaken for completed sale prices.

Mitigation: State that sold-history search is unavailable and present asks with units sold, watchers, and bids as demand signals rather than sale prices.

## Reference(s):

- [Scavio eBay search documentation](https://scavio.dev/docs/ebay-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=ebay-product-data)
- [Scavio eBay product documentation](https://scavio.dev/docs/ebay-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=ebay-product-data)
- [Scavio eBay seller documentation](https://scavio.dev/docs/ebay-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=ebay-product-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=ebay-product-data)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON listing, product, and seller data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live asking prices and demand signals; completed-sale history is unavailable.]

## Skill Version(s):

1.0.6 (source: evidence.json release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
