## Description: <br>
Create, inspect, and edit Microsoft Excel workbooks and XLSX files with reliable formulas, dates, types, formatting, recalculation, and template preservation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuwenxi416488212-ship-it](https://clawhub.ai/user/qiuwenxi416488212-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when working with Excel or spreadsheet artifacts that need reliable reading, editing, conversion, formulas, dates, formatting, workbook structure, or template preservation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet operations can overwrite or delete workbook content during sheet deletion, merging, conversion, or save operations. <br>
Mitigation: Work on backups or save to a new output path before destructive edits, merging workbooks, or converting formats. <br>
Risk: Processing spreadsheets from untrusted sources can expose the agent environment to unsafe workbook content or dependency-level vulnerabilities. <br>
Mitigation: Install in an isolated Python environment and pin current patched versions of openpyxl and pandas where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiuwenxi416488212-ship-it/excel-toolkit) <br>
- [Skill homepage](https://clawic.com/skills/excel-xlsx) <br>
- [README.md](artifact/README.md) <br>
- [README_CN.md](artifact/README_CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; generated work may include Excel workbooks, CSV, or TSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local spreadsheet files using openpyxl and pandas.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
