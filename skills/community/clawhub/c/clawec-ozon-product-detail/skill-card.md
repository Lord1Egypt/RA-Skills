## Description:

Uses the ClawEC API to batch query Ozon product details for up to 10 product IDs, including price, sales, conversion, commission, and inventory metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators, cross-border ecommerce sellers, and agent developers use this skill to retrieve and summarize Ozon product-detail metrics for SKU research, competitor product analysis, and batch product checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends queried Ozon item IDs and the user's ClawEC API credential to clawec.com.

Mitigation: Keep the API key in an environment variable or secret store, avoid pasting it into shared logs or chats, and review product IDs before running batch queries.

Risk: Batch queries may expose commercially sensitive product research targets to the ClawEC API service.

Mitigation: Confirm that the item IDs are appropriate to share with ClawEC before executing requests, especially in competitor or confidential sourcing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-ozon-product-detail)
- [Ozon product-detail response schema](references/response-schema.md)
- [ClawEC API base URL](https://www.clawec.com/api)
- [ClawEC Ozon product-detail endpoint](https://www.clawec.com/api/aigc/ec/ozon/data/product/detail)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance, JSON]

**Output Format:** [Chinese Markdown report with optional shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided CLAWEC_API_KEY; product IDs are limited to 10 per API request and should be split into batches when needed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
