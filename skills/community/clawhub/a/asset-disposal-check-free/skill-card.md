## Description:

固定资产处置表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。触发词包括 固定资产处置损益核对、固定资产处置表对不上。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill during fixed-asset disposal close, reconciliation, or review to check disposal tables for internal arithmetic consistency, totals, duplicate assets, and missing required values. It is a free local checker and does not replace tax, audit, impairment, depreciation-policy, or full paid-version review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free checker as a complete audit, tax, impairment, depreciation-policy, or full fixed-asset review.

Mitigation: Present it as an internal consistency checker only, and require qualified accounting review for tax, audit, impairment, depreciation policy, or other out-of-scope judgments.

Risk: The free version omits several checks listed by the artifact, including negative income or expense checks, negative net value checks, zero or negative original cost checks, net-outflow disposal checks, and no-income disposal gain checks.

Mitigation: Review the omitted-check list in each output and run additional controls or a fuller review when those conditions matter.

Risk: Incomplete or malformed input can prevent valid conclusions.

Mitigation: Provide the disposal table with headers for asset name, original cost, accumulated depreciation, book net value, disposal income, cleanup expense, and disposal gain or loss; treat insufficient-input results as no conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/asset-disposal-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, analysis, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON containing executed checks, findings, scope, omitted checks, and disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard libraries; expects a JSON file or pasted fixed-asset disposal table text with required headers.]

## Skill Version(s):

1.0.55 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
