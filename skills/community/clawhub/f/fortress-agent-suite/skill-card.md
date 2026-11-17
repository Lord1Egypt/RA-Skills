## Description:

Fortress Agent Suite provides self-healing, health monitoring, automated maintenance, proactive hardening, and model management for OpenClaw deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kienphan91](https://clawhub.ai/user/kienphan91)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add scheduled recovery, monitoring, backup, workspace integrity checks, and LLM provider configuration management to OpenClaw deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent root-level scheduled automation can modify OpenClaw configuration, restart services, and alter workspace state.

Mitigation: Install only in a trusted, isolated OpenClaw environment after reviewing every scheduled job and script; do not use shared systems or production hosts unless recurring root-level control is acceptable.

Risk: Automatic rollback, Git commits, gateway restarts, outbound Telegram notifications, and automatic skill installation can change state or disclose operational information with weak user control.

Mitigation: Remove auto-skill installation and cron self-repair before use, replace shell-based commands, add an uninstall path, and keep backups outside any Git repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kienphan91/skills/fortress-agent-suite)
- [Publisher profile](https://clawhub.ai/user/kienphan91)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration details, and operational code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance and configuration-oriented changes for OpenClaw environments; no structured API response contract is declared.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
