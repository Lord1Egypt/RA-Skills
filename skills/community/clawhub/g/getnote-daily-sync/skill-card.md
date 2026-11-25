## Description:

每日自动将 Get笔记（biji.com）当天的录音笔记、会议记录、待办事项汇总后写入 Notion 数据库，生成结构化日报页面。

This skill is ready for commercial/non-commercial use.

## Publisher:

[phoenixyy](https://clawhub.ai/user/phoenixyy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to sync the current day's Get笔记 notes, recordings, meeting summaries, and to-dos into a structured Notion daily report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to Get笔记 API credentials, a Notion token, and daily note contents.

Mitigation: Install only when this access is acceptable, store credentials as environment variables, and use a Notion integration limited to the target database.

Risk: Scheduled syncs can run automatically and may write notes at an unintended time.

Mitigation: Review the optional Cron schedule before enabling it and adjust the timezone if Asia/Shanghai is not appropriate.

## Reference(s):

- [Create a Notion integration](https://developers.notion.com/docs/create-a-notion-integration)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Notion page content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured Notion daily report and a short status message with the created page URL.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
