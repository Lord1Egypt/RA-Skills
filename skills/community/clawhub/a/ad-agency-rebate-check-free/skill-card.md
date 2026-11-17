## Description:

广告代理返点与框架返点核对（免费版）核对广告代理返点与框架返点表中的逐行复算、合计勾稽、重复行、空缺和负数问题，并让每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashiering, and reconciliation users can use this skill during monthly or quarterly close to check ad agency rebate tables for arithmetic, totals, duplicate rows, blank placeholders, and negative amounts. It is intended for local review of user-provided table text and does not decide contract terms, tax treatment, or whether source platform data is true.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free checker as a complete rebate audit even though some checks are explicitly omitted.

Mitigation: Review the reported executed and omitted checks before relying on the result, and use additional review for withheld checks.

Risk: The checker is Chinese-language and focused on local rebate reconciliation table conventions.

Mitigation: Install and use it only when reviewers can understand the Chinese output and the table format it expects.

Risk: The skill checks table arithmetic and consistency but does not decide contract terms, tax treatment, or source data truth.

Mitigation: Validate business, contract, and tax questions against the underlying agreements, finance policy, and qualified reviewers.

Risk: Insufficient or malformed input can prevent the checker from reaching a conclusion.

Mitigation: Provide the rebate table with required headers and treat insufficient-input responses as no conclusion, not as a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ad-agency-rebate-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; the bundled runner can emit structured JSON findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a local Node.js checker over user-provided table text; the free version reports its executed and omitted checks.]

## Skill Version(s):

1.0.45 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
