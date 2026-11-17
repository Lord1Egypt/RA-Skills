## Description:

Use when installing or setting up AgentLayer wallet for an AI agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lopushok9](https://clawhub.ai/user/lopushok9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and set up a local AgentLayer wallet runtime for OpenClaw, Claude Code, Codex, or Hermes. It provides installation commands and a short post-install briefing for agent wallet workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses unpinned npm execution with auto-approval for wallet and host-plugin installation.

Mitigation: Review the npm package and publisher before installing, prefer a pinned exact version, and avoid running the installer with elevated privileges.

Risk: The installed wallet and AI-host integrations can affect financial workflows.

Mitigation: Confirm the intended wallet behavior, permissions, and supported host integrations before use in environments that handle funds or transactions.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/lopushok9/Agent-Layer/tree/main/skills/agent-layer)
- [AgentLayer documentation](https://docs.agent-layer.tech)
- [AgentLayer GitHub repository](https://github.com/lopushok9/Agent-Layer)
- [AgentLayer blog](https://x.com/agentlayer_ai)
- [ClawHub skill page](https://clawhub.ai/lopushok9/skills/agent-layer)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes host-specific install commands and a concise post-install briefing.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
