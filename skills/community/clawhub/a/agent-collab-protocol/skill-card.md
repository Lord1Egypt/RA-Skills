## Description:

Standardized agent collaboration protocol for multi-agent systems. Defines L0/L1/L2 hierarchy, task contracts, error handling, agent templates, and a new-agent creation checklist — ready to use with OpenClaw or any agent framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[congjianfei](https://clawhub.ai/user/congjianfei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, framework authors, and team leads use this skill to standardize multi-agent collaboration, define L0/L1/L2 responsibilities, and scaffold OpenClaw-compatible agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agent instructions and configuration can grant broad control to user or task input.

Mitigation: Review and revise generated prompts, task contracts, and OpenClaw configuration so user/task content cannot override platform policy, authorization boundaries, or agent red lines.

Risk: The scaffold and operations guidance include filesystem workflows that can create or remove OpenClaw workspace and agent directories.

Mitigation: Run scaffold commands only with trusted simple identifiers, review generated paths and configuration before use, and avoid removal steps without validation and backups.

Risk: The security verdict is suspicious and requires review before installation or execution.

Mitigation: Install only after reviewing the artifact, using a pinned installer version, and confirming that the generated configuration matches the intended deployment.

## Reference(s):

- [Agent Collaboration Protocol](references/AGENT_COLLAB_PROTOCOL.md)
- [Operations Guide](references/OPERATIONS.md)
- [New Agent Checklist](references/NEW_AGENT_CHECKLIST.md)
- [AGENTS Template](references/TEMPLATE_AGENTS.md)
- [Identity Template](references/TEMPLATE_IDENTITY.md)
- [Values Template](references/TEMPLATE_SOUL.md)
- [Service Object Template](references/TEMPLATE_USER.md)
- [Domain Scaffold Script](references/scaffold-domain.sh)
- [ClawHub Skill Page](https://clawhub.ai/congjianfei/skills/agent-collab-protocol)
- [Publisher Profile](https://clawhub.ai/user/congjianfei)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown protocol files, JSON configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes templates, checklist-driven guidance, and a shell scaffold for OpenClaw agent workspace setup.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact _meta.json, and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
