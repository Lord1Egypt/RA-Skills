## Description:

Searches Shopee products through the ClawEC API and returns product names, prices, sales, ratings, markets, links, and images for product research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace researchers, and ecommerce operators use this skill to search Shopee listings by keyword and optional region, then compare products by price, sales, rating, rank, market, and link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords, selected regions, and the Clawec API key are sent to clawec.com.

Mitigation: Use a dedicated API key, avoid sensitive search terms, and confirm Clawec account and API terms before operational use.

Risk: Shopee search results may be incomplete, stale, unavailable, or returned with API errors such as invalid credentials.

Mitigation: Check API status and credentials on failed requests, and review returned product data before making sourcing or marketplace decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-shopee-product-search)
- [Shopee product search response schema](references/response-schema.md)
- [ClawEC API base](https://www.clawec.com/api)
- [Shopee search endpoint](https://www.clawec.com/api/aigc/ec/shopee_search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables, with optional JSON API responses and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided CLAWEC_API_KEY and sends the keyword and optional region to Clawec.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
