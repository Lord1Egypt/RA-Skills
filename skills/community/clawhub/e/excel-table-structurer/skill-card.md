## Description:

Structures hierarchical Excel .xlsx workbooks by filling parent values downward, showing group-level headers on the first row, filling selected group values for filtering, and applying workbook formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legionspace-hackathon](https://clawhub.ai/user/legionspace-hackathon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to restructure hierarchical Excel workbooks such as test cases, project task lists, and ledger-style tables into cleaner, filterable .xlsx outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fill values into blank cells and change workbook formatting while restructuring a spreadsheet.

Mitigation: Run it on a copy or write to a separate output path, then confirm detected column roles before returning or relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/legionspace-hackathon/skills/excel-table-structurer)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON configuration, shell commands, generated .xlsx workbook files, and JSON run summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The restructuring script writes a separate workbook and reports total row and group counts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
