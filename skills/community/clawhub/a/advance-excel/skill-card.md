## Description:

Use this skill any time a spreadsheet file is the primary input or output, including opening, reading, editing, fixing, creating, cleaning, restructuring, or converting .xlsx, .xlsm, .csv, and .tsv files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[berkgungor](https://clawhub.ai/user/berkgungor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and spreadsheet-focused agents use this skill to inspect, analyze, edit, create, format, recalculate, and validate spreadsheet workbooks and tabular data files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run local LibreOffice operations on spreadsheet files.

Mitigation: Use it only in workspaces where local LibreOffice execution on those files is acceptable.

Risk: Workbook edits and recalculation can change files in place.

Mitigation: Keep backups of important workbooks and prefer saving edits to new output files.

Risk: The bundled LibreOffice helper can support broader document conversion behavior than spreadsheet workflows require.

Mitigation: Avoid using the generic soffice helper for non-spreadsheet conversions unless that broader capability is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/berkgungor/skills/advance-excel)
- [Publisher profile](https://clawhub.ai/user/berkgungor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus generated or edited spreadsheet files when used by an agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON inspection or formula-recalculation results through bundled helper scripts.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
