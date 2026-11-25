## Description:

用于根据用户提供的类目、预算和筛选条件研究抖音电商商品，并输出候选清单、入选理由与待核实问题；来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向抖音电商经营者和选品研究人员，按给定类目、预算与筛选条件初筛商品，并整理可见信息、匹配理由和后续核实事项。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags automatic use of the unpinned socialdatax-skills@latest package as a supply-chain risk involving account permissions and API credentials.

Mitigation: Review and pin the package version before installation, and run it with only the permissions and credentials needed for the task.

## Reference(s):

- [SocialDataX API and key management](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/douyin-product-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown table with candidate products, selection reasons, sources, and follow-up checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Initial screening uses one search page, shows up to five candidates, and checks details for the two or three most relevant items. Findings depend on information returned by the platform.]

## Skill Version(s):

0.1.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
