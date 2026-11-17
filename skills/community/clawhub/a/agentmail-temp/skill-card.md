## Description:

AgentMail helps agents create and manage dedicated inboxes, send and receive email, and handle email workflows through webhooks and real-time events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liguang00806](https://clawhub.ai/user/liguang00806)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to create agent email identities, send and receive email programmatically, poll inboxes, and connect incoming messages to webhook-driven workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incoming email and webhook payloads can contain untrusted instructions that attempt prompt injection or unsafe downstream actions.

Mitigation: Allowlist trusted senders, process untrusted messages in isolated review sessions, mark email content as untrusted input, and require human approval before forwarding content to other systems.

Risk: The skill handles AgentMail API keys, email contents, webhook payloads, and test-server logs that may contain sensitive data.

Mitigation: Use isolated API keys and dedicated inboxes, avoid production data in local tests, bind receivers to localhost unless intentionally exposed, and redact logs.

Risk: Public webhook endpoints can be spoofed, retried, or abused if receiver controls are weak.

Mitigation: Use HTTPS, verify webhook signatures, validate payload structure, apply rate limiting, and handle webhook events idempotently.

## Reference(s):

- [AgentMail API Reference](artifact/references/API.md)
- [AgentMail Webhooks Guide](artifact/references/WEBHOOKS.md)
- [AgentMail Usage Examples](artifact/references/EXAMPLES.md)
- [AgentMail Console](https://console.agentmail.to)
- [AgentMail API Base URL](https://api.agentmail.to/v0)
- [ClawHub Skill Page](https://clawhub.ai/liguang00806/skills/agentmail-temp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AGENTMAIL_API_KEY when the bundled scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
