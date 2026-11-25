## Description:

当用户需要对比已选商品、比较规格和卖点差异，或准备竞品对照表时使用。输入 2–5 个抖音商品链接或商品 ID，输出注明价格口径、信息缺口和来源的商品差异表。来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

外部用户在比较抖音商品时，可输入 2–5 个自行选定的商品，查看规格、价格条件、可见卖点、信息缺口和来源，以准备可追溯的竞品对照表。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is rated suspicious because it runs an unpinned, automatically fetched package in commands that may access credentials; the scan was partial and cannot establish that the skill is safe.

Mitigation: Avoid installation until the package version is fixed and reviewed; treat the partial scan as inconclusive.

## Reference(s):

- [SocialDataX API access and account information](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Markdown, Analysis]

**Output Format:** [Markdown comparison table with product identifiers or links, specifications, price conditions, visible selling points, missing information, and sources.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares only the 2–5 products selected by the user; marks unavailable details and keeps differing price conditions explicit.]

## Skill Version(s):

0.1.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
