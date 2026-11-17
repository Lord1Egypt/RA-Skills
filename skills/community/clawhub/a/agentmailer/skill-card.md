## Description:

Build with AgentMailer's typed TypeScript, Python, Rust, Ruby, Go, or Swift SDK for persistent agent identities, email, A2A communication, events, domains, and policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentmailer](https://clawhub.ai/user/agentmailer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement AgentMailer SDK integrations for durable agent identities, email, A2A communication, events, domains, and policy while preserving safe delivery boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys, durable identities, or outbound messages could be misused if credentials are exposed or identity creation and sending are automated without approval.

Mitigation: Store AGENTMAILER_API_KEY in server-side secret storage and require explicit business approval before creating identities or sending messages.

Risk: Email, attachments, A2A messages, and event payloads can contain untrusted content.

Mitigation: Treat payloads as untrusted input, verify webhook signatures over the unmodified body, and durably accept events before asynchronous processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentmailer/skills/agentmailer)
- [SDK language guide](references/languages.md)
- [AgentMailer OpenAPI schema](https://api.agentmailer.ai/openapi.json)
- [AgentMailer quickstart](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-quickstart)
- [AgentMailer examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include language-specific SDK guidance, configuration steps, API usage patterns, and safety checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
