## Description: <br>
Analyze the weekly attendance records of employees at Zhuihui Branch and generate an attendance report in docx format with an xlsx detailed supplement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang2y](https://clawhub.ai/user/wang2y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations teams use this skill to analyze Zhuihui Branch attendance spreadsheets, apply branch-specific attendance rules, and prepare weekly attendance summaries with detailed supporting data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated JSON, DOCX, and XLSX outputs can contain sensitive employee attendance details. <br>
Mitigation: Install and run only when authorized to process the records, choose approved private output paths, review the documented exclusion and department-mapping rules, and delete generated reports when no longer needed. <br>
Risk: Branch schedules, holiday handling, and employee exclusion rules can change and may affect report accuracy. <br>
Mitigation: Review the documented attendance rules and mappings against the current reporting period before relying on generated summaries. <br>


## Reference(s): <br>
- [Special Attendance Analysis Rules](references/special-attendance-analysis-rules.md) <br>
- [Example: Weekly Attendance Analysis](examples/example-usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wang2y/analyzing-attendance-record-zhzh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance and generated attendance report artifacts such as DOCX and XLSX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process employee attendance records and produce sensitive report files that require approved private storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
