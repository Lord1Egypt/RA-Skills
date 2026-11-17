## Description:

Provides guidance and helper tooling for creating, editing, analyzing, formatting, visualizing, and recalculating spreadsheet files such as .xlsx, .xlsm, .csv, and .tsv.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and agents use this skill to build, inspect, modify, format, analyze, and recalculate spreadsheet workbooks while preserving formulas and existing workbook conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recalculation workflow can persistently install or overwrite a LibreOffice macro in the user's profile.

Mitigation: Run the skill in a disposable user profile or sandbox, review the macro behavior before use, and avoid using it on a primary LibreOffice profile.

Risk: Spreadsheet creation, editing, and recalculation can change workbook structure, formulas, and calculated values.

Mitigation: Keep backups of important spreadsheets and review formula error reports before relying on the resulting workbook.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; generated spreadsheet artifacts may be XLSX, XLSM, CSV, or TSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The recalculation helper returns JSON error reports and may modify local spreadsheet files during formula recalculation.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
