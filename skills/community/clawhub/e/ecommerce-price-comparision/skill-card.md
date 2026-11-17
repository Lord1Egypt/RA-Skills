## Description:

Compare products across JD, Taobao, Tmall, Pinduoduo, and Douyin Mall by normalizing product identity, standardizing price basis, detecting purchase risk, and producing decision-ready recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongtao-xiang](https://clawhub.ai/user/hongtao-xiang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to compare Chinese e-commerce listings for the same product across JD, Taobao, Tmall, Pinduoduo, and Douyin Mall. It supports risk-aware shopping guidance by separating true same-product matches from near-equivalent or non-comparable listings and by distinguishing lowest price, best value, and safest purchase options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping recommendations could be mistaken for authorization to purchase or provide account data.

Mitigation: Treat outputs as shopping advice only; do not provide credentials, private session data, payment details, or approval for autonomous checkout.

Risk: Visible prices may depend on coupons, membership, group-buy, livestream, subsidy, shipping, or pre-sale conditions.

Mitigation: Verify the final payable price and all activation conditions on the merchant page before making a purchase decision.

Risk: Similar listings may differ by model, capacity, package contents, condition, seller channel, or version.

Mitigation: Use strict same-product matching and downgrade or exclude listings when identity or price basis is uncertain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongtao-xiang/skills/ecommerce-price-comparision)
- [Comparison traps](artifact/comparison-traps.md)
- [Parsing and normalization](artifact/parsing-and-normalization.md)
- [Matching rules](artifact/matching-rules.md)
- [Pricing rules](artifact/pricing-rules.md)
- [Decision framework](artifact/decision-framework.md)
- [Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown narrative with structured comparison results and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes normalized product identity, platform-by-platform comparison, lowest price, best value, safest purchase, risk notes, price conditions, and uncertainty disclosures.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
