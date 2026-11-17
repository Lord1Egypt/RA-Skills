## Description:

AI机票助手 supports domestic flight search, fare and cabin detail lookup, booking orders, flight changes, refunds, cancellations, and order-detail queries through Python command-line tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search domestic flights, compare cabin prices and rules, create bookings, inspect orders, and request flight changes or refunds after authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passenger identity details and authentication data may be exposed through local storage, command arguments, or terminal output.

Mitigation: Use only in a trusted local environment, avoid shared machines, and redact passenger names, phone numbers, identity numbers, and API keys from logs and responses.

Risk: Network protections and endpoint validation are not strong enough for real booking workflows.

Mitigation: Do not use for real bookings, changes, or refunds until TLS verification and endpoint validation are fixed and reviewed.

Risk: Booking, payment, flight-change, and refund actions can have financial or travel consequences.

Mitigation: Require explicit user confirmation immediately before any booking, payment, change, cancellation, or refund submission, including zero-fee refunds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/ai-flight)
- [Fenbeitong flight service endpoint](https://app-gate.fenbeitong.com/air_biz/skill/execute)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with plaintext table blocks, command examples, and short status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include order identifiers, payment links, passenger details, refund estimates, and temporary local state created by helper scripts.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
