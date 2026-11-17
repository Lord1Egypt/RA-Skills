## Description:

ClawFeed 新闻推送定时抓取 BBC、CNBC、Reuters 和 Al Jazeera 新闻，使用 AI 生成中文摘要，并推送到飞书。

This skill is ready for commercial/non-commercial use.

## Publisher:

[goofyfht-blip](https://clawhub.ai/user/goofyfht-blip)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or operators use this skill to generate daily Chinese summaries of global news and send them to Feishu, either manually for tests or on a configured weekday schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring scheduled execution may send weekday news pushes without clear user confirmation.

Mitigation: Review or remove the crontab entry and prefer manual runs until the schedule is explicitly configured.

Risk: A fixed Feishu recipient may send summaries to an unintended conversation.

Mitigation: Confirm and update the Feishu recipient before installation or execution.

Risk: The skill references workspace scripts outside the reviewed package.

Mitigation: Inspect the referenced workspace scripts before allowing automated or manual execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Chinese news-summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate Feishu message delivery when configured; scheduled behavior depends on external workspace scripts not included in the reviewed artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
