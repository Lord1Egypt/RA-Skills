## Description:

Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, visualization, and formula recalculation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and spreadsheet-focused agents use this skill to create, modify, analyze, visualize, and recalculate spreadsheets while preserving formulas and workbook formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The formula recalculation script writes a persistent LibreOffice macro into the user's LibreOffice profile and may overwrite existing macro content.

Mitigation: Review before installing, run on copies of spreadsheets, avoid untrusted workbooks, and prefer changing the script to use a temporary LibreOffice profile before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/exceltable-in-ppt-xlsx)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and shell command snippets; spreadsheet files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formula recalculation can return JSON diagnostics with formula counts and Excel error locations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
