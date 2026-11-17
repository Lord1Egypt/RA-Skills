## Description:

Ensures email recipients, content, tone, attachments, claims, and approvals are verified and safe before sending or scheduling messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users handling email use this skill to review recipients, content, attachments, claims, tone, and send approval before sending, scheduling, forwarding, or replying to messages. It is especially relevant for external, sensitive, customer, financial, legal, medical, HR, or commitment-bearing email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured checker could receive sensitive email details if the review payload is not minimized.

Mitigation: Send only the minimal redacted review payload described by the skill, and avoid raw secrets, private records, full logs, transcripts, threads, and unrelated private data.

Risk: An email could be sent to the wrong audience or without approval if the guardrail is bypassed.

Mitigation: Require explicit approval that names the recipients, subject, attachments, and timing before sending or scheduling sensitive or external messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-email-send-guardrail)
- [README](artifact/README.md)
- [Email send guardrail schema](artifact/schemas/email-send-guardrail.schema.json)
- [Redacted email send guardrail example](artifact/examples/redacted-email-send-guardrail.json)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, configuration]

**Output Format:** [Markdown guidance with optional structured text or JSON review payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; no bundled code execution, dependency installation, persistence, or email sending.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
