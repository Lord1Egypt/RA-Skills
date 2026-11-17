## Description:

Monitors OpenClaw context-window usage and compresses older conversations when configured thresholds are exceeded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuhui435](https://clawhub.ai/user/yuhui435)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators using OpenClaw can use this skill to monitor context-window usage, trigger compression of older conversation history above configured thresholds, and preserve recent conversation rounds and key memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent hourly agent execution may run without active review.

Mitigation: Enable the scheduled task only after verifying the referenced scripts and documenting how to disable the cron entry.

Risk: The documented PowerShell command uses execution-policy bypass for an unaudited script path.

Mitigation: Run only scripts whose contents and hashes have been verified, and avoid execution-policy bypass unless it is explicitly required in a trusted environment.

Risk: Conversation compression may remove or alter context that users still need.

Mitigation: Confirm what data will be compressed or retained, keep backups or exports where appropriate, and tune retention thresholds before enabling automation.

## Reference(s):

- [Context Monitor ClawHub Skill Page](https://clawhub.ai/yuhui435/skills/context-monitor)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with PowerShell, Bash, configuration table, and log examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes warning and critical thresholds, recent-round retention, check interval, scheduled execution, and log output.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
