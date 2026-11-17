## Description:

Spawn a new OpenClaw agent through conversation. Uses official Docker setup and non-interactive onboarding, carries over API keys, tools, plugins, and skills from the current agent. User answers 2-3 questions. Use when the user wants to create, spin up, deploy, or provision a new OpenClaw agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[austineral](https://clawhub.ai/user/austineral)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to provision a new OpenClaw agent through a short conversational flow, carrying over detected provider settings, credentials, plugins, and workspace skills from the current agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw config, .env files, and token-like environment variables, then carries credentials into a new persistent agent.

Mitigation: Ask for explicit approval before reading secrets, limit collection to named required credentials, and avoid copying unrelated tokens or tool keys.

Risk: The skill runs network installers and installs plugins that may change over time.

Mitigation: Pin installer and plugin versions where possible, verify sources before execution, and show the exact commands for user confirmation.

Risk: The skill exposes an OpenClaw gateway and displays a live gateway token.

Mitigation: Default gateway binding to localhost unless remote access is explicitly requested, require confirmation for exposed ports, and avoid printing live tokens into chat.

## Reference(s):

- [OpenClaw repository](https://github.com/openclaw/openclaw.git)
- [OpenClaw install script](https://openclaw.ai/install.sh)
- [ClawHub skill page](https://clawhub.ai/austineral/skills/agent-spawner)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and deployment steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a deployment plan, command sequence, access URL, and gateway token handoff.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
