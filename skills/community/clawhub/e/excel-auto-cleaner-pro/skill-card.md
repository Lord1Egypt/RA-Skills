## Description:

Excel 数据自动清洗引擎 Pro helps agents clean CSV, XLSX, and JSON spreadsheet data by deduplicating rows, standardizing formats, handling missing values, classifying records, validating data logic, and producing quality reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhao123-dot](https://clawhub.ai/user/lijinhao123-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, operations, purchasing, ecommerce, and data analysis users can use this skill to turn messy business spreadsheets into cleaner datasets and reviewable cleaning reports. It is intended for agent-assisted data preparation tasks such as deduplication, normalization, missing-value handling, validation, and basic reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads business spreadsheets and creates cleaned output and report files, which may expose sensitive operational data if used on unapproved datasets.

Mitigation: Use it only with datasets the agent is permitted to read and write, and review generated cleaned files and reports before sharing them.

Risk: The security assessment notes that personal phone numbers may be sent to external web search during validation without clear consent or limits.

Mitigation: Require validation to remain local for datasets containing phone numbers, names, addresses, or ID numbers unless a specific external lookup is explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijinhao123-dot/skills/excel-auto-cleaner-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/lijinhao123-dot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with generated cleaning scripts, shell commands, cleaned spreadsheet files, and report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cleaned XLSX files and Markdown quality reports derived from user-provided datasets.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
