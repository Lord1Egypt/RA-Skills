## Description: <br>
Diagnose and repair Microsoft Excel XLSX workbook issues involving formulas, named ranges, Power Query refreshes, pivot tables, VBA or macro preservation, workbook corruption, and repeatable data cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, finance and operations teams, spreadsheet-heavy small businesses, and developers use this skill to diagnose Excel workbook defects and plan safe repairs while preserving formulas, structure, formatting, macros, and business logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Excel workbooks can contain sensitive business data. <br>
Mitigation: Use the skill on workbook copies, review proposed edits before applying them, and invoke it explicitly for workbook-specific repair or automation tasks. <br>
Risk: Some workbook structures, such as pivot caches, Power Query metadata, and macros, may not be safely rebuilt by Python libraries alone. <br>
Mitigation: Preserve package parts where possible and note when desktop Excel, Power Query, or Power BI tooling is required for recalculation or refresh. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kyro-ma/excel-xlsx-formula-cleanup-helper-180322) <br>
- [Requirement Plan](references/requirement-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with code blocks and validation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workbook diagnoses, safe repair plans, automation code, and validation steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
