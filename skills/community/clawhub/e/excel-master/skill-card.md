## Description:

Excel Master helps an agent open, inspect, filter, summarize, analyze, and save spreadsheet workbooks across multiple sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zywss](https://clawhub.ai/user/zywss)

### License/Terms of Use:

MIT-0

## Use Case:

Spreadsheet users and developers use this skill to let an agent work with Excel files: opening workbooks, viewing data, switching sheets, filtering rows, computing basic statistics, saving changes, and summarizing table structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read spreadsheet files named by the user and overwrite the currently opened workbook when asked to save.

Mitigation: Use it only with intended workbook paths, keep backups of important spreadsheets, and review save requests before allowing overwrite behavior.

Risk: The package claims dependency-free operation but requires the xlsx runtime package while declaring no dependencies.

Mitigation: Declare and pin the xlsx dependency before deployment, then retest workbook read and write behavior in the target runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zywss/skills/excel-master)
- [Artifact README](README.md)
- [Artifact skill definition](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Agent-facing text responses with JSON-formatted table previews and statistics when data is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read named spreadsheet files and save changes back to the currently opened workbook when requested]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
