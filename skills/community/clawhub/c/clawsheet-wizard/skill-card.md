## Description:

Create, inspect and edit Excel/XLSX files with reliable formulas, data quality checks and template diff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with Excel/XLSX files, inspect formulas, generate data quality reports, and compare edited workbooks against templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local spreadsheet scripts may process sensitive workbook contents.

Mitigation: Run the scripts only in a trusted local environment and review generated reports before sharing or acting on them.

Risk: The advertised auto-fix workflow should not be treated as verified workbook repair.

Mitigation: Use formula checking as inspection guidance, prefer new output filenames, and manually verify formulas and workbook changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/clawsheet-wizard)
- [Publisher profile](https://clawhub.ai/user/northcap-group)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline bash commands and local text or Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write report files or new spreadsheet filenames when users run the bundled scripts.]

## Skill Version(s):

1.0.10 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
