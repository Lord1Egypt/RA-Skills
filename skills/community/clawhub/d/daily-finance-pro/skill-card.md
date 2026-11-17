## Description:

Daily Finance Pro generates concise Chinese daily finance summaries with market sentiment indicators and optional scheduled delivery to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxxc](https://clawhub.ai/user/foxxc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused teams use this skill to request daily market briefings or configure recurring Feishu pushes that summarize top finance news, market mood, and key data points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled Feishu summaries may be visible to channel members or workspace administrators.

Mitigation: Review the Feishu destination and audience before enabling or changing a recurring push.

Risk: The artifact has minor documentation ambiguity around summary length and item count.

Mitigation: Confirm the desired report length and item count when configuring production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foxxc/skills/daily-finance-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style Chinese finance briefings with optional OpenClaw cron commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual reports include selected finance news and platform hot lists; scheduled Feishu pushes are concise summaries with market sentiment and a short item list.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
