## Description:

Create independent OpenClaw agents through an interview-driven workflow that scaffolds workspaces, personality files, channel settings, tool permissions, and team registry entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limoxt](https://clawhub.ai/user/limoxt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to define and deploy dedicated agents with isolated workspaces, tailored model choices, tool permissions, channel bindings, and generated operating files. It is intended for agent setup workflows that require an interview, visible configuration review, and deployment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make persistent OpenClaw workspace, registry, and gateway configuration changes, including broad session visibility.

Mitigation: Require a visible change plan, review the exact agent ID, workspace path, allow list changes, and sessions.visibility setting before deployment, and avoid sessions.visibility all unless the use case requires it.

Risk: Bundled helper scripts can create or remove agent directories and may affect more than the intended agent when used with untrusted or unusual agent IDs.

Mitigation: Use only trusted agent names, inspect script parameters before execution, keep backups of OpenClaw configuration and workspace data, and do not run remove-agent.sh on untrusted inputs until input validation is added.

## Reference(s):

- [Agent Forge Skill Page](https://clawhub.ai/limoxt/skills/agent-forge)
- [OpenClaw Multi-Agent Architecture](references/openclaw-multi-agent.md)
- [OpenClaw Multi-Agent Concepts](https://docs.openclaw.ai/concepts/multi-agent)
- [OpenClaw Session Concepts](https://docs.openclaw.ai/concepts/session)
- [OpenClaw Subagents Tool](https://docs.openclaw.ai/tools/subagents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent workspace files and OpenClaw configuration guidance based on interview inputs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
