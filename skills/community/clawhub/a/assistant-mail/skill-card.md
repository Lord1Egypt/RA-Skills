## Description:

Assistant Mail lets agents use managed email mailboxes through MCP with API key authentication, allowlisted outbound sending, consent controls, retention controls, and send caps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[assistantmail](https://clawhub.ai/user/assistantmail)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and small teams use this skill to connect OpenClaw, Hermes, Claude, or OpenAI agents to Assistant Mail mailboxes for listing, reading, sending, replying, recipient management, and usage checks through MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can connect real mailboxes through an unverified third-party MCP using an API key with broad mailbox read, send, update, and delete authority.

Mitigation: Review before installing, use a narrowly scoped and revocable API key when available, avoid broad mailbox or delete permissions where possible, and confirm the assistantmail-mcp package provenance and version before use.

Risk: Changing ASSISTANT_MAIL_API_BASE_URL can route mailbox operations to a non-default endpoint.

Mitigation: Keep ASSISTANT_MAIL_API_BASE_URL at the default hosted endpoint unless you deliberately trust the replacement endpoint.

Risk: Mailbox operations require the correct mailboxId and API key, so mishandled credentials or mailbox identifiers could expose or affect the wrong mailbox.

Mitigation: Store the API key securely, share it only with the intended agent runtime, and verify the target mailboxId from the mailbox listing before read, send, update, or delete actions.

## Reference(s):

- [Assistant Mail documentation](https://assistant-mail.ai/docs)
- [Assistant Mail ClawHub skill page](https://clawhub.ai/assistantmail/skills/assistant-mail)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP tool names, environment variables, API key handling notes, mailboxId requirements, and example tool inputs.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
