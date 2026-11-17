## Description:

A general daily news briefing skill that searches recent news for a configured domain, organizes it into a fixed Markdown report, and sends it through WeCom, Feishu, or Webhook channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shoyee94](https://clawhub.ai/user/shoyee94)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate concise daily Markdown news reports for a chosen topic and push them to enterprise messaging or webhook destinations. It supports interactive or manual configuration of the news domain, delivery channel, recipients, source preferences, and schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-entered configuration can be written into executable Python config files.

Mitigation: Review generated config.py before running the skill, avoid pasting configuration values from untrusted sources, and prefer manually creating a minimal safe config for sensitive deployments.

Risk: Webhook delivery can send report content to unrestricted external destinations.

Mitigation: Restrict webhook URLs to trusted HTTPS endpoints, avoid sensitive report content, and review webhook headers and destinations before enabling scheduled runs.

Risk: The documented cron setup can repeatedly execute the configured push workflow.

Mitigation: Verify the cron expression and script path before installation, and enable scheduled execution only after testing the configuration manually.

## Reference(s):

- [Configuration Reference](references/config.md)
- [Daily Report Format Reference](references/format.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report text with setup commands and Python configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a scheduled daily briefing and delivery-channel payloads for WeCom, Feishu, or Webhook.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
