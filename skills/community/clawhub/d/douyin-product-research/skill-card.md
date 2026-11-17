## Description:

当用户需要做抖音电商选品、抖音小店类目研究或整理候选商品时使用。输入类目、预算与筛选条件，输出候选清单、入选理由和需要进一步核实的问题。来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

供抖音电商卖家或选品人员根据类目或关键词、预算和筛选条件初筛候选商品，并复核相关商品详情。输出候选清单、匹配理由和需要进一步核实的问题。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags repeated use of an unpinned CLI that may change between runs and could expose local credentials or files; the scan is partial because several local references could not be resolved.

Mitigation: Review the CLI release before use and run it only in an environment whose credential and file access you are comfortable granting.

Risk: Search terms and product identifiers are sent to SocialDataX and could contain confidential or personal information.

Mitigation: Keep confidential and personal information out of searches and product identifiers.

## Reference(s):

- [SocialDataX API Key information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/douyin-product-research)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown table with candidate products, visible details, selection reasons, sources, and follow-up checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Initial screening from one search page, showing up to five candidates and reviewing two to three relevant product details; results do not establish market-wide sales or profitability.]

## Skill Version(s):

0.1.6 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
