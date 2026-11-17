## Description:

企业所得税纳税调整核对（免费版）在本地复算企业所得税纳税调整表的核心勾稽关系，检测重复、空白、占位符和调增/调减负数，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and tax staff use this skill before annual enterprise income tax filing to check whether adjustment-table arithmetic, totals, duplicate rows, blanks, placeholders, and negative adjustment amounts are internally consistent. It is a free local subset and does not replace full tax-law or limit-rule review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: A clean result can be mistaken for full tax compliance advice, even though the free release does not check several tax-limit and legal-validity issues.

Mitigation: Review the listed checks not run and manually confirm withheld limit-rule, tax-rate, and legal-validity items against applicable tax requirements.

Risk: Incomplete or malformed table input can prevent meaningful checking.

Mitigation: Provide the enterprise income tax adjustment table with headers and treat an insufficient-input result as no conclusion rather than as no issues found.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/cit-adjustment-check-free)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON report from a local Node.js checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; insufficient input returns missing-material guidance instead of a clean result.]

## Skill Version(s):

1.0.61 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
