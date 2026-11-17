## Description:

Converts one or more CSV files into formatted Excel workbooks, with encoding detection for Chinese text and optional multi-sheet output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuanguan2020](https://clawhub.ai/user/xuanguan2020)

### License/Terms of Use:


## Use Case:

Developers, analysts, and business users use this skill to convert individual CSV files or combine multiple CSV files into formatted Excel workbooks for reporting and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV files from untrusted sources may contain formula-like cells that remain active when the generated workbook is opened.

Mitigation: Review or sanitize untrusted CSV content before conversion and inspect the workbook before sharing it.

Risk: The converter depends on the local openpyxl package.

Mitigation: Install it in a virtual environment and pin the dependency version when reproducibility matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuanguan2020/skills/csvtoexcel)
- [Publisher profile](https://clawhub.ai/user/xuanguan2020)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown with inline bash code blocks and generated Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces .xlsx workbooks from selected local CSV files; generated spreadsheets may preserve formula-like cells from source CSV data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
