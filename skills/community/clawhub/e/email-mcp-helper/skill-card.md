## Description:

Email MCP Helper gives agents a reference for using a self-hosted email MCP server to read, search, send, organize, and manage email across configured IMAP/SMTP accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced users use this skill as a tool reference for connecting agents to an already deployed email MCP endpoint and safely selecting account, mailbox, message, and mutation parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox credentials and message contents can be exposed if the configured MCP endpoint is not controlled or independently verified.

Mitigation: Use only an MCP endpoint you control or have independently verified, and rotate and scope API keys.

Risk: The available tools can perform mutating email actions, including sending, forwarding, bulk moving, deleting, and permanent deletion.

Mitigation: Require explicit user confirmation before any mutating email action, especially bulk operations and permanent deletion.

Risk: The email MCP image or proxy deployment can change behavior if mutable or unaudited versions are used.

Mitigation: Pin the email MCP image and proxy to audited immutable versions before use.

Risk: Incorrect account names, mailbox paths, or email IDs can cause actions to target the wrong mailbox or message.

Mitigation: Call list_accounts and list_mailboxes before mailbox operations, and use email IDs returned by list_emails or search_emails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/encryptshawn/skills/email-mcp-helper)
- [email-mcp source code](https://github.com/codefuturist/email-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tool reference with example call sequences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [References an externally deployed email MCP server and does not bundle credentials or infrastructure.]

## Skill Version(s):

1.0.2 (source: server release evidence, created 2026-05-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
