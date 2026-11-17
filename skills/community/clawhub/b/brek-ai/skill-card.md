## Description:

Integrate with Brek Partner Core Chat API for hotel search and booking assistant flows, including session events, anti-abuse controls, and payment-safe booking steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo9](https://clawhub.ai/user/leo9)

### License/Terms of Use:


## Use Case:

Developers and external product teams use this skill to connect an agent to Brek Partner Core Chat for hotel search, booking, payment setup, session reuse, idempotency, and local call controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment setup links may be insufficiently scoped before being shown to users.

Mitigation: Use only a fixed or allowlisted HTTPS Brek API endpoint and validate payment setup links against documented Brek or payment-provider domains before display.

Risk: The skill handles a partner API key for booking flows.

Mitigation: Keep BREK_PARTNER_API_KEY narrowly scoped, stored outside chat, and rotated through approved operational channels.

Risk: Booking and payment confirmation actions can create financial or transactional side effects.

Mitigation: Require explicit user confirmation and reuse deterministic idempotency keys for booking, payment confirmation, and cancellation events.

## Reference(s):

- [API Templates](artifact/references/api-templates.md)
- [Call Control and Anti-Abuse](artifact/references/call-control.md)
- [Payment and Billing](artifact/references/payment-and-billing.md)
- [ClawHub Skill Page](https://clawhub.ai/leo9/skills/brek-ai)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration, code]

**Output Format:** [Markdown guidance with JSON and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Brek base URL, partner API key, actor and partner identifiers, client action IDs, idempotency keys, and local rate and budget controls.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
