## Description:

Auto-Heal monitors OpenClaw health and attempts automatic recovery for unresponsive gateways, stale agent sessions, and high memory usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zacharyzax](https://clawhub.ai/user/zacharyzax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw deployments and receive setup guidance, shell commands, and configuration for automatic health checks and recovery actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic repair behavior can restart OpenClaw services, kill sessions, and delete logs.

Mitigation: Review before installing in any active OpenClaw environment and run under an account whose sessions and logs may be modified.

Risk: Documented safety controls may not be enforced by the implementation.

Mitigation: Do not rely on enabled=false or autoFix=false until those settings are fixed and verified.

Risk: Background cron or nohup deployment can repeatedly execute unsafe recovery actions.

Mitigation: Avoid cron/nohup deployment until command execution is shell-safe and destructive repairs are gated or dry-run capable.

## Reference(s):

- [ClawHub Auto-Heal release](https://clawhub.ai/zacharyzax/skills/auto-heal)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operational guidance should account for automatic repair behavior and documented safety controls.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
