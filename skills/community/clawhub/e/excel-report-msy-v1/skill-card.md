## Description: <br>
Create formatted Excel report workbooks from CSV files using openpyxl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ms-yun](https://clawhub.ai/user/ms-yun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to convert user-selected CSV files into polished Excel .xlsx reports with formatted headers, numeric totals, filters, frozen headers, autosized columns, and a simple bar chart. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report script can create directories and overwrite the target workbook path selected by the user or agent. <br>
Mitigation: Choose an explicit output path, avoid pointing at existing workbooks unless replacement is intended, and verify the generated file before returning it. <br>
Risk: The skill requires the openpyxl Python dependency in the active environment. <br>
Mitigation: Install openpyxl only in environments where adding that dependency is acceptable, or use an environment that already provides it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ms-yun/excel-report-msy-v1) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [Markdown with generated .xlsx file paths and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Excel workbook files from CSV input; important outputs should be verified before delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
