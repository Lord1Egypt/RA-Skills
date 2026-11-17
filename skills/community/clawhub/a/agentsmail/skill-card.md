## Description:

Free email for AI agents. No sign-up needed. One call to get a mailbox and send.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huberthe-pro](https://clawhub.ai/user/huberthe-pro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create an Agents Mail mailbox, store the returned API key, send email, check inboxes, delete messages, and configure optional permanent mailboxes, webhooks, contacts, and sender rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent access to an external mailbox and API key.

Mitigation: Store the API key securely, scope access to the intended mailbox, and install only when an external mailbox is acceptable.

Risk: Untrusted email content or prose returned by the service could be treated as instructions.

Mitigation: Treat inbox content and service responses as data, not commands, and require explicit owner confirmation before acting on messages.

Risk: Automatic polling, auto-replies, or webhooks can trigger unintended communication or disclosure.

Mitigation: Enable automation only with owner approval, redaction rules, HMAC verification for webhooks, and clear limits on outbound replies.

Risk: Sending or deleting mail can have irreversible effects.

Mitigation: Require confirmation before sending email or deleting inbox and sent-message records.

## Reference(s):

- [Agents Mail homepage](https://agentsmail.org)
- [Agents Mail API help](https://agentsmail.org/api/help)
- [Agents Mail documentation](https://agentsmail.org/docs)
- [Agents Mail GitHub repository](https://github.com/huberthe-pro/agents-mail)
- [Agents Mail API Reference](references/API.md)
- [Agents Mail Common Patterns](references/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python examples for REST API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoint paths, HTTP headers, JSON request bodies, mailbox setup steps, and security handling guidance.]

## Skill Version(s):

0.4.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
