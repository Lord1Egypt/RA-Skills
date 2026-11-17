## Description:

Manage a family bookkeeping workflow backed by Feishu Bitable for recording income and expenses, querying summaries, updating ledger entries, and importing WeChat or Alipay bills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzlawliet](https://clawhub.ai/user/hzlawliet)

### License/Terms of Use:

MIT-0

## Use Case:

Household users and agents use this skill to maintain a shared family ledger in Feishu Bitable, including natural-language bookkeeping, monthly and yearly reporting, record updates, and duplicate-aware bill imports. Developers or operators can also run the bundled scripts to normalize statement files, precheck duplicates, export Feishu-importable CSVs, query live records, and write approved rows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Feishu app credentials and ledger identifiers, which can expose household financial records if mishandled.

Mitigation: Use environment variables instead of command-line secrets, grant the Feishu app only the permissions it needs, and clean temporary or output files that may contain financial data.

Risk: Bundled scripts can write new rows or update existing records in the live Feishu Bitable ledger.

Mitigation: Test with dry-run or non-production data first, run the duplicate precheck flow, review generated CSVs and payloads before writing, and require explicit user confirmation for destructive actions.

Risk: Generated CSV and JSON artifacts may contain sensitive transaction details and may be opened in spreadsheet software.

Mitigation: Review generated CSVs before opening or importing them, store outputs only in trusted locations, and delete intermediate files when they are no longer needed.

## Reference(s):

- [Family Bookkeeping Skill Page](https://clawhub.ai/hzlawliet/skills/family-bookkeeping)
- [Family Bookkeeping Category System](references/category-system.md)
- [Family Bookkeeping Feishu Import](references/feishu-import.md)
- [Family Bookkeeping Import Mapping](references/import-mapping.md)
- [Family Bookkeeping Reporting](references/reporting.md)
- [Family Bookkeeping Usage](references/usage.md)
- [Feishu Open API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON summaries, CSV files, and Feishu Bitable record payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce normalized ledger rows, import precheck reports, Feishu-importable CSVs, live ledger summaries, and direct write or update results when configured credentials are available.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
