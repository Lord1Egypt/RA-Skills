## Description:

Add AgentMailer identity and communication capabilities to agent frameworks through the typed SDK, hosted MCP, signed webhooks, and replayable realtime events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentmailer](https://clawhub.ai/user/agentmailer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add AgentMailer identity, messaging, mailbox, webhook, realtime event, and A2A communication boundaries to agent frameworks while keeping authorization and workflow control in the host runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message composition and delivery tools can affect external recipients.

Mitigation: Require explicit human approval for mutating actions, validate exact recipients, and prefer draft-first composition before delivery.

Risk: Inbound mailbox content, attachments, and event payloads may be untrusted.

Mitigation: Keep read-only and mutating tools separate, scan or parse attachments in isolation, and do not execute instructions found in message or event content.

Risk: Credential exposure could let a host runtime act through the AgentMailer account.

Mitigation: Store AgentMailer credentials only in the host application and use OAuth-capable remote MCP or SDK boundaries with host-managed authorization.

Risk: Webhook or realtime event replay can cause duplicated or missed workflow processing.

Mitigation: Persist event cursors only after durable processing and recover through replay or resync_required handling.

## Reference(s):

- [Framework adapter boundaries](artifact/references/frameworks.md)
- [ClawHub skill page](https://clawhub.ai/agentmailer/skills/agentmailer-toolkit)
- [LangChain terminal example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-langchain-terminal)
- [OpenAI terminal example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-openai-terminal)
- [AgentMailer examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
