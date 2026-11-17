## Description:

基于 Amazon 商品字段和评论反馈，识别商品描述的信息缺口并给出改写建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and operators use the skill to review product details and customer feedback, find gaps in a product description, and draft clearer wording. The release also exposes broader review analysis and monitoring functions that may incur one-time or recurring charges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This release includes paid analysis and recurring monitoring alongside description guidance, and its approval rules are inconsistent.

Mitigation: Use a package that enforces the advertised scope. Set credit spending to ask every time, choose manual collection for one-time work, and approve recurring charges separately.

## Reference(s):

- [Operation workflow](references/operation-workflow.md)
- [ARI API reference](references/reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Concise text or Markdown with evidence-based product-description observations and rewrite suggestions; review summaries when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ARI API key. Does not automatically modify or publish Amazon listing content.]

## Skill Version(s):

1.5.3 (source: CHANGELOG, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
