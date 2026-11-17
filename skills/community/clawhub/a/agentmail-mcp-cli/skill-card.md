## Description:

Manage AI agent email accounts via the AgentMail API, including inbox creation, thread inspection, email send, reply, forward, label, and attachment workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flohiwg](https://clawhub.ai/user/flohiwg)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let an agent manage AgentMail inboxes, inspect threads, send or reply to email, organize messages with labels, and retrieve attachment links through the AgentMail CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a mutable npm-distributed CLI and grants mailbox access through an AgentMail API key.

Mitigation: Install only from a trusted package source, prefer pinned package versions or an isolated environment, and use the narrowest AgentMail API key available.

Risk: Email send, reply, forward, label-update, attachment-access, and inbox-delete commands can affect mailbox contents, external recipients, or persistent resources.

Mitigation: Review recipients, message content, labels, attachment identifiers, inbox identifiers, and destructive operations before approving command execution.

## Reference(s):

- [AgentMail documentation](https://docs.agentmail.to)
- [AgentMail homepage](https://agentmail.to)
- [AgentMail CLI repository](https://github.com/FloHiwg/agentmail-cli)
- [AgentMail MCP server](https://github.com/agentmail-to/agentmail-mcp)
- [AgentMail Node SDK](https://github.com/agentmail-to/agentmail-node)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command option tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, the agentmail CLI, and AGENTMAIL_API_KEY; documented commands can send, forward, update, or delete email resources.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
