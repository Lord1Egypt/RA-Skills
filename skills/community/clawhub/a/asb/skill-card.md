## Description:

Asb helps agents use Agent Service Bus through an MCP server for service discovery, service composition, governance, LLM calls, messaging, CLI use, and A2A collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiyueqiu](https://clawhub.ai/user/qiyueqiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to configure and operate ASB integrations from an agent environment, including discovering services, composing workflows, sending messages, and invoking ASB CLI or MCP capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install and run external ASB code without a pinned version.

Mitigation: Use a pinned, reviewed ASB release and verify the package or repository before installation.

Risk: ASB orchestration, message sending, and LLM-provider capabilities may send data externally or trigger downstream operations.

Mitigation: Run the integration with least privilege, avoid sensitive data unless explicitly approved, and review planned operations before connecting real services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiyueqiu/skills/asb)
- [Agent Service Bus GitHub repository](https://github.com/qiyueqiu/Agent-Service-Bus)
- [Agent Service Bus documentation](https://github.com/qiyueqiu/Agent-Service-Bus/tree/main/docs)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP server configuration, ASB CLI commands, service orchestration guidance, and A2A integration examples.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
