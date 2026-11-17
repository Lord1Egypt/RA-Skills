## Description:

Track, categorize, and analyze personal expenses from receipt scans, manual entries, CSV imports, budgets, and spending reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eternal0404](https://clawhub.ai/user/eternal0404)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to maintain a local personal or business expense ledger, scan receipts, import bank statement CSVs, track budgets, and generate spending reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local storage of financial transaction, receipt, merchant, and imported bank-statement data can expose sensitive personal finance information on shared systems.

Mitigation: Use a private machine or account and protect the ~/.expense-tracker/ directory according to the sensitivity of the stored records.

Risk: CSV exports can contain sensitive expense records and may be redistributed or opened in tools with unsafe spreadsheet behavior.

Mitigation: Review exported CSVs before opening, sharing, or importing them into other systems.

Risk: Receipt OCR relies on optional local dependencies and may extract or categorize items incorrectly.

Mitigation: Review scanned receipt results and category assignments before relying on reports or budgets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eternal0404/skills/eternal-expense-tracker)
- [Publisher profile](https://clawhub.ai/user/eternal0404)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands; local JSON data and CSV exports when commands are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores transaction, budget, and category data locally under ~/.expense-tracker/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
