## Description:

Use in Feishu when long-running tasks should proactively report concise progress updates every 3 minutes, including stage-based percentage estimates and blocker notices when work appears stalled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents working in Feishu use this skill to keep long-running document generation, batch processing, and multi-step workflows visible with short progress heartbeats. It helps avoid silent waits while reducing fake or repetitive status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Periodic progress messages may expose sensitive task names or confidential work in a Feishu conversation.

Mitigation: Review workspace policy and task naming practices before enabling heartbeat updates for confidential workflows.

Risk: Chinese-oriented examples may not fit every team's language or tone expectations.

Mitigation: Localize the status-line examples and blocker phrasing before rollout where needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wd041216-bit/skills/feishu-progress-heartbeat)
- [Project homepage](https://github.com/wd041216-bit/openclaw-feishu-progress-heartbeat)
- [Publisher profile](https://clawhub.ai/user/wd041216-bit)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Short Feishu-friendly status lines or HEARTBEAT_OK]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stage-based percentage estimates; no executable code.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
