## Description:

预提待摊明细表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

General ledger accountants use this skill before monthly close or expense-period review to check accrued and prepaid expense amortization tables for row-level arithmetic, totals, duplicates, blanks, and missing required columns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accounting-table findings could be mistaken for an audit opinion or accounting judgment.

Mitigation: Treat the output as a deterministic table check and have qualified accounting or audit personnel review judgments, source documents, and policy decisions.

Risk: The free release intentionally omits several disclosed checks.

Mitigation: Review the reported checks_not_run list and perform those checks separately when they matter to close, audit, or tax work.

Risk: Users may run a local Node-based checker on sensitive accounting table text.

Mitigation: Install only trusted releases, review the disclosed local-execution behavior, and keep input handling aligned with the organization's data policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/accrued-expense-amortization-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable terminal text or JSON result containing findings, summary, and executed scope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard-library code; the free version lists checks that are not executed.]

## Skill Version(s):

1.0.22 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
