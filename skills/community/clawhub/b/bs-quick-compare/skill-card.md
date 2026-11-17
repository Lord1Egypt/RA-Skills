## Description:

Period-over-period variance analysis on the Balance Sheet pulled from QuickBooks Online, producing a 4-tab Excel workbook with Summary, Detail, Flags, and CDC Log sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting operators use this skill to compare QuickBooks Online balance sheets across periods, investigate material changes in assets, liabilities, and equity, and prepare month-end, YTD, loan, or investor reporting support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QuickBooks Online credentials and client financial data may be exposed if the skill is installed or run in an inappropriate environment.

Mitigation: Use the skill only in environments authorized for the reporting task and keep QBO credentials out of dependency installation contexts.

Risk: The disclosed local cache can contain sensitive balance sheet values.

Mitigation: Protect the `.cache/bs-quick-compare/{slug}.json` file with the same access controls as financial reports and clear it when retention is not needed.

Risk: Dependency installation can introduce ordinary supply-chain risk.

Mitigation: Use a pinned and reviewed `openpyxl` dependency before running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/bs-quick-compare)
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to run a QuickBooks Online balance sheet comparison pipeline that produces an Excel workbook.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
