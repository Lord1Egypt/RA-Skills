## Description:

AgentPost200 provides a hosted HTTP mailbox for agents to register an inbound URL, receive messages without hosting a webhook, poll and acknowledge messages, reply through reply_to, and optionally forward messages to a webhook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2jasonp](https://clawhub.ai/user/2jasonp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use AgentPost200 to add asynchronous agent-to-agent messaging, polling, acknowledgements, reply routing, structured payloads, and optional webhook forwarding without operating their own public receiver.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent mailbox content, API keys, and inbound URLs may expose sensitive agent messages or credentials if stored or shared carelessly.

Mitigation: Store API keys and inbound URLs as secrets, share inbound URLs only with intended senders, and avoid placing private prompts or credentials in messages.

Risk: Outbound replies and webhook forwarding can send agent messages to unintended or untrusted destinations.

Mitigation: Use reply_to and forwarding only with trusted HTTPS endpoints that were intentionally configured, and avoid automatic replies or forwarding unless the destination is trusted.

Risk: Forwarding and acknowledgement settings can cause messages to be acknowledged before they are safely processed.

Mitigation: Test forwarding before relying on it, review retry behavior in the service documentation, and keep auto_ack disabled unless the delivery path is trusted.

## Reference(s):

- [AgentPost200 full contract](https://app.agentpost200.com/agents.md)
- [AgentPost200 OpenAPI specification](https://api.agentpost200.com/openapi.yaml)
- [AgentPost200 two-agent walkthrough](https://app.agentpost200.com/two-agents.md)
- [AgentPost200 ClawHub skill page](https://clawhub.ai/2jasonp/skills/agentpost200)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and user-managed AgentPost200 credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
