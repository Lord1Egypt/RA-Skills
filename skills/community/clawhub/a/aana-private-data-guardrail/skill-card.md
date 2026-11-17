## Description:

AANA-grounded privacy guardrail instructions for preventing agents from exposing private account, billing, payment, health, legal, personal, or sensitive business data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before drafting, summarizing, sending, storing, or transforming private data so responses are necessary, authorized, minimized, and safe. It is especially relevant for account, billing, payment, health, legal, personal, HR, student, customer, and sensitive business workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive data could be included in review payloads sent to an external checker.

Mitigation: Send only minimal redacted summaries and use only trusted checkers configured by the user or administrator.

Risk: The skill is a privacy review aid, not a compliance system.

Mitigation: Route high-impact, irreversible, or compliance-sensitive actions to a verified system or human review.

Risk: Unsupported account, billing, payment, health, legal, or personal facts could be introduced into a response.

Mitigation: Ask, verify, revise, or defer instead of inventing private facts or eligibility outcomes.

## Reference(s):

- [AANA Private Data Guardrail Skill on ClawHub](https://clawhub.ai/mindbomber/skills/aana-private-data-guardrail)
- [Private data review schema](artifact/schemas/private-data-review.schema.json)
- [Redacted private data review example](artifact/examples/redacted-private-data-review.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Agent-facing guidance with an optional redacted JSON review payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; does not execute commands, call services, persist memory, or write files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
