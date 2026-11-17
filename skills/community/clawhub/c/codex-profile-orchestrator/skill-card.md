## Description:

Deterministic OpenClaw Codex profile failover for Windows workspaces with duplicate detection, workspace variant aliases, quota-aware profile choice, Telegram session sync, network outage protection, and install helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugurinanc12](https://clawhub.ai/user/ugurinanc12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to stabilize multi-account Codex profile switching in OpenClaw workspaces, inspect OAuth profile state, select a healthier account, and install a repeatable profile orchestration workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy token-bearing Codex profile data into workspace registry or backup files.

Mitigation: Run dry-run first, keep the workspace state directory private, and protect or remove registry and backup files that may contain credentials.

Risk: Apply or daemon mode can rewrite authentication profile order, session overrides, and remove invalid profiles after the configured streak.

Mitigation: Inspect the dry-run JSON before enabling apply or daemon mode, and use conservative invalid-streak settings.

Risk: Telegram and other OpenClaw session sync can move session overrides to the selected profile.

Mitigation: Limit configured session targets and verify the selected profile before enabling notifications or session sync.

## Reference(s):

- [State Model](references/state-model.md)
- [ClawHub skill page](https://clawhub.ai/ugurinanc12/skills/codex-profile-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads, shell commands, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce dry-run reports, apply-mode changes, daemon startup commands, and installation configuration.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
