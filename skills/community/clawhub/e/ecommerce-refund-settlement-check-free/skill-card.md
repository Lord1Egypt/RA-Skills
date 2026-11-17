## Description:

电商退货退款与货款结算核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文，本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations users can use this skill during monthly ecommerce settlement review to recalculate refund, commission, payable, net settlement, duplicate-row, blank-field, placeholder, and negative-amount checks from provided table data. It is intended to produce cited findings from the supplied rows and to withhold conclusions when the input is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input tables may contain sensitive ecommerce settlement or accounting data.

Mitigation: Provide only the rows and fields needed for the check, remove unnecessary sensitive data, and follow the security guidance that inspection found local execution without network transmission or persistence.

Risk: The free version does not include every advanced settlement check listed by the artifact.

Mitigation: Treat results as limited to the stated free checks and review withheld or out-of-scope items separately before relying on the reconciliation.

Risk: Insufficient or malformed input can lead to no conclusion rather than a clean result.

Mitigation: Supply table headers and enough recognizable rows, and do not treat an insufficient-input response as confirmation that no issues exist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ecommerce-refund-settlement-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Chinese-language text or JSON with cited table-check findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided table text; insufficient input returns no conclusion.]

## Skill Version(s):

1.0.54 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
