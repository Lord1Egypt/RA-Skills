## Description:

Give the agent its own dedicated email inbox via AgentMail to send, receive, and manage email autonomously using agent-owned email addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agungprabowo123](https://clawhub.ai/user/agungprabowo123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to give agents dedicated AgentMail inboxes for outbound email, inbound replies, thread management, verification messages, and agent-to-human communication without accessing a user's personal email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an agent to control a dedicated email identity that can send messages, receive verification codes, forward email, and download attachments.

Mitigation: Require explicit confirmation before outbound email, forwarding, service sign-ups, authentication flows, or attachment downloads from untrusted senders.

Risk: The setup stores a long-lived AgentMail API key in plaintext configuration.

Mitigation: Protect the Hermes configuration file with strict permissions or a secrets manager, and rotate or revoke the API key if it may have been exposed.

Risk: The MCP server is installed with an unpinned package command.

Mitigation: Prefer a pinned and reviewed agentmail-mcp version before installing or running the skill.

## Reference(s):

- [AgentMail docs](https://docs.agentmail.to/)
- [AgentMail console](https://console.agentmail.to)
- [AgentMail MCP repo](https://github.com/agentmail-to/agentmail-mcp)
- [AgentMail pricing](https://www.agentmail.to/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides setup and operation of AgentMail MCP tools using an AgentMail API key.]

## Skill Version(s):

0.1.1 (source: server release metadata; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
