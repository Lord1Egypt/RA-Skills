## Description:

Give your OpenClaw agent its own email inbox. Use AgentSend to create inboxes, send and receive email, inspect threads, and register webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luv005](https://clawhub.ai/user/luv005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when an OpenClaw agent needs to create inboxes, send or receive email, inspect threads, or register email webhooks through AgentSend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses an external MCP package.

Mitigation: Review or pin the @agentsend/mcp runtime where possible before deployment.

Risk: AgentSend API keys or sandbox credentials may be stored locally.

Mitigation: Treat AGENTSEND_API_KEY and ~/.agentsend/credentials.json as sensitive and use an account or sandbox that can be revoked.

Risk: The agent can send messages or register webhook URLs.

Mitigation: Confirm message recipients, content, and webhook URLs before use, and register webhooks only for URLs the user controls.

## Reference(s):

- [AgentSend Skill Setup](https://agentsend.io/skill)
- [AgentSend Email on ClawHub](https://clawhub.ai/luv005/skills/agentsend-email)

## Skill Output:

**Output Type(s):** [text, guidance, configuration, API calls]

**Output Format:** [Markdown guidance with tool-use instructions and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use AGENTSEND_API_KEY or locally stored AgentSend sandbox credentials.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
