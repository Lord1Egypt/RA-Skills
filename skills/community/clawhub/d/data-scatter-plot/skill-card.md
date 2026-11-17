## Description:

Reads CSV or Excel data and generates scatter plots from Result values with optional Min/Max Limit reference lines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewhb](https://clawhub.ai/user/matthewhb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to parse local CSV or Excel test data and produce scatter-plot image files for each item and column combination, including Min/Max Limit context when those rows are present.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads selected CSV or Excel files and writes generated plot images to local storage.

Mitigation: Run it only in an environment where the selected input files and configured output directory are approved for that data.

Risk: Runtime dependencies are declared with lower-bound versions rather than pinned versions.

Mitigation: Pin or lock pandas, matplotlib, openpyxl, and xlrd before production use.

Risk: Plots depend on expected spreadsheet rows such as Result, Min Limit, and Max Limit being present and correctly formatted.

Mitigation: Review generated plots against the source spreadsheet before using them for operational or quality decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matthewhb/skills/data-scatter-plot)

## Skill Output:

**Output Type(s):** [files, shell commands, code, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; generated chart files are PNG by default.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local scatter-plot image files in the configured output directory; default output format is png.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
