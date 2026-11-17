## Description:

Ensures customer support replies are accurate, policy-compliant, minimize private data, avoid unauthorized promises, and recommend safe next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Support agents and agent developers use this instruction-only skill to review customer support drafts before sending, especially replies involving account facts, refunds, policy claims, private data, or high-impact support outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Support review payloads can expose raw account records, payment details, credentials, private messages, or full ticket histories.

Mitigation: Send only redacted summaries to any approved checker or reviewer, and omit raw records, payment data, credentials, and unrelated customer details.

Risk: A support reply can make unsupported account claims or unauthorized refund, credit, policy exception, escalation, or timeline promises.

Mitigation: Verify important claims and authorization through an approved support system or human review before sending, and use conditional review language when facts are missing.

## Reference(s):

- [AANA Support Reply Guardrail Skill on ClawHub](https://clawhub.ai/mindbomber/skills/aana-support-reply-guardrail)
- [Support Reply Review Schema](schemas/support-reply-review.schema.json)
- [Redacted Support Reply Review Example](examples/redacted-support-reply-review.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or structured JSON review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; may use the bundled review schema for redacted support-reply assessments.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact manifest reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
