## Description:

Helps an agent register and use a Crustacean Email Gateway mailbox for an OpenClaw identity, including token recovery, inbox and outbox access, message status updates, forwarding configuration, and outbound email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nycomar](https://clawhub.ai/user/nycomar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create and manage a Crustacean Email Gateway mailbox tied to an OpenClaw identity. It supports registration, bearer-token recovery, mailbox lookup, inbox and outbox review, status changes, forwarding, and outbound sending through the gateway API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles mailbox bearer tokens and OpenClaw identity material for registration, recovery, reading, sending, status changes, and forwarding.

Mitigation: Install only when the Crustacean Email Gateway service is trusted, protect the local token file with restrictive permissions, and avoid sharing JSON output from registration or recovery.

Risk: A custom API base could route identity and mailbox operations to an unintended service.

Mitigation: Use the default API base or a custom API base only when it is controlled and intentionally configured.

Risk: Mailbox forwarding can send inbound mail to an external destination without a verification flow.

Mitigation: Review forwarding changes before applying them, confirm the destination address manually, and disable forwarding when it is no longer needed.

## Reference(s):

- [Crustacean Email Gateway API Reference](artifact/references/api.md)
- [Usage Examples](artifact/references/examples.md)
- [Crustacean Email Gateway API](https://api.crustacean.email/api/v1)
- [Create And Use New Agent Email Address on ClawHub](https://clawhub.ai/nycomar/skills/create-email-address)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or write local mailbox token metadata and call the Crustacean Email Gateway API.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
