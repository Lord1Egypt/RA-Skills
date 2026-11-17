## Description:

零配置即装即用的跨平台比价工具，一次搜索同时查询京东、淘宝、拼多多三大平台同款商品价格，自动识别品牌和优惠券，返回最优购买建议。增强超时容错，数据通过腾讯云代理安全转发。暑期全网比价，多平台对比找最低价

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to compare product prices from Chinese ecommerce platforms by entering a product keyword or product link. It returns price-comparison results, coupon-aware purchase guidance, and purchase links where available, but it does not place orders or track shipments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and pasted product links are sent through the publisher's Tencent cloud proxy.

Mitigation: Review the skill before installation and avoid submitting sensitive, private, or account-specific product links or search text.

Risk: Advertised platform coverage may not match the implemented behavior, including Pinduoduo and full Taobao coverage.

Mitigation: Treat comparison results as advisory and confirm prices, coupons, platform availability, and product identity directly on the ecommerce platforms before buying.

Risk: The artifact contains an embedded shared proxy token.

Mitigation: Prefer a publisher update that removes the embedded token and uses installer-provided credentials or a documented proxy authentication flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-shopping/skills/best-price)
- [Publisher profile](https://clawhub.ai/user/cn-shopping)
- [京东自营精选](https://clawhub.ai/cn-shopping/jd-selection)
- [淘宝精选](https://clawhub.ai/cn-shopping/taobao-selection)
- [拼多多精选](https://clawhub.ai/cn-shopping/pdd-selection)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown or plain text with price comparisons, coupons, recommendations, and purchase links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on publisher proxy availability and ecommerce platform data coverage.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
