## Description: <br>
Create a formatted Excel (.xlsx) spreadsheet from provided 2D data, applying styles, colors, alignment, and auto-adjusted column widths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sereinZhi](https://clawhub.ai/user/sereinZhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who need spreadsheet deliverables use this skill to turn structured chat data, tables, or reports into a downloadable Excel workbook with basic styling. It is useful for reports, exports, and formatted tabular data handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper may install openpyxl automatically if it is missing. <br>
Mitigation: Use an approved Python environment and preinstall or review openpyxl before running the helper. <br>
Risk: The skill writes an .xlsx file to the requested filename or path. <br>
Mitigation: Confirm the output filename and path before generation, especially when working in shared directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sereinZhi/generate-excel) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Guidance] <br>
**Output Format:** [XLSX file plus a status dictionary from the helper function] <br>
**Output Parameters:** [2D] <br>
**Other Properties Related to Output:** [Supports simple cell values and styled cell dictionaries for bold text, text color, background color, and horizontal alignment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
