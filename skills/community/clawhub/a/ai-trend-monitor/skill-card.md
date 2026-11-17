## Description:

Monitors AI trend signals across GitHub, Reddit, Twitter/X, Xiaohongshu, and news sources, then produces major-news alerts and scheduled Feishu summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyuyang001-oss](https://clawhub.ai/user/wuyuyang001-oss)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and market research teams can use this skill to monitor AI market and technical trends, detect major AI news by configurable criteria, and send real-time or scheduled Feishu notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu webhook URLs can notify unintended recipients if they are misconfigured.

Mitigation: Confirm every webhook URL before installation and keep webhook secrets scoped to the intended Feishu recipients.

Risk: The current artifact behaves like a prototype: it uses mock search data, and only the scheduled summary path performs an actual webhook POST.

Mitigation: Validate the intended run mode before relying on alerts, and replace mock search data with the intended search API before production monitoring.

## Reference(s):

- [Skill documentation](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/wuyuyang001-oss/skills/ai-trend-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Feishu interactive card JSON, Markdown-style notification text, and console text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled summaries can be sent through Feishu webhooks; real-time major-news mode logs notification text in the current artifact.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
