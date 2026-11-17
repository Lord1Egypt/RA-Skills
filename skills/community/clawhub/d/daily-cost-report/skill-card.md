## Description:

Generate daily OpenClaw cost reports with breakdown by agent/model/channel. Use when: daily cron job, on-demand cost analysis, cost auditing. Generates HTML-formatted email reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kjvarga](https://clawhub.ai/user/kjvarga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate daily OpenClaw usage and cost reports for cost auditing, usage review, and scheduled email delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process broad OpenClaw usage metadata and email reports externally.

Mitigation: Use local-only report generation unless recipients are trusted and explicitly configured.

Risk: Reports are stored in predictable /tmp file paths that may expose usage or cost data on shared systems.

Mitigation: Store reports in a private user-owned directory with restrictive permissions.

Risk: Scheduled execution could increase impact if run with elevated privileges.

Mitigation: Avoid running this as a privileged scheduled job.

Risk: The release declares an OPENAI_API_KEY requirement that the security guidance identifies as unused.

Mitigation: Remove the unused OPENAI_API_KEY requirement before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kjvarga/skills/daily-cost-report)
- [Publisher profile](https://clawhub.ai/user/kjvarga)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown cost reports, HTML email reports, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize cost, token usage, cache metrics, model usage, channel usage, and top sessions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
