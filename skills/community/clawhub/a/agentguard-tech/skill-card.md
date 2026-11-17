## Description:

Installs AgentGuard to secure an AI agent by wrapping tools with evaluate() to block prompt injection, tool abuse, and malicious commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koshaji](https://clawhub.ai/user/koshaji)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add AgentGuard-based security controls to an AI agent, including tool-call evaluation, policy configuration, and status verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a mutable third-party npm package that can participate in agent security decisions.

Mitigation: Use a pinned and reviewed AgentGuard SDK version before deploying it in a real agent or project.

Risk: The skill wraps tool calls with evaluate(), which may inspect tool names and arguments.

Mitigation: Confirm AgentGuard data-handling terms and limit sensitive tool arguments before allowing the SDK to evaluate every tool call.

Risk: The skill can create an external AgentGuard account and store an API key locally.

Mitigation: Require explicit approval before account creation and store any API key in protected secret storage rather than plain project files.

## Reference(s):

- [AgentGuard Tech ClawHub Skill Page](https://clawhub.ai/koshaji/skills/agentguard-tech)
- [AgentGuard Enterprise](https://agentguard.thebot.club/enterprise)
- [AgentGuard Dashboard](https://agentguard.thebot.club/dashboard)
- [AgentGuard API Keys](https://agentguard.thebot.club/keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose npm installation, account or API-key setup, tool wrapping, local configuration files, and verification steps.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
