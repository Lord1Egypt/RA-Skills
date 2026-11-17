## Description:

根据书名生成读书活动，生成详细介绍、每日打卡计划、问答题库等文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lay-white](https://clawhub.ai/user/lay-white)

### License/Terms of Use:

MIT-0

## Use Case:

External users can provide a book title and use this skill to create a reading activity package with a book introduction, a seven-day reading check-in plan, and a question bank.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates local files and packages generated outputs into a ZIP archive.

Mitigation: Confirm the configured output path and permissions before running, and inspect generated files before sharing the archive.

Risk: The documented workflow uses .xls filenames while the helper reports that .xls output is unsupported.

Mitigation: Use a supported spreadsheet extension or update the helper before relying on spreadsheet generation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown documents, Excel-compatible files, and a ZIP archive]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs are organized under a timestamped local reading-activities folder.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
