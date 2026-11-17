## Description:

预提费用台账逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users run this skill during month-end close, reconciliation, or inventory checks to verify accrual-expense ledger arithmetic, totals, duplicates, blanks, and free-tier scope. It reports row-level findings and withholds conclusions when required ledger material is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Node script against ledger text supplied by the user.

Mitigation: Run it only in an environment approved for the ledger data being checked and review the local-script behavior before deployment.

Risk: Findings cite row numbers and calculated values rather than preserving full original evidence excerpts.

Mitigation: Keep the source ledger available and reconcile reported rows and calculations against the original material before acting on results.

Risk: The free version deliberately omits several accrual-expense checks.

Mitigation: Review the reported checks_not_run list and do not treat the free-tier output as coverage for withheld checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/accrual-expense-check-free)
- [Skill instructions](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis]

**Output Format:** [Plain text or JSON report with row-level findings, executed checks, checks not run, summary counts, and scope notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided accrual ledger text; returns insufficient-input status instead of conclusions when required material is missing.]

## Skill Version(s):

1.0.62 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
