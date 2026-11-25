## Description:

当用户需要撰写或优化商品详情页、商品介绍和购买 FAQ 时使用。提供商品链接或商品资料，输出商品详情页结构、分段文案与购买 FAQ；可按需参考同类商品。在线商品能力支持抖音与小红书，已有资料可直接写作。来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce sellers and content teams use this skill to draft or revise product detail pages, product descriptions, and purchase FAQs from supplied product information or supported Douyin and Xiaohongshu product details. It can consult a small number of comparable listings when the user requests that research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an automatically selected, unpinned CLI package version; a compromised future release could run with the user's permissions. Scanner analysis was partial, so the security evidence is incomplete.

Mitigation: Before online lookups, verify and pin the CLI to a trusted release where possible, and limit the credentials and filesystem access available to its runtime.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/devinchen2014/skills/ecommerce-detail-copywriter)
- [SocialDataX product and API information](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown product-page copy with sections, product details, and purchase FAQs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source notes and missing-information prompts; separates supported product facts from suggested marketing language.]

## Skill Version(s):

0.1.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
