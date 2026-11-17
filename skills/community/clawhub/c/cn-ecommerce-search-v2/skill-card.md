## Description:

Supports product search and price comparison across Taobao, Tmall, JD.com, Pinduoduo, Xianyu, Xiaohongshu, Douyin, and 1688 with specific product links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vince199907](https://clawhub.ai/user/vince199907)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers, sourcing users, and agents use this skill to collect product listings from major Chinese e-commerce platforms, compare prices, and present purchase-oriented recommendations. It is intended for search and comparison support, not autonomous checkout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may move from shopping comparison into order placement, account changes, or use of saved payment methods.

Mitigation: Require separate explicit confirmation from the user for each transaction, account change, or payment action.

Risk: Listings, prices, availability, seller claims, and authenticity signals may be incomplete, stale, or gated behind platform login.

Mitigation: Verify final product pages, seller details, and checkout terms directly on the platform before relying on the recommendation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vince199907/skills/cn-ecommerce-search-v2)
- [Publisher profile](https://clawhub.ai/user/vince199907)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown price comparison tables with product links and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser or web-search access to supported shopping platforms; prices, stock, authenticity, and seller terms should be verified at time of use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
