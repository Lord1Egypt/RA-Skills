## Description:

AI新闻工具-专业版 helps agents aggregate multi-source news, generate AI summaries and keywords, manage subscriptions and alerts, search historical news, and analyze topic trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and enterprise teams use this skill to monitor news, track industry and competitor activity, generate digests and reports, and configure recurring alerts or pushes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad command execution through the external news-pro CLI can perform actions outside the reader's intended news-intelligence task.

Mitigation: Install only when the CLI is trusted, run it with least privilege, and limit agent use to the documented news aggregation, search, reporting, and alert workflows.

Risk: Recurring alerts and outbound webhook or email pushes can disclose monitored topics, internal reports, or sensitive destinations.

Mitigation: Review scheduled push configuration before enabling it and use only approved webhook, email, report, API-key, and local-index destinations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/ai-news-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, JSON, YAML, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce reports, JSON or CSV exports, webhook or email push configurations, and local news-index guidance when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
