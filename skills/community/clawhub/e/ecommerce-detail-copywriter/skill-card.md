## Description:

当用户需要撰写或优化商品详情页、商品介绍和购买 FAQ 时使用。提供商品链接或商品资料，输出商品详情页结构、分段文案与购买 FAQ；可按需参考同类商品。在线商品能力支持抖音与小红书，已有资料可直接写作。来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and commerce teams use this skill to draft or refine product detail pages and purchase FAQs from supplied product information or supported Douyin and Xiaohongshu product data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The changing CLI package could expose credentials or local resources if compromised.

Mitigation: Use the CLI only when you trust its source, keep credentials in the documented private store, and do not expose secrets or unrelated local files during execution.

Risk: Online lookups send product identifiers and search terms to SocialDataX.

Mitigation: Use online lookups only when needed for the requested task, and provide only the supported product identifiers or search terms required.

## Reference(s):

- [SocialDataX API key information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/ecommerce-detail-copywriter)
- [SocialDataX billing](https://socialdatax.com/dashboard/billing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured product copy with purchase FAQs, source notes, and missing information to verify.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
