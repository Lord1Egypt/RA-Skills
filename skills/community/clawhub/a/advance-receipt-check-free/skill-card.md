## Description:

预收账款与收入确认台账逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations users use this skill during monthly close, reconciliation, or inventory-style ledger review to check advance receipt and revenue recognition tables for arithmetic consistency, total-row agreement, duplicate customers, missing fields, and negative balances. It is a local checker for the listed free checks only, not a full accounting or legal revenue-recognition review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial ledger inputs can contain sensitive business data.

Mitigation: Use the skill only in environments where local file handling of that data is acceptable, and avoid providing ledgers unless the user is comfortable with a local checker processing them.

Risk: The free release performs only the listed reconciliation checks and does not provide full accounting, tax, legal, or revenue-recognition judgment.

Mitigation: Use outputs as deterministic ledger-check results for review, and route revenue-recognition timing, contract interpretation, tax, or accounting-standard questions to qualified reviewers.

Risk: The interface and output are primarily Chinese, which may reduce review quality for teams that do not read Chinese.

Mitigation: Have a Chinese-reading reviewer validate inputs, outputs, and any business decisions derived from the findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/advance-receipt-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON ledger-check results with cited row-level findings, executed and withheld check lists, and insufficient-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; accepts a JSON or plain-text ledger input file and includes explicit out-of-scope checks.]

## Skill Version(s):

1.0.62 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
