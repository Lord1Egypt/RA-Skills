## Description:

当用户需要提炼商品主图卖点、主副标题或安排商品图片信息层次时使用。提供商品链接或商品资料，输出主图标题、副标题、卖点短句与配图建议；可按需参考同类商品。在线商品能力支持抖音与小红书，已有资料可直接写作。来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and product marketers use this skill to turn product details into concise main-image titles, subtitles, selling-point phrases, and image suggestions. It can read supported Douyin or Xiaohongshu product listings and refer to a small number of comparable products when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because it repeatedly invokes the mutable SocialDataX CLI @latest, creating a supply-chain risk; the available scan is incomplete.

Mitigation: Review the CLI package and version before execution, and prefer a reviewed fixed version over @latest when available.

Risk: Online product lookups may send product URLs or other lookup inputs to SocialDataX.

Mitigation: Use online lookup only for inputs the user is comfortable sharing with SocialDataX; use supplied product details directly when appropriate.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/ecommerce-main-image-copywriter)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown copy with titles, subtitles, selling-point phrases, image suggestions, and source notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usually three variants; each has one title, one subtitle, up to three selling-point phrases, and an image suggestion. Facts are limited to user-provided material or returned product data.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
