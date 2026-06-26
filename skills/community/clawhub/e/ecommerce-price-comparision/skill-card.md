## Description: <br>
Compare products across JD, Taobao, Tmall, Pinduoduo, and Douyin Mall by normalizing product identity, standardizing price basis, detecting purchase risk, and producing decision-ready recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hongtao-Xiang](https://clawhub.ai/user/Hongtao-Xiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to compare the same product across major Chinese e-commerce platforms, normalize payable prices, and receive lowest-price, best-value, and safest-purchase recommendations with risks and conditions disclosed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live prices, coupons, shipping, inventory, seller status, and platform conditions can change or be unavailable to the agent. <br>
Mitigation: Verify current prices, coupon eligibility, shipping, seller legitimacy, return policies, and platform-specific conditions directly on the shopping platform before purchase. <br>
Risk: A low visible price may reflect a different product variant, deposit, pre-sale, group-buy, membership, livestream, subsidy, or other conditional basis. <br>
Mitigation: Use only high-confidence same-product matches for strict lowest-price conclusions and label conditional or uncertain prices before recommending. <br>
Risk: Raw cheapest-listing recommendations can be misleading when seller trust, after-sales support, package contents, condition, or delivery reliability differ. <br>
Mitigation: Present separate lowest-price, best-value, and safest-purchase options with trade-offs and risk notes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Hongtao-Xiang/ecommerce-price-comparision) <br>
- [Publisher Profile](https://clawhub.ai/user/Hongtao-Xiang) <br>
- [Comparison Traps](comparison-traps.md) <br>
- [Parsing and Normalization](parsing-and-normalization.md) <br>
- [Matching Rules](matching-rules.md) <br>
- [Pricing Rules](pricing-rules.md) <br>
- [Decision Framework](decision-framework.md) <br>
- [Examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes normalized target product, platform comparison, lowest price option, best value option, safest purchase option, risk notes, price conditions, and uncertainty disclosures.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
