## Description:

Searches 1688 products through the ClawEC API and returns prices, sales volume, links, seller information, and AI suggestions for sourcing research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, sourcing teams, and developers use this skill to search 1688 product listings, compare suppliers by price and sales signals, and summarize product-sourcing observations from ClawEC results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and the user-provided ClawEC API key are sent to clawec.com.

Mitigation: Use an API key intended only for ClawEC and avoid submitting sensitive search terms unless sharing them with the service is acceptable.

Risk: Product-search results and AI suggestions can be incomplete, stale, or unsuitable for a purchasing decision.

Mitigation: Review supplier details, prices, sales signals, and product links before acting on the recommendations.

## Reference(s):

- [1688 Product Search Response Schema](references/response-schema.md)
- [ClawEC API Base URL](https://www.clawec.com/api)
- [ClawEC 1688 Product Search Endpoint](https://www.clawec.com/api/aigc/tool/1688_product_search_lite)
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/clawec-1688-product-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with comparison tables and optional shell commands; raw API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided CLAWEC_API_KEY and sends search keywords to clawec.com.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
