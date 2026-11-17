## Description:

Generates gene-expression bubble plots from TSV or CSV expression matrices for cell type by cancer type comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fmaxy](https://clawhub.ai/user/fmaxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and bioinformatics users use this skill to inspect gene-expression data and generate dot plots showing average expression and positive-cell fraction across cell types and cancer types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plotting script may write output files outside the selected output folder.

Mitigation: Run the skill in a disposable workspace and choose an output directory where accidental overwrites cannot damage important files.

Risk: The setup guidance suggests modifying the system Python environment.

Mitigation: Install pandas and matplotlib in a virtual environment before running the script.

Risk: Untrusted input files can affect generated filenames and output behavior.

Mitigation: Use trusted input files or sanitize filenames and selected gene names before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fmaxy/skills/bubble-plot)
- [Publisher profile](https://clawhub.ai/user/fmaxy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated PNG/PDF plot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can create one PNG and one PDF for each selected gene and tissue grouping.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
