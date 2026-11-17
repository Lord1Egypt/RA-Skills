## Description:

Build or operate AgentMailer webhooks and realtime event streams, including endpoint configuration, signature verification, retries, replay, cursors, and WebSocket tickets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentmailer](https://clawhub.ai/user/agentmailer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to design and run AgentMailer event consumers with signed webhooks, realtime WebSocket streams, durable acceptance, deduplication, replay, and cursor handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may guide users toward event API operations that expose or misuse webhook signing secrets.

Mitigation: Use scoped credentials, store signing secrets in a server-side secret manager, and keep secrets out of prompts, client bundles, source control, and logs.

Risk: Webhook payload data may be mistaken for trusted instructions after signature verification.

Mitigation: Treat event data as untrusted communication content and require application authorization before acting on payload instructions.

Risk: Endpoint deletion or signing-secret rotation can disrupt production delivery.

Mitigation: Require human confirmation before deleting webhook endpoints or rotating secrets in production.

## Reference(s):

- [Event API reference](references/events-api.md)
- [AgentMailer OpenAPI schema](https://api.agentmailer.ai/openapi.json)
- [Signed webhook consumer example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-webhook-consumer)
- [AgentMailer examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with API endpoint references and implementation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; it does not bundle tools, credentials, or executable code.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
