## Description:

Generate professional Bloomberg-style Excel workbooks from natural language descriptions. Creates multi-sheet workbooks with dashboards, KPI cards, charts, conditional formatting, and data tables. Use when asked to build Excel files, spreadsheets, dashboards, trackers, or reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synapsefirm-cmd](https://clawhub.ai/user/synapsefirm-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to create formatted Excel workbooks, dashboards, trackers, and business reports from natural-language requests or source data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's default client-delivery workflow uses a shared password for protected workbooks.

Mitigation: Use a unique user-supplied password for each workbook and do not rely on workbook protection as confidentiality control.

Risk: The skill references a fixed local output path, which can lead to misplaced or mishandled business workbooks.

Mitigation: Confirm the output path before generation and apply cleanup and secure delivery practices for HR, finance, sales, or client data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python/openpyxl code and shell commands; generated workbook artifacts are Excel .xlsx files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces multi-sheet workbooks with dashboards, KPI cards, charts, conditional formatting, and data tables.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
