## Description:

Generates Xiaohongshu operations reports from Feishu Bitable data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangfeng1995](https://clawhub.ai/user/huangfeng1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operations teams use this skill to read Xiaohongshu post metrics from Feishu Bitable and produce a weekly performance report with data overview, high-performing content analysis, issue diagnosis, and optimization suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may access more Feishu Bitable data than needed if the connected app has broad read permissions.

Mitigation: Limit the Feishu app to read access for the specific Bitable and columns needed for Xiaohongshu reporting before installation.

Risk: Report output may be in Chinese by default.

Mitigation: Ask the agent to adapt the report language when a different audience language is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangfeng1995/skills/ai-report-generator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report content is based on Feishu Bitable fields for post title, publish time, views, likes, saves, comments, and shares.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
