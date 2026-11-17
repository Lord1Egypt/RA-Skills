## Description:

Visualize coding sessions as a real-time strategy game with automatic deploy and event reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[idosal](https://clawhub.ai/user/idosal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use AgentCraft to visualize coding sessions, start a local AgentCraft service when needed, and report session, prompt, file access, command, and idle events to a local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can report sensitive prompts, file paths, and shell commands to the local AgentCraft service.

Mitigation: Use it only in non-sensitive workspaces unless telemetry is reduced or disabled, and redact prompts, paths, and commands before reporting.

Risk: The skill can start third-party code through npx.

Mitigation: Review the package before installation and prefer a pinned, reviewed AgentCraft version with explicit user consent.

Risk: Sharing the local service through a public tunnel can expose session telemetry.

Mitigation: Do not expose the local service through a public tunnel without authentication.

## Reference(s):

- [AgentCraft homepage](https://getagentcraft.com)
- [ClawHub AgentCraft skill page](https://clawhub.ai/idosal/skills/agentcraft)
- [ClawHub idosal publisher profile](https://clawhub.ai/user/idosal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON event payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to run local health checks, start AgentCraft through npx, create a session identifier, and post event reports with curl.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
