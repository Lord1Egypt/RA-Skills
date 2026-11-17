## Description:

定时访问指定电商或社交平台页面，抓取点赞、评论、销量等数据，检测异常波动，自动截图并发送提醒通知。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hwl1413520](https://clawhub.ai/user/hwl1413520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure scheduled competitor monitoring for public ecommerce and social pages, track engagement or sales metrics, detect spikes, and receive alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser scraper can access user-configured URLs with broad network reach.

Mitigation: Restrict task configs to trusted public platform URLs and avoid running the skill on networks that expose sensitive internal services.

Risk: Monitoring results and screenshots can capture and retain sensitive competitive or account data.

Mitigation: Disable screenshots unless needed, set short retention windows, and protect the data and screenshot directories.

Risk: Webhook and email notifications can send captured monitoring details or attachments to unintended destinations.

Mitigation: Review every notification destination and secret before execution, and test alerts with non-sensitive data first.

Risk: The installer installs browser automation dependencies and accepts custom target paths.

Mitigation: Run installation in a virtual environment with reviewed paths and pinned dependencies where possible.

## Reference(s):

- [Platform Selectors Reference](references/PLATFORM_SELECTORS.md)
- [ClawHub Skill Page](https://clawhub.ai/hwl1413520/skills/competitor-monitor-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and Python code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, the skill can write JSONL monitoring data, alert records, screenshots, and Markdown reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
