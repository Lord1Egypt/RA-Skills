## Description:

Data Chart Tool helps agents turn CSV, JSON, or Excel data into configurable charts such as bar, line, pie, area, and licensed scatter plots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and report authors use this skill to create chart files or previews from tabular data for finance, sales, research, and personal analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python import path handling may load attacker-controlled local code.

Mitigation: Use an isolated Python environment, avoid shared writable directories, and fix the import-path issue before multi-user or sensitive-data use.

Risk: The paid-feature license check has weak secret handling and authorization properties.

Mitigation: Do not persist SKILL_LICENSE_SECRET in shell startup files, protect license material, and treat the paid-feature gate as limited authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopiabenben/skills/data-chart-tool)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [Chart files in PNG, JPEG, PDF, or SVG with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports preview mode and configurable chart type, columns, labels, colors, style, figure size, DPI, grid, legend, and license file path.]

## Skill Version(s):

1.1.0-premium (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
