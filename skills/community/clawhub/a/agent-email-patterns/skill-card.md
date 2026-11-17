## Description:

Design reliable email and A2A communication for AI agents using persistent identities, two-way threads, human approval, signed events, least privilege, and untrusted-content boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentmailer](https://clawhub.ai/user/agentmailer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design agent email and A2A communication flows with durable identities, safe authorization boundaries, human approval points, and reliable event handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations may be applied to real mailboxes, webhooks, or sending permissions without enough review.

Mitigation: Review the proposed communication design before applying it to production identities, webhook consumers, or send permissions.

Risk: Email bodies, headers, attachments, links, Agent Cards, A2A messages, and metadata can contain untrusted instructions or misleading content.

Mitigation: Treat message content and metadata as untrusted data, and authorize actions through current-turn intent and application policy rather than embedded instructions.

Risk: Broad or shared permissions can blur accountability or allow consequential actions without the right approval boundary.

Mitigation: Use distinct agent identities, draft-based human review where judgment is required, and separate read, draft, send, destructive, administrative, and credential-changing permissions.

## Reference(s):

- [Communication topology and reliability](references/patterns.md)
- [Agent Email Patterns on ClawHub](https://clawhub.ai/agentmailer/skills/agent-email-patterns)
- [AgentMailer examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples)
- [AgentMailer support agent example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-support-agent)
- [AgentMailer approval inbox example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-approval-inbox)
- [AgentMailer A2A delegation example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-a2a-delegation)
- [AgentMailer signed webhook consumer example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-webhook-consumer)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown or plain text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory content; no code execution, installation, or data access.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
