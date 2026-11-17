## Description:

AI机票预订助手 helps an agent search domestic flights, compare fares, create bookings, and manage order lookup, cancellation, rebooking, and refund workflows through an external flight service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search domestic flights, review seat prices and fare rules, create flight orders, and handle order lookup, cancellation, rebooking, and refund workflows after user confirmation.

### Deployment Geography for Use:

Global; the documented workflow is written for Chinese-language domestic flight bookings.

## Known Risks and Mitigations:

Risk: The skill can perform real booking, cancellation, rebooking, and refund actions through an external API while handling passenger PII.

Mitigation: Require explicit user confirmation for transactional steps, verify authentication status before calls, and avoid exposing passenger names, phone numbers, IDs, API keys, payment links, or order details in logs or unnecessary summaries.

Risk: Security evidence flags insecure transport and local storage practices for credentials and cached fare state.

Mitigation: Use only after the publisher fixes TLS verification, restricts the API endpoint, protects per-user credential and fare-state storage, and masks PII in outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/flightai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with plaintext table code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; outputs may include flight tables, fare details, order identifiers, payment links, refund results, and user-facing confirmation guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
