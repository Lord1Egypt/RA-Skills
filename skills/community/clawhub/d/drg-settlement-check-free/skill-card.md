## Description:

医保结算清单与DRG入组核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and hospital reimbursement staff use this skill during monthly settlement and reconciliation to check DRG settlement tables for arithmetic consistency, total-row agreement, duplicate rows, blanks, placeholders, and negative amounts. It is intended as a local checking aid and not as a substitute for hospital coding,医保办, or local policy review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive medical and payment data from user-provided files.

Mitigation: Run it only in an approved local environment, review inputs before use, and handle source files according to the organization's privacy and data-retention rules.

Risk: The output can be mistaken for a complete reimbursement, coding, or local policy decision.

Mitigation: Treat findings as reconciliation support and have hospital coding,医保办, or local policy reviewers validate any operational decision.

Risk: The free edition intentionally omits checks such as missing DRG group code, weight-range alerts, and high/low multiple case handling.

Mitigation: Review the reported omitted checks and perform manual or separate paid/full-scope review when those checks are needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/drg-settlement-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON containing executed checks, findings, scope, omitted checks, and source-line evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library behavior; does not require registration, an API key, or network access, and refuses to make conclusions when required input is missing.]

## Skill Version(s):

1.0.48 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
