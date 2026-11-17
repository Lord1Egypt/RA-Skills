## Description:

分析指定 Amazon ASIN 的 1–3 星评论，归纳负面反馈根因并提出产品与文案改进建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

面向 Amazon 卖家和运营人员，整理指定商品的差评主题与趋势，帮助定位退货诱因并制定产品或商品文案改进方案。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some report or collection commands can charge credits before the user approves the cost, including a command presented as a preview.

Mitigation: Set ARI to ask before every charge with autoconfirm off; use quote for previews, avoid deepdive when a quote-only flow is required, and obtain separate approval for recurring charges.

Risk: A manual collection choice for an existing product preserves its current schedule, which may continue collecting and charging credits.

Mitigation: Check the product's existing schedule before collection and get separate approval before changing or continuing recurring collection.

Risk: The saved ARI API key grants access to the user's account.

Mitigation: Keep the API key private and do not include it in reports or command examples.

## Reference(s):

- [ARI API Reference](artifact/references/reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Charts]

**Output Format:** [Markdown analysis with ranked review themes, product and copy recommendations, star distribution, and review trend charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings reflect the available review sample and collection window; the skill requires an ARI API key for account data and paid operations.]

## Skill Version(s):

1.5.3 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
