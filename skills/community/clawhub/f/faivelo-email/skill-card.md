## Description:

Set up and use email on a custom domain with Faivelo. Use when the user needs mailboxes on their own domain (hello@, support@, team inboxes), wants their app to send transactional email (receipts, password resets, notifications) from their domain, needs to receive replies or inbound mail as webhooks, or wants an AI agent to read and send mail through an inbox (MCP or REST). Covers the `npx faivelo init` CLI, the `faivelo` SDKs for Node and Python, the REST API, signed webhooks and the hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ethannschwartz](https://clawhub.ai/user/ethannschwartz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure custom-domain email for apps and agents, including mailboxes, transactional sending, inbound webhooks, and inbox access through MCP or REST.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags the unpinned `npx faivelo` command; its review is partial, so the security evidence is incomplete.

Mitigation: Verify the package version and integrity through a trusted source before running setup, and review the skill before use.

Risk: The documented agent connection can expose Drive or hosted-service capabilities beyond email, and service creation can incur charges.

Mitigation: Grant only the required mailbox access and scopes, prefer an agent key for autonomous use, and get the user's approval before creating paid services.

## Reference(s):

- [Faivelo MCP server](references/mcp.md)
- [Faivelo REST API](references/rest-api.md)
- [Faivelo webhooks](references/webhooks.md)
- [Faivelo developer documentation](https://faivelo.com/docs/developers/coding-agents/)
- [Faivelo API reference](https://faivelo.com/docs/api)
- [Faivelo plans and pricing](https://faivelo.com/docs/billing/plans/?via=clawhub)
- [ClawHub release](https://clawhub.ai/ethannschwartz/skills/faivelo-email)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API calls, Configuration instructions]

**Output Format:** [Markdown with inline shell commands, JSON examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover Node.js, Python, REST, MCP, and webhooks.]

## Skill Version(s):

1.3.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
