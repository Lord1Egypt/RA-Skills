## Description:

Excel2Insights helps agents inspect structured spreadsheet data, run statistical analysis and data quality checks, generate charts, and produce insight reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users can use this skill to quickly profile CSV, XLSX, XLS, or TSV datasets, identify data quality issues, create visualizations, and generate structured Markdown or HTML reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dataset-controlled column names can affect generated chart filenames and report HTML.

Mitigation: Use the skill only with trusted datasets until filenames are sanitized and report HTML is escaped.

Risk: Generated reports and previews can expose sensitive source data.

Mitigation: Review output locations and report contents before sharing or publishing generated files.

## Reference(s):

- [Demo walkthrough](references/demo-walkthrough.md)
- [Demo report preview](references/demo-report-preview.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or HTML reports, JSON analysis summaries, PNG chart files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs may include source dataset values, chart image files, and report files written to a local output directory.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
