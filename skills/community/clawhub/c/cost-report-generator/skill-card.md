## Description: <br>
Generates formatted Excel cost analysis reports from project expense spreadsheets, grouped by customer category with yearly totals, monthly detail, and monthly averages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard052317](https://clawhub.ai/user/richard052317) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, finance teams, and operations analysts use this skill to convert project-cost Excel workbooks into customer-segmented cost analysis reports for 2025 and 2026. It is intended for local processing of spreadsheets that match the documented cost-column and customer-category structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Source spreadsheets and generated reports can contain sensitive business cost data. <br>
Mitigation: Process files locally, choose an explicit output directory with appropriate access controls, and review the report before sharing. <br>
Risk: Reports may omit or misclassify data when input spreadsheets do not match the documented columns or supported customer categories. <br>
Mitigation: Confirm the source workbook structure and customer category values before relying on the generated financial analysis. <br>


## Reference(s): <br>
- [Cost Report Generator on ClawHub](https://clawhub.ai/richard052317/cost-report-generator) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, code, guidance] <br>
**Output Format:** [Excel workbook (.xlsx) with console status messages and optional Python return path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped local Excel reports with separate 2025 and 2026 cost-analysis worksheets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
