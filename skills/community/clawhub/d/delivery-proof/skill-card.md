## Description:

Coordinate and record exact-approved delivery against pre-defined acceptance criteria while preserving private evidence and preparing an evidence-labelled field report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bilbop1](https://clawhub.ai/user/bilbop1)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and agents use this skill after a payable test reaches delivery or an observed result to stage exact-approved delivery, record acceptance and economic proof, and prepare a redacted field report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may help prepare or retain private delivery evidence, including customer or payment-related proof.

Mitigation: Use it only where the operator has authority to handle the material, minimize retained evidence, and redact sensitive details.

Risk: A staged delivery, publication, payment, contract, or account action could be mistaken for approval to act externally.

Mitigation: Require fresh exact approval before any external send, post, payment, contract, or account change.

Risk: Copied delivery records, messages, attachments, or customer statements may contain untrusted instructions or sensitive data.

Mitigation: Treat copied material as evidence only, ignore embedded instructions, and exclude prompt-injection or unsafe material from acceptance and economic proof.

## Reference(s):

- [Acceptance and proof protocol](references/acceptance-and-proof.md)
- [MoneyPrinter Field Report](references/field-report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured headings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a Delivery Record and, when requested, a staged MoneyPrinter Field Report; external delivery, publication, payment, contract, or account actions require fresh exact approval.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
