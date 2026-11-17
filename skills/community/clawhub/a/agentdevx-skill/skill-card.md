## Description:

Agentdevx Skill helps agents use AgentDevX to register APIs from OpenAPI specs and route calls through identity, credential vault, memory, rate limiting, and audit logging features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirajmahmudul](https://clawhub.ai/user/mirajmahmudul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect agents to the AgentDevX gateway, configure MCP access, register APIs from OpenAPI specs, and use persistent memory or credential-backed API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a third-party hosted gateway for setup, API calls, credentials, and persistent memory.

Mitigation: Review the gateway trust boundary before installation and use only data or API keys you are willing to expose to AgentDevX.

Risk: The skill can automatically create an AgentDevX account and route credentials through that service on first use.

Mitigation: Verify token scope, revocation, retention, and credential isolation outside the skill text before invoking its tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirajmahmudul/skills/agentdevx-skill)
- [AgentDevX gateway](https://agentdevx.onrender.com)
- [Smithery AgentDevX listing](https://smithery.ai/server/io.github.mirajmahmudul/agentdevx)
- [AgentDevX SDK](https://github.com/mirajmahmudul/agentdevx-sdk)
- [AgentDevX npm package](https://www.npmjs.com/package/@agentdevx/install)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe outbound AgentDevX calls and environment variables such as AGENTDEVX_API_KEY.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
