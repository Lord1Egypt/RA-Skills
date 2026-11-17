## Description:

Claude Code Enhancement adds OpenClaw helpers for coordinating multiple agents, managing tool permissions, storing structured memory, and tracking task workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntaffffff](https://clawhub.ai/user/ntaffffff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using OpenClaw use this skill to coordinate worker agents, manage tool access, persist project preferences, and track task progress during coding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain sensitive user, project, client, or regulated information.

Mitigation: Do not store secrets, credentials, private client data, or regulated information in memory; require confirmation before saving persistent memory.

Risk: Permission controls are too broad for automatic approval, including default allowance of unknown tools and a bypass mode.

Mitigation: Deny unknown tools by default, remove or lock down bypass mode, and require confirmation for file changes, shell commands, and network-capable tools.

Risk: Agent creation can delegate tasks without enough review when used in unattended workflows.

Mitigation: Require user confirmation for agent creation and review spawned-agent prompts, tool access, and outputs before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntaffffff/skills/claude-code-enhancement)
- [ClawHub publisher profile](https://clawhub.ai/user/ntaffffff)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-oriented text with inline code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent memory entries and agent or task state in the local OpenClaw workspace.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
