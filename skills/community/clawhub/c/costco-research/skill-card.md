## Description:

Researches Costco products, categories, warehouse stock/availability, and reviews using the Crawlora API, returning clean JSON. Use when the user asks to find a Costco product, check delivery/warehouse availability, browse Costco categories, or pull Costco product reviews — instead of scraping Costco.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers can use the skill to find and compare Costco products, check US delivery availability, browse reviews, and locate nearby warehouses. It returns product and location results as normalized JSON for an agent to summarize or compare.

### Deployment Geography for Use:

United States (availability lookups require a US ZIP code and state)

## Known Risks and Mitigations:

Risk: Search terms and any ZIP/state or coordinates used for lookups are sent to Crawlora; API use can consume credits.

Mitigation: Share only the location detail needed, review Crawlora's privacy practices, and account for API-credit costs.

Risk: The Crawlora API key is required to make requests.

Mitigation: Keep the key in CRAWLORA_API_KEY and protect it from disclosure.

## Reference(s):

- [Costco endpoint reference](reference/endpoints.md)
- [Crawlora API access](https://crawlora.net)
- [Costco Research on ClawHub](https://clawhub.ai/crawlora-org/skills/costco-research)

## Skill Output:

**Output Type(s):** [JSON, Product and availability information, Comparison guidance]

**Output Format:** [Normalized JSON results with concise product, review, delivery, and warehouse summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect the returned Costco data; delivery availability lookups are US-only.]

## Skill Version(s):

1.0.16 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
