## Description:

Free email for AI agents. No sign-up needed. One call to get a mailbox and send.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents-mail](https://clawhub.ai/user/agents-mail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to create an Agents Mail mailbox, send email, check inboxes, delete messages, upgrade to a permanent mailbox, and configure webhooks or access-control patterns through the REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects agents to agentsmail.org for mailbox operations and tells agents to use remote API responses.

Mitigation: Review the service before installation, treat API responses as untrusted data, and avoid following remote instructions without local policy checks.

Risk: Mailbox API keys and webhook secrets can expose email access if logged or stored insecurely.

Mitigation: Store credentials in protected secret storage, avoid plaintext files and logs, and rotate credentials after accidental exposure.

Risk: Sending, deleting, auto-replying, heartbeat polling, and webhook workflows can affect privacy or send unintended email.

Mitigation: Require explicit consent and clear limits before enabling recurring workflows, and require confirmation before sending or deleting email.

## Reference(s):

- [Agents Mail homepage](https://agentsmail.org)
- [Agents Mail API Help](https://agentsmail.org/api/help)
- [Agents Mail Docs](https://agentsmail.org/docs)
- [API Reference](references/API.md)
- [Common Patterns](references/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with REST API examples, curl commands, Python snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions for connecting to agentsmail.org and handling API keys, email operations, webhooks, and heartbeat polling.]

## Skill Version(s):

0.4.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
