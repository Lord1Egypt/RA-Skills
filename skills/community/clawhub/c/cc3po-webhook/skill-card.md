## Description:

Implement secure webhook receivers and senders with proper verification and reliability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carloscbrls](https://clawhub.ai/user/carloscbrls)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design webhook receivers and senders with HMAC verification, replay prevention, idempotency, retry handling, and delivery tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook debugging logs may expose full URLs, tokens, query strings, headers, payloads, or response bodies.

Mitigation: Log endpoint identifiers, status codes, timings, sizes, and correlation IDs by default; redact sensitive data, restrict access, and keep retention short.

Risk: Webhook implementation guidance can be applied incorrectly in production systems.

Mitigation: Review proposed receiver and sender behavior before deployment, especially signature verification, replay prevention, idempotency, retry handling, and logging.

## Reference(s):

- [CC3PO Webhook Skill Page](https://clawhub.ai/carloscbrls/skills/cc3po-webhook)
- [ClawHub metadata homepage](https://clawhub.ai/carloscbrls/webhook)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with inline examples and implementation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides webhook security and reliability recommendations; no executable tools are included.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
