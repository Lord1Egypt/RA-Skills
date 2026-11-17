## Description:

Search, register, and manage internet domains for AI agents via DomainForAgents API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[midnight-rgb](https://clawhub.ai/user/midnight-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search for domains, generate domain suggestions, register or renew domains, manage DNS records, and check domain pricing or account balance through the DomainForAgents API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real domain purchases, renewals, payment actions, or DNS writes.

Mitigation: Require explicit user confirmation before any purchase, renewal, payment action, or DNS change.

Risk: API keys and claim codes may be exposed in chat logs or command output.

Mitigation: Store credentials in a secret store or environment variable and avoid printing secrets in chat, logs, or examples.

Risk: The recommended MCP package is installed through an unpinned package command.

Mitigation: Use a pinned and reviewed MCP package version where possible before installation.

## Reference(s):

- [DomainForAgents Documentation](https://domainforagents.io/docs)
- [DomainForAgents OpenAPI Specification](https://api.domainforagents.io/api/openapi.json)
- [DomainForAgents MCP Server](https://www.npmjs.com/package/@domainforagents/mcp)
- [ClawHub Skill Page](https://clawhub.ai/midnight-rgb/skills/domainforagents)
- [Publisher Profile](https://clawhub.ai/user/midnight-rgb)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include REST API calls, MCP setup commands, DNS record examples, and payment or renewal guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
