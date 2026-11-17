## Description:

结合 Amazon 商品详情和评论证据，诊断买家决策障碍并提出页面转化表达建议；仅用于证据驱动的转化表达诊断，不用于转化率预测、广告投放或自动发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and ecommerce operators use the skill to identify buyer decision barriers from product details and review evidence, then develop evidence-based listing copy suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conflicting instructions may result in credit spending or recurring data collection without clear approval.

Mitigation: Use a corrected package that consistently enforces the advertised workflow. Set ARI to ask before every charge, authorize one-time collection, and approve recurring collection separately.

Risk: Authorization stores an ARI key locally, and generated reports are archived with the service.

Mitigation: Before use, account for local key storage and service-side report archiving when deciding whether to authorize the skill.

## Reference(s):

- [Operation workflow](references/operation-workflow.md)
- [ARI API reference](references/reference.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown report with evidence-based listing copy suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in available product and review evidence; does not predict conversion rates or publish page changes.]

## Skill Version(s):

1.5.3 (source: server-resolved release evidence, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
