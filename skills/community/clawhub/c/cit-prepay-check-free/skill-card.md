## Description:

季度预缴所得税计算表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting staff use this skill to check Chinese quarterly corporate income tax prepayment tables before reconciliation or filing. It reruns arithmetic checks, total-row tie-outs, duplicate-period detection, and blank-field checks while citing the source rows.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The checker can identify table arithmetic and completeness issues, but it is not tax or legal advice and does not replace official filing review.

Mitigation: Use it only as a local pre-check for relevant exported table text, and have qualified reviewers confirm tax treatment and filing decisions.

Risk: The free version intentionally omits some checks that are listed as not included.

Mitigation: Review the disclosed checks that were run and the checks not run before relying on the result.

Risk: Incomplete or malformed input can produce unsupported conclusions if treated casually.

Mitigation: Provide the table header and relevant rows; when the skill reports insufficient input, do not treat that as a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/cit-prepay-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON findings from a local Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; insufficient input returns missing requirements instead of a no-issue conclusion.]

## Skill Version(s):

1.0.52 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
