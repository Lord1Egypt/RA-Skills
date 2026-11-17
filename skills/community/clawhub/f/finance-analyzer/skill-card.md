## Description:

This skill analyzes financial statements from Excel or CSV files, extracts income statement, balance sheet, and cash flow data, and calculates metrics including ROE, ROA, gross margin, and net margin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengmengkaizmk](https://clawhub.ai/user/zhengmengkaizmk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to parse financial statement spreadsheets, calculate core profitability and balance-sheet metrics, and present formulas, components, warnings, and interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and local script execution can affect the user's Python environment.

Mitigation: Use a dedicated virtual environment and avoid privileged or system-wide pip installs.

Risk: Financial spreadsheets and optional JSON exports may contain sensitive extracted financial data, and the output path can overwrite an existing file.

Mitigation: Review the spreadsheet before processing, choose output paths deliberately, and avoid persisting sensitive results unless needed.

Risk: Ambiguous sheet names, missing line items, or unit differences can produce incomplete or misleading metrics.

Mitigation: Review warnings, formulas, components, and units before relying on the analysis; specify a sheet or inspect the file manually when parsing is uncertain.

## Reference(s):

- [Financial Statements Guide](references/financial_statements_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save parsed financial data and calculated metrics to a user-selected JSON file.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
