## Description:

Helps set up custom-domain email and integrate mailboxes, transactional sending, inbound webhooks, and agent inbox access through Faivelo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ethannschwartz](https://clawhub.ai/user/ethannschwartz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and domain owners use this skill to set up mailboxes, send application email, receive inbound events, and connect an agent to an inbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mail, alias, or DNS changes can disrupt delivery or affect other users.

Mitigation: Require explicit approval before sending, deleting, or changing mailboxes, aliases, or DNS; confirm any MX migration or forced edit.

Risk: Broad credentials can expose inbox contents or unrelated Drive files.

Mitigation: Use a restricted agent key with only the needed mailbox and scopes; omit drive:read unless explicitly required.

Risk: The setup command executes an unpinned package.

Mitigation: Use a pinned or otherwise verified Faivelo CLI version in sensitive environments.

Risk: API keys, mailbox passwords, and webhook secrets may leak through configuration or logs.

Mitigation: Keep credentials out of source control and logs, prefer authorization headers, and verify webhook signatures before processing events.

## Reference(s):

- [Faivelo Email ClawHub release](https://clawhub.ai/ethannschwartz/skills/faivelo-email)
- [Faivelo documentation for coding agents](https://faivelo.com/docs/developers/coding-agents/)
- [Faivelo API reference](https://faivelo.com/docs/api)
- [MCP server guide](references/mcp.md)
- [REST API guide](references/rest-api.md)
- [Webhook guide](references/webhooks.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions, Markdown]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a mailbox setup summary and DNS records requiring attention.]

## Skill Version(s):

1.2.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
