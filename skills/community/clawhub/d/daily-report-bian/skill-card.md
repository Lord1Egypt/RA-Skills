## Description:

Automatically generates a concise daily research progress report from Feishu session history and recent memory files, then prepares it for scheduled Feishu delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[databian](https://clawhub.ai/user/databian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to summarize daily research work into a Feishu-ready report covering today's progress, continuing projects, tomorrow's plan, system status, and a 30-day activity heatmap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive Feishu session history and recent memory files with weak scoping.

Mitigation: Limit use to a specific Feishu user or conversation and install only where the operator is authorized to process that information.

Risk: Generated summaries can persist information into memory files and may be routed for Feishu delivery.

Mitigation: Show a report preview before sending and make memory writes optional or explicitly confirmed.

Risk: The security review recommends caution in shared or multi-user OpenClaw environments.

Mitigation: Review the skill before installation and avoid shared deployments unless access and routing are tightly restricted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/databian/skills/daily-report-bian)
- [Publisher profile](https://clawhub.ai/user/databian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown report text with shell command usage examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill documentation caps the report at 1000 Chinese characters and includes a 30-day activity heatmap.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
