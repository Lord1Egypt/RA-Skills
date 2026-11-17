## Description:

Cross-platform buying decision skill that compares the same product across Taobao, Tmall, JD, PDD, VIPSHOP, and similar marketplaces, distinguishes flagship, self-operated, and third-party sellers, normalizes coupon-adjusted price and fulfillment tradeoffs, and outputs the optimal purchase path instead of a raw price table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT

## Use Case:

External shoppers and shopping-assistant agents use this skill to compare equivalent listings across Chinese marketplaces, normalize final payable price and seller risk, and recommend a concrete purchase path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live prices, coupons, seller badges, delivery promises, warranty terms, and return policies can change or differ by account or region.

Mitigation: Verify current listing pages, checkout price, seller identity, warranty or invoice terms, and return policy before buying.

Risk: Shopping advice could be misread as permission to transact or use private account information.

Mitigation: Keep the skill advisory only; do not provide credentials, payment details, or consent for it to place orders or send purchase messages.

Risk: Listings may look comparable while differing by SKU, bundle, seller type, warranty, shipping, or payment conditions.

Mitigation: Normalize model, variant, bundle, seller path, warranty, shipping, and payment conditions before comparing options.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/buying)
- [Platform Lenses](artifact/references/platform-lenses.md)
- [Risk-Adjusted Pricing](artifact/references/risk-adjusted-pricing.md)
- [Purchase Paths](artifact/references/purchase-paths.md)
- [Example Prompts](artifact/references/example-prompts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style recommendation with comparison notes and action-oriented purchase paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include final verdicts, risk-adjusted price explanations, backup routes, and next-step buying guidance.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
