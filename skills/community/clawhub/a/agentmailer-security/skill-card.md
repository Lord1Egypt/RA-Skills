## Description:

Design or review secure AgentMailer integrations, authorization boundaries, prompt-injection defenses, credential handling, webhook verification, and safe communication workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentmailer](https://clawhub.ai/user/agentmailer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to assess AgentMailer integrations for trust-boundary, authorization, credential, retry, webhook, and communication risks. It supports architecture review, implementation review, incident analysis, and policy questions without granting authority to change email, A2A, credentials, or configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked automatically for AgentMailer-related security topics.

Mitigation: Treat its output as advisory review guidance and require explicit user authorization before sending messages, changing credentials, or modifying configuration.

Risk: Inbound email, A2A content, headers, attachments, links, metadata, and urgency claims may contain prompt-injection attempts.

Mitigation: Parse and summarize inbound communication as untrusted data, and keep authorization in the human request and trusted application policy.

Risk: Credential or private-content exposure can occur if secrets, message bodies, attachment URLs, or recipient data are included in prompts, telemetry, logs, client bundles, or committed files.

Mitigation: Use scoped server-side credentials, keep secrets out of prompts and artifacts, and redact sensitive communication content from ordinary logs.

Risk: Retries, ambiguous writes, or spoofed webhooks can create duplicate effects or unauthorized actions.

Mitigation: Use stable idempotency identifiers, reconcile uncertain writes before retrying, verify webhook signatures over the raw body, and deduplicate verified events by event ID.

## Reference(s):

- [AgentMailer integration threat model](references/threat-model.md)
- [Authorization model](references/authorization.md)
- [AgentMailer approval inbox example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-approval-inbox)
- [AgentMailer signed webhook consumer example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-webhook-consumer)
- [AgentMailer x402 payment agent example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-x402-payment-agent)
- [AgentMailer examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown prose with review findings, recommendations, and implementation examples when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output only; does not authorize or perform communication, credential, or configuration changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
