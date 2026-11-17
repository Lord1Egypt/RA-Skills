## Description:

Optimize shopping-cart top-up plans for Taobao, JD, PDD, Tmall, and local ecommerce promotions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping assistants use this skill to compare cart top-up options, coupon thresholds, add-on item choices, and stacking caveats before checkout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coupon stacking, refundability, shipping, and category restrictions can differ from the skill's estimates at checkout.

Mitigation: Ask users to verify final platform checkout terms before acting on the recommendation.

Risk: Users may overbuy filler items that are not useful just to trigger a discount.

Mitigation: Prefer useful or refundable household items and avoid recommending useless purchases unless the user explicitly optimizes only for lowest immediate price.

Risk: The skill could be asked for account-specific shopping help that would require credentials or session access.

Mitigation: Keep guidance calculation-only and do not request account credentials or platform session access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/cart-optimizer)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with shopping-cart calculations, recommendations, and checkout caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not require account credentials or platform session access.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
