## Description:

中国新闻聚合(专业版) helps agents aggregate Chinese news, summarize it with AI, schedule recurring runs, analyze sentiment, search history, and distribute results through configured channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external teams use this skill to monitor Chinese news sources, generate summaries and reports, track sentiment, and send alerts or briefings to collaboration channels. It is intended for news aggregation, market research, public-relations monitoring, and internal intelligence workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound webhooks and callback URLs could send summaries or alerts to unintended destinations.

Mitigation: Inspect generated configuration, allow only trusted HTTPS endpoints, avoid arbitrary callback URLs, and require confirmation before sending to Feishu, DingTalk, email, Slack, or other webhooks.

Risk: Scheduled execution can create recurring network activity and repeated message delivery.

Mitigation: Require explicit user confirmation before starting scheduled jobs and review cron or schedule settings before enabling them.

Risk: Broad activation wording may cause the skill to run outside an explicit news aggregation request.

Mitigation: Use this skill only for explicit news aggregation, monitoring, summarization, or distribution requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/china-news-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON, YAML, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce news summaries, sentiment labels, execution logs, scheduled job configuration, webhook delivery guidance, and channel-specific message content.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
