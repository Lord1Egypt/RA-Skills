## Description:

Integrates AgentMail API workflows so agents can create inboxes, send and receive email, and handle email events through polling, webhooks, and helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synesthesia-wav](https://clawhub.ai/user/synesthesia-wav)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add AgentMail-backed email identity, inbox management, outbound email, inbound message processing, and webhook-driven workflows to agent systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted inbound email and webhook payloads can cause prompt injection or unintended agent actions.

Mitigation: Process only verified senders, mark email content as untrusted context, filter suspicious content, and require human review for consequential actions.

Risk: Attachment download examples can mishandle untrusted filenames or files.

Mitigation: Use safe filename handling, store attachments in a controlled directory, scan or quarantine untrusted files, and avoid automatic downstream processing.

Risk: Auto-responder, digest, Slack forwarding, and distributed sending examples can leak sensitive email content or send unwanted messages.

Mitigation: Forward or distribute only authorized non-sensitive content, require opt-in recipient controls, add rate limits, and use exact approval tokens before sending consequential mail.

Risk: Webhook endpoints may receive unauthenticated or unexpected events.

Mitigation: Verify webhook signatures or shared secrets, subscribe only to needed events, log blocked attempts, and fail closed on invalid payloads.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/synesthesia-wav/skills/agentmail-integration)
- [AgentMail Console](https://console.agentmail.to)
- [API Reference](references/API.md)
- [Webhook Setup and Security](references/WEBHOOKS.md)
- [AgentMail Common Patterns](references/patterns.md)
- [AgentMail Examples](references/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose AgentMail API calls and helper script invocations; live use requires AGENTMAIL_API_KEY.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
