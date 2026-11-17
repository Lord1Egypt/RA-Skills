## Description:

Bilingual expense tracking and bookkeeping skill for recording spending, generating reports, exporting ledgers, and creating expense charts in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swiftuis](https://clawhub.ai/user/swiftuis)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal finance assistants use this skill to record daily expenses from natural-language Chinese or English messages, categorize transactions, summarize spending, export ledger data, and generate charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports and exports can contain sensitive financial data.

Mitigation: Review outputs before sharing and keep the ledger, export, and chart directories private unless the user explicitly chooses to share them.

Risk: The chart renderer may capture the desktop instead of only the report when image rendering fails.

Mitigation: Fix or disable chart rendering before use; prefer non-screenshot report formats until the renderer is reviewed.

## Reference(s):

- [Expense Categories](references/categories.md)
- [ClawHub skill page](https://clawhub.ai/swiftuis/skills/accounting-assistant)
- [Publisher profile](https://clawhub.ai/user/swiftuis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown responses with JSON command results, CSV or JSON exports, and HTML or PNG chart files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores ledger data, exports, and chart artifacts under ~/.qclaw/workspace/expense-ledger/.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
