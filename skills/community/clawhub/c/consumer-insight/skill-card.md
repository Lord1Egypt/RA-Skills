## Description:

帮助卖家基于 Amazon 评论样本生成消费者洞察报告，梳理用户画像、购买动因、使用场景、痛点、竞品替代关系与产品机会，并将结论关联到评论证据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon 卖家、产品团队和市场人员可用它分析商品评论，了解消费者动因、痛点、使用场景和竞品差异，并为产品规划与市场汇报准备有评论依据的洞察。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands described as quotes can spend credits, and collection plus analysis charges may exceed the automatic-spending limit.

Mitigation: Set autoconfirm off before generating reports, review the combined collection and analysis cost, and approve it explicitly.

Risk: Weekly collection can create recurring charges when enabled.

Mitigation: Keep collection manual unless recurring fees are approved, and obtain fresh approval for quotes that were not answered.

## Reference(s):

- [ARI CLI 与 API 参考](references/reference.md)
- [ARI 产品运营工作台](https://ari.funewa.com/zh/operations)
- [ARI 报告中心](https://ari.funewa.com/zh/reports)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Markdown consumer insight reports and concise answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are tied to sampled review evidence and report the applicable data window.]

## Skill Version(s):

1.5.3 (source: frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
