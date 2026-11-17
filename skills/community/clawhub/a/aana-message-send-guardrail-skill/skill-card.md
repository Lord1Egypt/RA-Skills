## Description:

Validates message destination, audience, tone, privacy, claims, and approval before an agent sends or posts messages on chat, SMS, DM, or public channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make an agent pause before sending messages, check recipients, channel scope, tone, privacy, claims, and explicit approval, then decide whether to draft, revise, ask, redact, request approval, send, or block.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured external checker could receive sensitive message content if raw messages, screenshots, logs, secrets, customer records, or unrelated thread history are sent for review.

Mitigation: Send only the minimal redacted review payload recommended by the skill and confirm that private details are omitted when a summary is enough.

Risk: An agent may otherwise send to an ambiguous, public, or overly broad destination without explicit approval.

Mitigation: Require exact channel and recipient confirmation, check mentions and broadcast scope, and block or ask when destination, audience, or approval is unclear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mindbomber/skills/aana-message-send-guardrail-skill)
- [Message Send Guardrail Schema](artifact/schemas/message-send-guardrail.schema.json)
- [Redacted Message Send Guardrail Example](artifact/examples/redacted-message-send-guardrail.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style checklist and decision summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; may include a minimal redacted review payload when an AANA checker is configured.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
