## Description:

An OpenClaw memory-management skill that guides agents to build a local three-layer memory system, organize notes and files, run AutoDream consolidation, and propose backups with user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yewubin-jpg](https://clawhub.ai/user/yewubin-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to give an agent a persistent local memory workflow for user preferences, project context, notes, files, error lessons, and periodic memory consolidation. It is intended for users who want agent-assisted organization of a local workspace while retaining explicit confirmation before broad writes, scheduled automation, backup, or external sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for persistent automation and broad local workspace access.

Mitigation: Require separate user opt-in before enabling memory writes, profile storage, AutoDream scheduling, MCP sync, or workspace backup.

Risk: Workspace backups and imported assistant histories may capture sensitive local data.

Mitigation: Review what will be saved before backup or import, avoid sensitive workspaces by default, and confirm retention, restore, and deletion procedures.

Risk: Scheduled jobs may continue changing or scanning the workspace after initial setup.

Mitigation: Confirm how to list, inspect, modify, and remove cron jobs before enabling AutoDream or backup automation.

Risk: Memory contents may become outdated or conflict with current files and user intent.

Mitigation: Treat memory as hints, verify important actions against current files and user confirmation, and update contradictory memory entries explicitly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yewubin-jpg/skills/claude-code-memory-yewubin)
- [Artifact README](artifact/README.md)
- [Installation guide](artifact/INSTALLATION_GUIDE.md)
- [Onboarding guide](artifact/templates/ONBOARDING_GUIDE.md)
- [AutoDream protocol](artifact/templates/DREAM_PROTOCOL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workspace organization guidance, memory templates, onboarding prompts, and proposed automation steps for review before execution.]

## Skill Version(s):

1.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
