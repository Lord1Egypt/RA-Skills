## Description:

Helps agents provide Python/openpyxl guidance and runnable recipes to create, read, filter, append, merge, and validate .xlsx workbooks without breaking formulas, dates, or formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[po-et](https://clawhub.ai/user/po-et)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill when an agent needs to draft or adapt local Python scripts for Excel workbook automation, including batch creation, filtering, appending, formula handling, date normalization, merged-cell cleanup, and multi-workbook consolidation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated spreadsheet scripts can modify formulas, dates, formatting, or workbook objects in ways the user did not intend.

Mitigation: Run scripts only on backup copies or newly saved output files, open the result in Excel or WPS, and compare sample rows against the source workbook before delivery.

Risk: Spreadsheets may contain personal, financial, or business-sensitive data.

Mitigation: Keep processing local, redact samples, screenshots, and logs, and avoid exposing identifiers such as ID numbers or phone numbers in shared outputs.

Risk: openpyxl does not calculate formulas and may not preserve every workbook feature such as shapes, charts, macros, or controls.

Mitigation: Warn users when formula values require opening and saving in Excel, use keep_vba for .xlsm when needed, and avoid overwriting source workbooks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/po-et/skills/excel-processing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scripts are intended for local execution with openpyxl and should include a run summary, formula reminders, and spot-check guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
