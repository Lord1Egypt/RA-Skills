## Description:

Local-first personal bookkeeping skill for SQLite-backed expense recording, account management, budget tracking, weekly and monthly reports, and CSV import from Alipay and WeChat records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenkang-xie](https://clawhub.ai/user/wenkang-xie)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to keep a local personal cashbook, record expenses from natural language or payment screenshots, manage accounts and budgets, import transaction CSVs, and generate spending reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags the reset command as able to delete an arbitrary user-writable file when CASHBOOK_DB is changed.

Mitigation: Run init.py --force only after verifying the exact database path and keeping a backup of any existing file.

Risk: Imported CSVs and screenshot-derived transaction fields can contain incorrect amounts, dates, or merchants.

Mitigation: Use dry-run or review flows where available and confirm parsed amounts, dates, accounts, and categories before committing records.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wenkang-xie/skills/cashbook)
- [Account management guide](references/account.md)
- [Budget management guide](references/budget.md)
- [Data model](references/schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Text and Markdown responses with inline shell commands; local SQLite database updates and CSV exports when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-first operation with SQLite storage; screenshot and CSV-derived records should be confirmed before writing.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
