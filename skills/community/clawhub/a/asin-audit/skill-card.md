## Description:

Amazon ASIN 运营体检 Skill：综合商品详情与评论证据，输出问题、证据与运营优先级。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and operators use this skill to assess one ASIN using product detail and review evidence, then prioritize operational improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a scope mismatch: this single-product audit includes broader account controls, automatic spending, and recurring monitoring with conflicting approval rules.

Mitigation: Review before installation, keep use within the intended single-ASIN audit, require approval before each charge, use manual collection for one-time work, and check existing recurring schedules separately.

## Reference(s):

- [ARI API reference](references/reference.md)
- [Operations workflow](references/operation-workflow.md)
- [ARI service](https://ari.funewa.com)
- [ClawHub release page](https://clawhub.ai/funewa/skills/asin-audit)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown audit with findings, supporting evidence, and prioritized operational recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ground conclusions in available product and review evidence; identify data gaps where relevant.]

## Skill Version(s):

1.5.3 (source: CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
