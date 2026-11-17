## Description:

Sends transactional email through Drin by helping an agent choose a verified sending domain, compose content, send through MCP, CLI, SDK, or REST, and handle delivery-related errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atom00blue](https://clawhub.ai/user/atom00blue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send notifications, receipts, OTPs, alerts, password resets, and replies through the Drin email API while handling common delivery errors honestly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send email to unintended recipients or with inappropriate content.

Mitigation: Confirm the sender domain, recipients, subject, body, and authorization before sending.

Risk: Email content is transmitted to an external email provider and could expose secrets or regulated data.

Mitigation: Avoid secrets or regulated data unless explicit authorization and safeguards are in place.

Risk: Retrying a delivery action can create duplicate transactional emails.

Mitigation: Use an idempotency key for retryable sends such as receipts and OTPs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atom00blue/skills/drin-send-email)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Drin MCP, CLI, SDK, or REST instructions and example email payloads.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
