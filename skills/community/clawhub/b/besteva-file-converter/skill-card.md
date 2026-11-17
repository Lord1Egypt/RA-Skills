## Description:

This skill helps agents convert documents, images, and spreadsheets between PDF, Word, common image formats, Excel, and CSV, including single-file and batch workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[besteva77](https://clawhub.ai/user/besteva77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and external users use this skill when they need an agent to prepare or run document, image, and spreadsheet file conversions while checking dependencies, output locations, and conversion results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad batch conversions can write many files or write into unexpected locations if pointed at important directories.

Mitigation: Use a dedicated output folder, avoid batch runs over important directories, and review generated paths before opening or sharing results.

Risk: CSV files from untrusted sources may contain formulas that execute when opened in spreadsheet software.

Mitigation: Treat untrusted CSV and Excel outputs as active content and inspect or sanitize formula-like cells before opening them in a spreadsheet application.

Risk: PDF conversion and manipulation behavior may be hard to audit for complex or malformed files.

Mitigation: Run conversions in an isolated virtual environment and review output quality and contents before relying on converted files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/besteva77/skills/besteva-file-converter)
- [Publisher profile](https://clawhub.ai/user/besteva77)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Files]

**Output Format:** [Markdown with inline shell commands and file path summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create converted files in user-selected output paths or batch output directories.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
