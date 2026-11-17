## Description:

按主 ASIN 与已授权竞品的商品字段和评论证据整理可比特性矩阵，并标注资料缺口与体验差异；仅用于静态特性对照。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and product analysts use this skill to compare a main ASIN with authorized competitors using available product fields and review evidence, and to identify information gaps and reported experience differences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes broader account controls, and commands described as quote-only may trigger paid analysis.

Mitigation: Use a release that enforces comparison-only scope and quote-only behavior; set the account to ask before each charge and approve recurring collection separately. Omitting --confirm alone is insufficient.

## Reference(s):

- [Operation workflow](artifact/references/operation-workflow.md)
- [ARI CLI and API reference](artifact/references/reference.md)
- [ARI product operations](https://ari.funewa.com/zh/operations)
- [ClawHub skill page](https://clawhub.ai/funewa/skills/competitor-features)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown comparison matrix with evidence notes and information gaps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static comparison based on available product fields and review evidence; does not establish sales, inventory, advertising, order, or actual return-rate performance.]

## Skill Version(s):

1.5.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
