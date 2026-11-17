## Description:

Generate beautiful interactive HTML dashboards from CSV/Excel files with smart insights, auto-detected charts, correlations, and statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ratnaditya-j](https://clawhub.ai/user/ratnaditya-j)

### License/Terms of Use:

MIT

## Use Case:

External users, data analysts, and developers use csvglow to turn CSV, TSV, XLS, and XLSX files into local interactive HTML dashboards for visual exploration and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command may open the generated dashboard in a browser by default.

Mitigation: Use the documented --no-open option when browser launch is not desired.

Risk: The external csvglow binary itself was not independently audited by the security review.

Mitigation: Install csvglow from a trusted source and scan or review the binary before deployment.

Risk: Generated self-contained HTML dashboards may embed information from the input spreadsheet.

Mitigation: Use approved local files and handle generated dashboards according to the sensitivity of the source data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ratnaditya-j/skills/csvglow)
- [csvglow homepage](https://github.com/ratnaditya-j/csvglow)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target local CSV, TSV, XLS, or XLSX files and may write a self-contained HTML dashboard.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
