## Description: <br>
Automatically analyze CSV or Excel files and generate professional data analysis reports with charts, summaries, and insights as Word (.docx) or PDF output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suntianchong](https://clawhub.ai/user/suntianchong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, analysts, and developers use this skill to turn uploaded CSV, TSV, or Excel files into structured business or operations reports with profiling, charts, findings, and recommendations. It is suited for sales, operations, marketing, finance, and general tabular-data reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may modify the host Python environment while installing reporting dependencies. <br>
Mitigation: Use a virtual environment or container, and approve host-level package installation only when it is expected for the reporting task. <br>
Risk: The skill processes selected local spreadsheets that may contain sensitive business or personal data. <br>
Mitigation: Use only intended input files, review outputs before sharing, and avoid uploading data that should not be processed by the agent. <br>
Risk: Broad activation for spreadsheet analysis can make the skill unnecessary for simple summaries or charts. <br>
Mitigation: Confirm the user needs a full Word or PDF report before applying the complete workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suntianchong/data-report-generator) <br>
- [Publisher profile](https://clawhub.ai/user/suntianchong) <br>
- [Chart Styling Reference](references/chart-styling.md) <br>
- [General Analysis Reference](references/general.md) <br>
- [PDF Generation Fallback](references/pdf-fallback.md) <br>
- [Sales & Performance Analysis Reference](references/sales-analysis.md) <br>
- [Segmentation Analysis Reference](references/segmentation.md) <br>
- [Statistical Analysis Reference](references/statistical.md) <br>
- [Time Series Analysis Reference](references/time-series.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples for generating DOCX or PDF report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill typically produces report-generation steps, charts, summary text, recommendations, and final Word or PDF report files through the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
