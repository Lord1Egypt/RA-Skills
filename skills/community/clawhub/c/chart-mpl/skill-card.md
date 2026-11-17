## Description:

Generate PNG/SVG charts (line, bar, hbar, pie, stacked, scatter, area) from CSV data using matplotlib.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xvespertine](https://clawhub.ai/user/0xvespertine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent workflows use this skill to turn CSV data into BI-ready PNG or SVG chart images for visualization, reporting, and multi-series comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions install an unpinned matplotlib dependency into a reusable virtual environment.

Mitigation: Install from a trusted Python package index and pin matplotlib and dependencies when reproducibility or supply-chain control matters.

Risk: CSV contents and generated chart paths may reveal sensitive source data.

Mitigation: Run the script only on intended CSV files and review generated image paths before sharing outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xvespertine/skills/chart-mpl)

## Skill Output:

**Output Type(s):** [shell commands, code, files, guidance]

**Output Format:** [Markdown with inline bash commands and generated PNG or SVG chart file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated chart files are written to a requested output path or the default workspace exports/images directory.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
