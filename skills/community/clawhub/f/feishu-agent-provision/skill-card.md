## Description:

Creates, clones, deletes, diagnoses, and schedules Feishu group AI agents for OpenClaw, including workspace files, group routing, cron reports, and persistent memory setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmqiang-711](https://clawhub.ai/user/lmqiang-711)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to provision Feishu group-specific agents, manage group bindings, schedule recurring reports, clone existing agent workspaces, delete retired agents, and diagnose routing issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill administers local OpenClaw agents, Feishu group bindings, scheduled jobs, and persistent memory.

Mitigation: Install and run it only when those administrative changes are intended, review the planned workspace, binding, cron, and gateway changes before approval, and keep a backup of the OpenClaw configuration.

Risk: Unsafe file-write or command-generation behavior could affect the user's local OpenClaw setup when inputs are untrusted.

Mitigation: Review or patch path validation and cron command generation before accepting untrusted agent IDs, paths, group IDs, or schedule values.

Risk: Scheduled Feishu reports can send messages to a group if delivery settings are wrong or insufficiently reviewed.

Mitigation: Validate delivery.channel, delivery.to, sessionTarget, and the send-before-confirmation wording before enabling cron jobs.

Risk: Deletion cleanup may leave residual workspaces or remove active agent state unexpectedly.

Mitigation: Use the preview and explicit confirmation flow, stop active sessions before deletion, verify trash-based cleanup in the target environment, and restart the gateway only after reviewing the result.

## Reference(s):

- [Cron Template](artifact/references/cron-template.md)
- [ClawHub Skill Page](https://clawhub.ai/lmqiang-711/skills/feishu-agent-provision)
- [Publisher Profile](https://clawhub.ai/user/lmqiang-711)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python helper scripts, JSON configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for confirmation before sensitive configuration changes, scheduled-message setup, cloning, deletion, and gateway restart steps.]

## Skill Version(s):

3.2.8 (source: server release evidence and artifact version history, released 2026-06-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
