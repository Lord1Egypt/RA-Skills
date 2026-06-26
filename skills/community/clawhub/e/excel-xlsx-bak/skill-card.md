## Description: <br>
Create, inspect, and edit Microsoft Excel workbooks and XLSX files with reliable formulas, dates, types, formatting, recalculation, and template preservation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qmao-hub](https://clawhub.ai/user/qmao-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and automation agents use this skill when spreadsheet deliverables need dependable formulas, formatting, workbook structure, date handling, and type preservation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet edits can silently damage formulas, dates, identifiers, formatting, or workbook structure. <br>
Mitigation: Review formulas, representative cells, data types, formatting, and workbook structure before delivery. <br>
Risk: Formula caches may be stale after edits, and openpyxl preserves formulas without calculating them. <br>
Mitigation: Recalculate in a spreadsheet engine when current values matter and verify that no formula errors remain. <br>
Risk: Macro-enabled workbooks and legacy Excel formats can carry behavior or compatibility constraints outside normal XLSX editing. <br>
Mitigation: Use trusted files, avoid executing macros unless explicitly required, and preserve macro-enabled or legacy formats only with appropriate tooling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qmao-hub/excel-xlsx-bak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with optional code snippets or shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on preserving workbook formulas, formatting, data types, and structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
