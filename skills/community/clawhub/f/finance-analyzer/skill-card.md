## Description: <br>
This skill analyzes financial statements from Excel or CSV files, extracts financial data, and calculates key metrics such as ROE, ROA, gross margin, and net margin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengmengkaiZMK](https://clawhub.ai/user/zhengmengkaiZMK) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and finance teams use this skill to parse local Excel or CSV financial statements and prepare metric tables, calculation components, warnings, and interpretation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted or unexpected spreadsheet inputs could be processed by the local analyzer. <br>
Mitigation: Run the analyzer only on financial files the user intentionally provides for local processing. <br>
Risk: Dependency control matters because the script depends on pandas and openpyxl. <br>
Mitigation: Install in a trusted Python environment and review or pin pandas and openpyxl when dependency governance is required. <br>
Risk: The optional output path can write or overwrite a JSON file. <br>
Mitigation: Choose an output path deliberately and avoid paths that point to important existing files. <br>
Risk: Financial metrics can be incomplete or misleading when source rows are missing, mislabeled, or use unexpected units. <br>
Mitigation: Review formulas, component values, warnings, and units before presenting financial conclusions. <br>


## Reference(s): <br>
- [Financial Statements Guide](references/financial_statements_guide.md) <br>
- [finance-analyzer on ClawHub](https://clawhub.ai/zhengmengkaiZMK/finance-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summary with metric tables; the bundled script can emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file analysis; optional JSON output may write or overwrite the selected output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
