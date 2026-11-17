## Description:

Searches Chinese shopping platforms for coupon-adjusted prices and returns ranked product listings with purchase links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ablejimmy](https://clawhub.ai/user/ablejimmy)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and their agents compare listed coupon-adjusted prices across Chinese e-commerce platforms and find purchase links for matching products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping search terms are sent to an external shopping service.

Mitigation: Do not include sensitive personal information in product keywords.

Risk: Purchase links may include rebate or referral tracking.

Mitigation: Review the destination and final price before buying; use the result only as a price reference if tracking is unwanted.

## Reference(s):

- [Best Price Finder on ClawHub](https://clawhub.ai/ablejimmy/skills/best-price-finder)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Ranked Markdown table by default; JSON array when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes product, platform, shop, listed and coupon-adjusted prices, coupon, monthly sales, and purchase link when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
