## Description:

API-first email platform designed for AI agents that supports dedicated inboxes, programmatic sending and receiving, webhooks, and email-based workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayapower](https://clawhub.ai/user/mayapower)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to create agent email identities, send and receive email through AgentMail, and connect inbound messages to webhook-driven workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incoming email and webhook payloads may contain untrusted instructions or sensitive email content.

Mitigation: Allowlist trusted senders, isolate inboxes per workflow, verify webhook signatures, and treat email content as untrusted input before an agent acts on it.

Risk: Webhook and attachment examples can expose email contents or write files unsafely if copied into production use.

Mitigation: Avoid logging full webhook payloads, sanitize attachment filenames, redact or obtain consent before copying email contents into external systems, and review integrations before production use.

Risk: AgentMail credentials could be overexposed if shared across workflows.

Mitigation: Use a dedicated AgentMail API key and scope operational access to the specific inboxes and workflows that need it.

## Reference(s):

- [AgentMail API Reference](references/API.md)
- [AgentMail Webhooks Guide](references/WEBHOOKS.md)
- [AgentMail Usage Examples](references/EXAMPLES.md)
- [AgentMail Console](https://console.agentmail.to)
- [AgentMail API Base URL](https://api.agentmail.to/v0)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python snippets, shell commands, and runnable helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AGENTMAIL_API_KEY for authenticated AgentMail API operations.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
