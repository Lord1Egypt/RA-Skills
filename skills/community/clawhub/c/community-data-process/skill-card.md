## Description: <br>
Automates community group spreadsheet export processing by cleaning customer group data, auditing key metrics, appending filtered records to a BI upload workbook, and verifying the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuhui435](https://clawhub.ai/user/yuhui435) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations or data analysts use this skill to process BAIC community group Excel exports from Downloads, retain selected group-label rows, validate numeric metrics, and append the cleaned data to the BI community data upload workbook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads matching customer and BI Excel files from the local Downloads folder. <br>
Mitigation: Keep only the intended source workbook in Downloads before execution and review the generated BI upload workbook before using it. <br>
Risk: The merge workflow is append-only and can duplicate records when rerun against the same source data. <br>
Mitigation: Run the merge once per intended export, or inspect and remove duplicate appended rows before uploading the BI workbook. <br>
Risk: The workflow uses file creation time as the statistics date, so an incorrect source file can produce records for the wrong date. <br>
Mitigation: Confirm the latest matching customer group export in Downloads is the intended file before running the process. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuhui435/community-data-process) <br>
- [Publisher profile](https://clawhub.ai/user/yuhui435) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Console status text plus generated Excel workbooks and a text result report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates cleaned and merged BI upload workbooks in the local Downloads folder; normal operation depends on pandas and openpyxl.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
