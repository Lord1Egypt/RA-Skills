## Description:

Queries and downloads Dongfang Caifu (Eastmoney) research reports across industry, stock, strategy, macro, and brokerage morning report categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manymore13](https://clawhub.ai/user/manymore13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users can use this skill to find Eastmoney research report categories, query recent reports by industry, stock, or report type, download PDFs, and export report metadata for spreadsheet review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact asks users to install and run mutable remote code that was not included in the reviewed package.

Mitigation: Review the remote repository and dependencies before installing, prefer a pinned commit or trusted release, and run the tool in a virtual environment with limited filesystem access.

Risk: Bulk downloads can create significant local disk usage and place load on the external report service.

Mitigation: Use bounded page sizes and output directories, avoid broad bulk downloads by default, and monitor downloaded file volume.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manymore13/skills/eastmoney-reports)
- [Publisher profile](https://clawhub.ai/user/manymore13)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands, structured report summaries, and downloaded PDF or CSV files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local report downloads and CSV exports depending on selected command or MCP tool.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
