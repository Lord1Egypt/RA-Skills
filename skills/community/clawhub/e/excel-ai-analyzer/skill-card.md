## Description: <br>
Automatically analyzes provided Excel files to generate statistical summaries, anomaly findings, Markdown reports, and data-quality suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oct1st85](https://clawhub.ai/user/oct1st85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, operators, and developers use this skill to inspect a user-provided Excel workbook and receive quick summaries of columns, numeric statistics, missing values, outliers, and suggested follow-up checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet contents may include secrets, regulated personal data, or confidential financial or business information. <br>
Mitigation: Use only in an agent environment approved for the workbook's data classification, and avoid providing sensitive spreadsheets unless the analysis is necessary. <br>
Risk: The release advertises chart generation, but the reviewed version does not implement that feature. <br>
Mitigation: Treat chart output as unsupported in this version and rely on the Markdown report and statistical summaries instead. <br>
Risk: Automated statistics and anomaly flags can be incomplete or misleading without domain review. <br>
Mitigation: Review the generated report against the source workbook before using findings for financial, operational, or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oct1st85/excel-ai-analyzer) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Test report](artifact/test-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with a structured analysis result object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-selected Excel file and summarizes the first worksheet; chart generation is advertised but not implemented in the reviewed artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, SKILL.md, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
