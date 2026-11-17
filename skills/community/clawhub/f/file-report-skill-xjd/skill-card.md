## Description:

统计指定目录的文件类型和数量，生成Markdown格式报表

This skill is ready for commercial/non-commercial use.

## Publisher:

[xujiangdong](https://clawhub.ai/user/xujiangdong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize the files in a selected directory by extension and receive a concise Markdown report with counts and totals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests local filesystem write access even though its documented workflow returns the Markdown report in conversation.

Mitigation: Review before installing and remove or reject filesystem.write unless the skill is updated to clearly document confirmed, user-chosen file output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xujiangdong/skills/file-report-skill-xjd)
- [Publisher profile](https://clawhub.ai/user/xujiangdong)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the selected directory path, statistics timestamp, a table of file types and counts, and total file count; documented behavior excludes files in subdirectories.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
